import backtrader as bt
import datetime
from datetime import timedelta
import pandas as pd
from markowitz_portfolio import getMaxSharpePortfolio

class MaxSharpeStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def start(self):
        self.val_start = self.broker.get_cash()  # keep the starting cash

    def stop(self):
        # calculate the actual returns
        self.roi = (self.broker.get_value() / self.val_start) - 1.0
        print('ROI:        {:.2f}%'.format(100.0 * self.roi))


    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    '%s BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f, Cash Available %.2f' %
                    (order.data._name,
                     order.executed.price,
                     order.executed.value,
                     order.executed.comm,
                     self.broker.get_cash()))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('%s SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f, Cash Available %.2f' %
                        (order.data._name,
                         order.executed.price,
                         order.executed.value,
                         order.executed.comm,
                         self.broker.get_cash()))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        today = self.datas[0].datetime.datetime()
        day = today.day
        if day % 15 == 0:
            end = today - timedelta(days = 1) # calculate up to yesterday
            start = end - timedelta(days = 365.24) # 1 year of data

            #format into dataframe
            tickers = [d._name for d in self.datas]
            data_adj_close = None

            # print(today.strftime("%Y-%m-%d"),start.strftime("%Y-%m-%d"),end.strftime("%Y-%m-%d"))
            for i in tickers:

                temp = pd.read_csv(i+'.csv')
                temp.Date = pd.to_datetime(temp.Date)
                temp = temp.loc[(temp.Date <= end) &
                                (temp.Date >= start)]
                try:
                    data_adj_close[i] = temp['Adj Close']
                except:
                    data_adj_close = pd.DataFrame()
                    data_adj_close[i] = temp['Adj Close']

            sharpe_portfolio = getMaxSharpePortfolio(data_adj_close)


            # print(sharpe_portfolio)
            sharpe_portfolio = list(sharpe_portfolio.items())
            # print(sharpe_portfolio)
            sharpe_portfolio_sell_first = []
            for name, amount in sharpe_portfolio:
                currposition = self.getposition(data = self.getdatabyname(name))
                percentage = (currposition.size *currposition.price) / self.broker.getvalue()
                sharpe_portfolio_sell_first.append((name,amount,amount - percentage))



            sharpe_portfolio_sell_first = sorted(sharpe_portfolio_sell_first, key=lambda t: t[2])
            print(sharpe_portfolio_sell_first)
            for name, amount, change in sharpe_portfolio_sell_first:
                if change == 0.0:
                    continue
                self.log('Order Created for %s to target percentage %.2f' %
                         (name, amount))
                self.order = self.order_target_percent(self.getdatabyname(name), amount)
