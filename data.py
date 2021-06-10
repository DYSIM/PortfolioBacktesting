import yfinance as yf
import pandas as pd


def yfinancedata(tickers: list):
    for ticker in tickers:
        data = yf.download(tickers = ticker, period = '5y')
        data.to_csv(ticker+'.csv')

    return
