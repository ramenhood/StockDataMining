#!/usr/bin/env python

"""
Authored by: Jared Hancock
Last Update: May 2015
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib


matplotlib.rcParams.update({'font.size': 9})
from stock import pullData
from graphStock import getEvents
from calcUtils import *

def plotEvents(span='1y'):
    dates, symbols, closep, percRets, profit, grossp, pos = getEvents()

    if len(dates) <= 0:
        return "No results to display\n"

    fig = plt.figure(figsize=(10,8))

    buyx = []
    buyy = []
    sellx = []
    selly = []
    lossx = []
    lossy = []

    ax1 = plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=4, axisbg='#000000')
    ax1.grid(True, color='w')

    spydate, spyp, h, l, o, v = pullData("SPY", span)
    spyRets = percent_daily_returns(spyp)
    ax1.plot(spydate[:-1], spyRets, '#81BEF7', label="SP500", alpha =0.5)

    # annX = 0.2
    # annY = 0.90
    for i in range(0, len(dates), 1):
        if pos[i] == 'buy':
            buyx.append(dates[i])
            buyy.append(grossp[i])
        elif pos[i] == 'sell':
            if grossp[i] > 0:
                sellx.append(dates[i])
                selly.append(grossp[i])
            else:
                lossx.append(dates[i])
                lossy.append(grossp[i])
        # ax1.annotate(symbols[i], dates[i], grossp[i], xytext=0.9,textcoords='axes fraction',
        #              arrowprops=dict(facecolor='white',shrink=0.05), fontsize=9, color='w',
        #                      horizontalalignment='right', verticalalignment='bottom')
        # annX += 0.1


    ax1.scatter(buyx, buyy, color='#A9F5F2', label="Bought")
    ax1.scatter(sellx, selly, color='#40FF00', label="Sold:Profit")
    ax1.scatter(lossx,lossy, color='#FF0000', label="Sold:Loss")



    plt.title("Logged Events")
    plt.ylabel("Gross Profit %")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
    plt.xlabel("Date")


    plt.tight_layout()
    plt.legend()
    plt.show()
    fig.savefig('events.png',facecolor=fig.get_facecolor())



