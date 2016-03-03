import numpy as np
import pandas as pd
import Quandl


def get_adj_close(tickers, start="", end="", ratio=True):
    """
    Returns DataFrame with the adjusted close values for the 
        tickers passed in during the time frame specified
    """
    
    result = {}
    
    for ticker in tickers:
        try:
            result[ticker] = Quandl.get("WIKI/"+ticker, trim_start=start, trim_end=end)['Adj. Close']
        except DatasetNotFound:
            print(ticker, 'is not a vaild ticker')
            return
    
    if ratio:
        if result[tickers[0]].mean() > result[tickers[1]].mean():
            result[tickers[0]+'/'+tickers[1]] = result[tickers[0]]/result[tickers[1]]
        else:
            result[tickers[1]+'/'+tickers[0]] = result[tickers[1]]/result[tickers[0]]
    
    return pd.DataFrame(result).dropna()
