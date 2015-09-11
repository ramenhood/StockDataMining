#!/usr/bin/env python

"""
Authored by: Jared Hancock
Last Update: May 2015
"""

# matplotlib particulars credit to Harrison Kinsley


# TODO: calc RSI events inside the RSI function? instead of looping over the whole set again in main
# TODO: consider using py2exe or cython to create an executabe

''' Yahoo API notes:
    Data puled from >= 1 year and < 10 years will use a period of 14 (see: RSI). 10 years and higher, and the period
    will be 28.

    API date ranges:
        (n)d: days, using minute units in unix timestamps
        (n)m: months, using day as units
         <5y:  uses days as units
         >=5y: uses weeks as units

'''


import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.finance import candlestick
import matplotlib
import pylab
import csv
from calcUtils import *
matplotlib.rcParams.update({'font.size': 9})
from portManager import getEvents

def getEvents():
    fromfile = open("events.txt", 'r')
    fileData = csv.reader(fromfile)
    dates = []
    symbols = []
    closep = []
    percRets = []
    tradeProfit = []
    grossp = []
    pos = []

    for line in fileData:
        dates.append(mdates.datestr2num(line[0]))
        symbols.append(line[1])
        closep.append(float(line[2]))
        percRets.append(float(line[3]))
        tradeProfit.append(float(line[4]))
        grossp.append(float(line[5]))
        pos.append(line[6])

    return dates, symbols, closep, percRets, tradeProfit, grossp, pos


