__author__ = 'Jared'

import numpy as np
import pandas as pd


'''====================================================================================================================
Relative Strength Index (RSI): average gain over the average loss ; RSI is a reliable way to track momentum.
        When a security's price goes above 70, it could be considered to be overbought, which suggests an opportunity
        to sell. Likewise, if the price dips below 30, it could be considered underbought, suggesting an opportunity
        to buy.
    Params: current stock price;
            n = time period, default set to 14. 14 is typical when measuring RSI;
'''
def rsiFunc(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed>=0].sum()/n
    down = -seed[seed<0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1.+rs)

    for i in range(n, len(prices)):
        delta = deltas[i-1] # cause the diff is 1 shorter

        if delta>0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n

        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)

    return rsi


'''==================================================================================================================
Simple Moving Average(MA1 or SMA): Calculates the average price over a specified window of time.
        Good for tracking short term drops/spikes in stock price
    Params: values - data to average;
            window - time frame from which to calculate the averages;
'''
def movingaverage(values,window):
    weigths = np.repeat(1.0, window)/window
    smas = np.convolve(values, weigths, 'valid')
    return smas # as a numpy array


'''==================================================================================================================
Exponential Moving Average(EMA): Similar to SMA, but it weights recent data more heavily. Simply speaking, the EMA
    will almost always outperform the SMA.
    Params: values - data to average;
            window - time frame from which to calculate the averages;
'''
def ExpMovingAverage(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a =  np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a


'''==================================================================================================================
Moving Average Convergence Divergence (MACD): Follows trends AND momentum using a fast and slow EMA
    ~ MACD line = 12 EMA - 26 EMA
    ~ Signal line = 9 EMA of the MACD line
    ~ MACD histogram = MACD line - Signal Line

    Params:
    Return Value: emaslow, emafast, and macd which are all len(x) arrays
'''
def computeMACD(x, slow=26, fast=12):
    emaslow = ExpMovingAverage(x, slow)
    emafast = ExpMovingAverage(x, fast)
    return emaslow, emafast, emafast - emaslow


'''==================================================================================================================
standard_deviation: coputes the stdev of an array of prices over a specified time frame
    Params:
        - tf: time frame
        - prices: closing prices of a given security
'''
def standard_deviation(tf,date,prices):
    sd = []
    sddate = []
    x = tf
   ######
    while x <= len(prices):
        array2consider = prices[x-tf:x]
        standev = array2consider.std()
        sd.append(standev)
        sddate.append(date[x])
        x+=1
    return sddate,sd



'''==================================================================================================================
bollinger_bands: measures volatility
    Params:
        ~ mult: multiplier, usually 2
        ~ tff: time frame, typically 20 is used.
    the middleband is the SMA of the price

'''
def bollingerBands(date, closep, mult, tff):
    bdate = []
    topBand = []
    botBand = []
    midBand = []

    x = tff

    while x < len(date):
        curSMA = movingaverage(closep[x-tff:x], tff)[-1]
        d, curSD = standard_deviation(tff, date, closep[0:tff])

        curSD = curSD[0]

        TB = curSMA + (curSD * mult)
        BB = curSMA - (curSD * mult)
        D = date[x]

        bdate.append(D)
        topBand.append(TB)
        botBand.append(BB)
        midBand.append(curSMA)

        x+=1

    return bdate, topBand, botBand, midBand

'''==================================================================================================================
'''
def calc_vwap(date, vol, highp, lowp):

    tmp1 = np.zeros_like(vol)
    tmp2 = np.zeros_like(vol)
    for i in range(0, len(vol)):
        tmp1[i] = tmp1[i-1] + vol[i] * (highp[i] + lowp[i]) / 2
        tmp2[i] = tmp2[i-1] + vol[i]
    return tmp1/tmp2

def daily_returns(prices):
    return np.diff(prices)

def percent_daily_returns(prices):
    return np.diff(prices)/ prices[:-1] * 100