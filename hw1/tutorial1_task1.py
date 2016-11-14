'''
(c) 2011, 2012 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see
http://wiki.quantsoftware.org/index.php?title=QSTK_License
for license details.

Created on January, 24, 2013

@author: Sourabh Bajaj
@contact: sourabhbajaj@gatech.edu
@summary: Example tutorial code.
'''

# QSTK Imports
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import time
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

print "Pandas Version", pd.__version__

def formatDate(dateStr):
    dateStr = time.strptime(dateStr, '%B %d, %Y')
    y, m, d = dateStr[0:3]
    return dt.datetime(y, m, d)

def simulate(startdate, enddate, symbols, allocation):
    dt_start = formatDate(startdate)
    dt_end = formatDate(enddate)
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

    c_dataobj = da.DataAccess('Yahoo')
    ls_keys = ['close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    close_price = d_data['close'].values    
    close_normalized_price = close_price / close_price[0, :]

    allocation = np.array(allocation)
    close_normalized_price_alloc = np.multiply(close_normalized_price, allocation)
    ret = np.cumsum(close_normalized_price_alloc, axis=1)[:, len(symbols) - 1]    

    tsu.returnize0(ret)

    std = np.std(ret)

    cum_ret = np.sum(ret) + 1

    sharpe_ratio = tsu.get_sharpe_ratio(ret)

    daily_ret = np.mean(ret)

    return std, daily_ret, sharpe_ratio, cum_ret

def portfolio_optimizer(startdate, enddate, symbols):
    max_sharpe = -1
    max_alloc = [0.0, 0.0, 0.0, 0.0]
    for i in range(0, 11):
        for j in range(0, 11-i):
            for k in range(0, 11-i-j):
                for l in range(0, 11-i-j-k):
                    if (i + j + l + k) == 10:
                        alloc = [float(i)/10, float(j)/10, float(k)/10, float(l)/10]
                        vol, daily_ret, sharpe, cum_ret = simulate(startdate, enddate, symbols, alloc)
                        if sharpe > max_sharpe:
                            max_sharpe = sharpe
                            max_alloc = alloc
    print(max_sharpe)                        
    print(max_alloc)
    return max_alloc

def test1():
    # List of symbols
    symbols = ['AXP', 'HPQ', 'IBM', 'HNZ']
    startdate = 'January 1, 2010'
    enddate = 'December 31, 2010'
    simulate(startdate, enddate, symbols, [0.0, 0.0, 0.0, 1.0])

def test2():
    # List of symbols
    symbols = ['AAPL', 'GLD', 'GOOG', 'XOM']
    startdate = 'January 1, 2011'
    enddate = 'December 31, 2011'
    simulate(startdate, enddate, symbols, [0.4, 0.4, 0.0, 0.2]) 

def test3():
    # List of symbols
    symbols = ['AAPL', 'GLD', 'GOOG', 'XOM']
    startdate = 'January 1, 2011'
    enddate = 'December 31, 2011'
    portfolio_optimizer(startdate, enddate, symbols)    

def main():
    ''' Main Function'''

    test3()

if __name__ == '__main__':
    main()
