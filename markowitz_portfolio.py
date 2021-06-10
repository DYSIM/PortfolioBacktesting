import numpy as np
import pandas as pd
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from datetime import datetime, timedelta

import yfinance as yf


def getMaxSharpePortfolio(data_adj_close):
    # print(data_adj_close.head())
    avg_returns = expected_returns.mean_historical_return(data_adj_close, compounding=True) # mean return
    cov_mat = risk_models.sample_cov(data_adj_close) # sample covariance
    # print(avg_returns)
    ef = EfficientFrontier(avg_returns, cov_mat)
    weights = ef.max_sharpe() # get allocation with max sharpe
    cleaned_weights = ef.clean_weights()
    return cleaned_weights
