import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import *
import seaborn as sns
import statsmodels.api as sm

sns.set_style("whitegrid", {'axes.edgecolor': '.6', 
                            'axes.facecolor': '0.9', 
                            'grid.color': '.82', 
                            'legend.frameon': True,
                            'axes.labelsize': 'small'})

def get_lagged_series(series, order=1, log=False):
    lagged = None
    if log:
        lagged = np.log(series).diff(order).dropna();
    else:
        lagged = series.diff(order).dropna();
    
    return lagged

def plot_stocks(index, stocks, labels, positions=None, label_annually=True):
    """
    Plots up to 5 stocks
    
    Args:
        index (DateTimeIndex): date range
        stocks (list): list of stocks to plot
        labels (list): labels to use for plotting
        positions (list of dicts): optional postions to overplot
        label_annually (boolean): plots x label monthly if false, annually otherwise
        
    Returns (None): Will output plot inline
    """
    colors = ['firebrick','steelblue','orange','mediumorchid', 'mediumseagreen']
    
    fig, ax = plt.subplots(figsize=(20,8));
    
    if label_annually:
        span = YearLocator();
        my_format = DateFormatter('%Y');
    else:
        span = MonthLocator();
        my_format = DateFormatter('%b %Y');    
    
    ax.xaxis.set_major_locator(span);
    ax.xaxis.set_major_formatter(my_format);
    ax.autoscale_view();
    
    plt.title('Adjusted Close Prices', fontsize=20);
    plt.ylabel('Adj. Close', fontsize=15);
    plt.xlabel('Time', fontsize=15);
    
    for stock, label, color in zip(stocks, labels, colors):
        ax.plot_date(index, stock, color=color, linestyle='-', marker=None, label=label);
        plt.xticks(rotation=45)
    
    if positions:
        for position in positions:
            ax.axvline(df.index[position['open']], color='lime', linestyle='-')
            ax.axvline(df.index[position['close']], color='red', linestyle='-')
 
    plt.legend(loc=2, prop={'size':15}, frameon=True);

def plot_lagged_series(series, order=1, log=False):
    """
    Plots lagged series
    
    Args:
        series (ndarray): time series
        order (int): the order of the difference
        log (boolean): whether to log transform before difference
    
    Returns (None): plots inline
    """
    plt.figure(figsize=(8,4));
    plt.xlabel('Time Index');
    plt.ylabel('Difference');
    
    if log:
        plt.title('Log Series Lagged by ' + str(order));
        lagged = get_lagged_series(series, order, log)
    else:
        plt.title('Series Lagged by ' + str(order));
        lagged = get_lagged_series(series, order, log)
        
    plt.plot(np.arange(0,lagged.size,1), lagged);

def plot_correlograms(series, limit=50):
    fig = plt.figure(figsize=(15,8));
    ax1 = fig.add_subplot(211);
    fig = sm.graphics.tsa.plot_acf(series, lags=limit, ax=ax1);
    plt.title('Correlogram');
    plt.xticks(np.arange(0,limit+1,1))
    plt.xlim([-1,limit])
    
    ax2 = fig.add_subplot(212);
    fig = sm.graphics.tsa.plot_pacf(series, lags=limit, ax=ax2);
    plt.title('Partial Correlogram');
    plt.xticks(np.arange(0,limit+1,1))
    plt.xlim([-1,limit])