def graphStock(mystock, MA1, MA2, rsi=None, vwap=None, events=0):
    """
    :param mystock:
    :param MA1:
    :param MA2:
    :param rsi:
    :param vwap:
    :param events:
    :return:
    """
    stock = mystock.symbol
    date, closep, highp, lowp, openp, volume = mystock.date, mystock.closep, mystock.highp,\
                                               mystock.lowp, mystock.openp, mystock.vol

    x = 0
    y = len(date)
    dataList = []
    while x < y:
        appendLine = date[x],openp[x],closep[x],highp[x],lowp[x],volume[x]
        dataList.append(appendLine)
        x+=1

    Av1 = movingaverage(closep, MA1)
    Av2 = movingaverage(closep, MA2)

    # SP = 'starting point'
    SP = len(date[MA2-1:])  # this line ensures that we have enough data calculable from moving avgs to plot

    fig = plt.figure(facecolor='#000000', figsize=(16,9))

    ax1 = plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=4, axisbg='#000000')
    candlestick(ax1, dataList[-SP:], width=.003, colorup='#53c156', colordown='#ff1717')

    def standard_dev(tf,date,prices): # return an array of stdevs and correlating dates
        sd = []
        stdDate = []
        x = tf
        while x <= len(prices):
            array2consider = prices[x-tf:x]
            standev = array2consider.std()
            sd.append(standev)
            stdDate.append(date[x])
            x+=1
        return stdDate,sd

    def bollinger_bands(date, closep, mult, tFrame):
        bdate = []
        topBand = []
        botBand = []
        midBand = []
        x = tFrame

        while x < len(date):
            curSMA = movingaverage(closep[x-tFrame:x], tFrame)[-1]
            d, curStDev = standard_dev(tFrame, date, closep[0:tFrame])
            curStDev = curStDev[0]

            TB = curSMA + (curStDev * mult)
            BB = curSMA - (curStDev * mult)
            D = date[x]

            bdate.append(D)
            topBand.append(TB)
            botBand.append(BB)
            midBand.append(curSMA)

            x+=1

        return bdate, topBand, botBand, midBand

    # plot the bolllinger bands
    bb_date, topBand, botBand, midBand = bollinger_bands(date, closep, 2, 20)
    try:
        ax1.plot(bb_date[-SP:], topBand[-SP:], '#81BEF7', alpha = .7)
        ax1.plot(bb_date[-SP:], botBand[-SP:], '#81BEF7', alpha = .7)
        ax1.plot(bb_date[-SP:], midBand[-SP:], '#81BEF7', alpha = .7)

    except Exception, e:
        print str(e)

    # plot the SMA
    Label1 = str(MA1)+' SMA'
    Label2 = str(MA2)+' SMA'

    ax1.plot(date[-SP:],closep[-SP:],'#F7FE2E',label='Close', linewidth=1.3)
    if vwap != None:
        ax1.plot(date[-SP:],vwap[-SP:],'#F58031',label='VWAP',linewidth=0.8)
    # ax1.plot(date[-SP:],Av1[-SP:],'#e1edf9',label=Label1, linewidth=1.5)
    # ax1.plot(date[-SP:],Av2[-SP:],'#4ee6fd',label=Label2, linewidth=1.5)

    ax1.grid(True, color='w')
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.yaxis.label.set_color("w")
    ax1.spines['bottom'].set_color("#5998ff")
    ax1.spines['top'].set_color("#5998ff")
    ax1.spines['left'].set_color("#5998ff")
    ax1.spines['right'].set_color("#5998ff")
    ax1.tick_params(axis='y', colors='w')
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    ax1.tick_params(axis='x', colors='w')
    plt.ylabel('Volume and Price')


    # this is the legend for the moving averages
    maLeg = plt.legend(loc=9, ncol=2, prop={'size':7},
               fancybox=True, borderaxespad=0.)
    maLeg.get_frame().set_alpha(0.4)
    textEd = pylab.gca().get_legend().get_texts()
    pylab.setp(textEd[0:5], color = 'w')

    ax0 = plt.subplot2grid((6,4), (0,0), sharex=ax1, rowspan=1, colspan=4, axisbg='#07000d')

    rsiCol = '#c1f9f7'
    posCol = '#386d13'  # color when RSI < 30
    negCol = '#8f2020'  # color when RSI > 70

    ax0.plot(date[-SP:], rsi[-SP:], rsiCol, linewidth=1.5)
    ax0.axhline(70, color=negCol)
    ax0.axhline(30, color=posCol)
    ax0.fill_between(date[-SP:], rsi[-SP:], 70, where=(rsi[-SP:]>=70), facecolor=negCol, edgecolor=negCol, alpha=0.5)
    ax0.fill_between(date[-SP:], rsi[-SP:], 30, where=(rsi[-SP:]<=30), facecolor=posCol, edgecolor=posCol, alpha=0.5)
    ax0.set_yticks([30,70])
    ax0.yaxis.label.set_color("w")
    ax0.spines['bottom'].set_color("#5998ff")
    ax0.spines['top'].set_color("#5998ff")
    ax0.spines['left'].set_color("#5998ff")
    ax0.spines['right'].set_color("#5998ff")
    ax0.tick_params(axis='y', colors='w')
    ax0.tick_params(axis='x', colors='w')
    plt.ylabel('RSI')

    volumeMin = 0
    # volume plot
    ax1v = ax1.twinx()
    ax1v.fill_between(date[-SP:],volumeMin, volume[-SP:], facecolor='#00ffe8', alpha=.4)
    ax1v.axes.yaxis.set_ticklabels([])
    ax1v.grid(False)
    ax1v.set_ylim(0, 3*volume.max())
    ax1v.spines['bottom'].set_color("#5998ff")
    ax1v.spines['top'].set_color("#5998ff")
    ax1v.spines['left'].set_color("#5998ff")
    ax1v.spines['right'].set_color("#5998ff")
    ax1v.tick_params(axis='x', colors='w')
    ax1v.tick_params(axis='y', colors='w')


    ax2 = plt.subplot2grid((6,4), (5,0), sharex=ax1, rowspan=1, colspan=4, axisbg='#07000d')

    # MACD graph #
    fillcolor = '#00ffe8'
    nslow = 26
    nfast = 12
    nema = 9

    emaslow, emafast, macd = computeMACD(closep)

    ema9 = ExpMovingAverage(macd, nema)

    ax2.plot(date[-SP:], macd[-SP:], color='#4ee6fd', lw=2)
    ax2.plot(date[-SP:], ema9[-SP:],color='#e1edf9', lw=1)
    ax2.fill_between(date[-SP:], macd[-SP:]-ema9[-SP:], 0, alpha=0.5, facecolor=fillcolor, edgecolor = fillcolor)


    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax2.spines['bottom'].set_color("#5998ff")
    ax2.spines['top'].set_color("#5998ff")
    ax2.spines['left'].set_color("#5998ff")
    ax2.spines['right'].set_color("#5998ff")
    ax2.tick_params(axis='x', colors='w')
    ax2.tick_params(axis='y', colors='w')
    plt.ylabel('MACD', color='w')
    ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5, prune='upper'))


    for label in ax2.xaxis.get_ticklabels():
        label.set_rotation(45)

    plt.suptitle(stock.upper(),color='w')

    plt.setp(ax0.get_xticklabels(), visible=False)
    plt.setp(ax1.get_xticklabels(), visible=False)

    #plt.show()
    fig.savefig('bare.png',facecolor=fig.get_facecolor())
    # whatever value currently being graphed can go in to date[] and Av1[]

    e_dates, e_symbols, e_closep, e_perc_rets, e_profit, e_grossp, e_pos = getEvents()
    i = 0
    annX = 0.2
    annY = 0.90
    if events > 0 and len(e_dates) > 0:
        # lastSym = e_symbols[0]
        for i in range(0, len(e_dates),1):
            if e_symbols[i] == stock:
                ax1.annotate(e_pos[i], (e_dates[i], e_closep[i]), xytext = (annX, annY), textcoords='axes fraction',
                             arrowprops=dict(facecolor='white',shrink=0.05), fontsize=9, color='w',
                             horizontalalignment='right', verticalalignment='bottom')
                annX += 0.05
            # else:
            #     annX += 0.05
            #     ax1.annotate(e_symbols[i], (e_dates[i], e_closep[i]), xytext = (annX, annY), textcoords='axes fraction',
            #                  arrowprops=dict(facecolor='white',shrink=0.03), fontsize=7, color='w',
            #                  horizontalalignment='right', verticalalignment='bottom')
            # lastSym = e_symbols[i]

        '''ax1.annotate('EVENT',(date[510],Av1[510]),
            xytext=(0.8, 0.9), textcoords='axes fraction',
            arrowprops=dict(facecolor='white', shrink=0.05),
            fontsize=8, color = 'w',
            horizontalalignment='right', verticalalignment='bottom')'''

    plt.subplots_adjust(left=.09, bottom=.14, right=.94, top=.95, wspace=.20, hspace=0)
    plt.show()

    fig.savefig('events.png',facecolor=fig.get_facecolor())


