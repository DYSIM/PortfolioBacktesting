import backtrader as bt
import datetime
from datetime import timedelta
import os
import sys
from data import yfinancedata
import pandas as pd

from MaxSharpeStrategy import MaxSharpeStrategy



if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(MaxSharpeStrategy)


    tickers = ['GM', 'MCD', 'NKE', 'AAPL', 'MSFT', 'JNJ', 'JPM', 'BA', 'C', 'ARKK']

    # pricedatadf = yfinancedata(tickers)

    for i in range(len(tickers)):
        ticker = tickers[i]


        # Create a Data Feed
        data = bt.feeds.YahooFinanceCSVData(
            dataname=ticker+'.csv',
            name=ticker,
            # Do not pass values before this date
            fromdate=datetime.datetime(2018, 1, 15),
            # Do not pass values after this date
            todate=datetime.datetime(2021, 12, 31),
            reverse=False)

        # Add the Data Feed to Cerebro
        cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(10000.0)

    # # Add a FixedSize sizer according to the stake
    # cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    # 0.08% ... divide by 100 to remove the %
    cerebro.broker.setcommission(commission=0.0008)

    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe")
    cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='annual')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    session = cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    strat = session[0]
    print('Sharpe Ratio:', strat.analyzers.sharpe.get_analysis())
    print('Annual Returns:', strat.analyzers.annual.get_analysis())
    print('DrawDowns:', strat.analyzers.drawdown.get_analysis())
    print('Trade Analysis:', strat.analyzers.ta.get_analysis())
