#!/usr/bin/env python

# chartstocks.py

# http://chartapi.finance.yahoo.com/instrument/1.0/'+stocksymbol+'/chartdata;type=quote;range=1y/csv

import urllib2
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.finance import candlestick
import matplotlib
import pylab


stockList = 'NKE', 'COST', 'TD', 'THC', 'INTC', 'UA', 'SLB'



def graphData(stock):
    try:
        stockFile = stock+'.txt'

        datefunc = lambda x: mdates.num2date(x)

        date, closep, highp, lowp, openp, volume = np.loadtxt(stockFile, delimiter=',', unpack=True,
                                                              converters={ 0: datefunc})

        ### use this for non-unix time stamps
        # date, closep, highp, lowp, openp, volume = np.loadtxt(stockFile, delimiter=',', unpack=True,
        #                                                       converters={ 0: mdates.strpdate2num('%Y%m%d')})

        x = 0
        y = len(date)

        dataList = []
        while x < y:
            lineToAppend = date[x], openp[x], closep[x], highp[x], lowp[x], volume[x]
            dataList.append(lineToAppend)
            x+=1

        fig = plt.figure()
        axis1 = plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=4, axisbg='#07000d')
        #axis1.plot(date, openp)
        #axis1.plot(date, highp)
        #axis1.plot(date, lowp)
        axis1.plot(date, closep)

        plt.ylabel('Stock Price')
        axis1.grid(True)

        axis2 = plt.subplot2grid((6,4), (0,0), sharex=ax1, rowspan=1, colspan=4, axisbg='#07000d')
        axis2.bar(date, volume)
        plt.ylabel('Volume')
        axis2.grid(True)

        axis1.xaxis.set_major_locator(mticker.MaxNLocator(10))
        axis1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        for label in axis1.xaxis.get_ticklabels():
            label.set_rotation(45)

        plt.subplots_adjust(left=.10, bottom=.19, right=.93, top=.95, wspace=.20, hspace=.07)

        plt.xlabel('Date')
        plt.ylabel('Stock Price')
        plt.suptitle(stock+' Stock Price')
        plt.show()

    except Exception, e:
        print "main loop", str(e)

for stock in stockList:
    graphData(stock)
    #time.sleep(100)
