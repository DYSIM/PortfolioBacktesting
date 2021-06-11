# Hobby Project: Portfolio Backtesting with BackTrader

Implementing Markowitz portfolio optimization with [pyportfolioopt](https://pyportfolioopt.readthedocs.io/en/latest/), backtest a strategy to rebalance the tangency portfolio (max sharpe) every half a month.

Instructions:

Run 'pip install -r requirements.txt'

Run 'Python backtest.py'

Price data of the tickers will be downloaded as csv files.

Backtesting framework used is [backtrader](https://www.backtrader.com/).

-------------------------------------------------------

# Theory

Under Markowitz's portfolio theory, the efficient frontier is the curve which consists of all the portfolios that generate highest return for the given level of risk in the set of all portfolios. Mathematically, can be obtained by minimizing the variance of the portfolio, subject to constraints.

![alt text](https://www.niceideas.ch/airxcell_doc/doc/images/marko_1.png)




# Tangency portfolio

The most optimal portfolio in terms of risk and reward is not the minimum variance portfolio, but instead the one with maximum sharpe ration. Sharpe ratio is the expected return, accounting for the amount of risk taken

![alt text](https://a.c-dn.net/c/content/dam/publicsites/igcom/uk/images/ContentImage/Sharpe%20ratio.png)


To locate this portfolio, we require the Capital Market Line as well, as the point where CML is tangent to efficient frontier is the tangency portfolio. The sharpe ratio is actually the the slope of the CML.

![alt text](https://cdn.wallstreetmojo.com/wp-content/uploads/2019/10/Capital-Market-Line.png.webp)

Using the Capital Market Line, an optimization problem can be stated and solved by [pyportfolioopt](https://pyportfolioopt.readthedocs.io/en/latest/).



*ALL images found on google*
