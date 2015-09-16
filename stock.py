#!/usr/bin/env python

"""
Authored by: Jared Hancock
Last Update: May 2015
"""

import urllib2
import matplotlib.dates as mdates
import time
import datetime
import numpy as np
import csv


class Stock:
    def __init__(self, symbol):
        self.symbol = symbol
        self.price = 0.0
        self.closep = []
        self.date = []
        self.vol = []
        self.highp = []
        self.lowp = []
        self.openp = []


class Event:
    def __init__(self):
        self.symbol = None
        self.percRets = []
        self.vwap = []
        self.pos = []
        self.dates = []
        self.closep = []


'''

'''
def getEvents():
    fromfile = open("events.txt", 'r')
    fileData = csv.reader(fromfile)
    dates = []
    symbols = []
    closep = []
    percRets = []
    e_vwap = []
    pos = []

    for line in fileData:
        dates.append(mdates.datestr2num(line[0]))
        symbols.append(line[1])
        closep.append(float(line[2]))
        percRets.append(float(line[3]))
        e_vwap.append(line[4])
        pos.append(line[5])

    events = []

    e = Event()
    e.symbol = symbols[0]

    for i in range(0, len(closep)):
        if e.symbol == symbols[i]:
            e.closep.append(closep[i])
            e.dates.append(dates[i])
            e.percRets.append(percRets[i])
            e.vwap.append(e_vwap[i])
            e.pos.append(pos[i])




    return events #dates, symbols, closep, percRets, e_vwap, pos

def pullIntraDay(stock):
    '''
        Use this to dynamically pull a stock:
    '''
    try:
        print 'Currently Pulling',stock
        print str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')), '\n'
        #Keep in mind this is close high low open data from Yahoo
        urlToVisit = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range=1d/csv'
        stockFile = []
        try:
            sourceCode = urllib2.urlopen(urlToVisit).read()
            splitSource = sourceCode.split('\n')
            for eachLine in splitSource:
                splitLine = eachLine.split(',')

                fixMe = splitLine[0]

                if len(splitLine)==6:
                    if 'values' not in eachLine:
                        fixed = eachLine.replace(fixMe, str(datetime.datetime.fromtimestamp(int(fixMe)).strftime('%Y-%m-%d %H:%M:%S')))
                        stockFile.append(fixed)
        except Exception, e:
            print str(e), 'failed to organize pulled data.'
    except Exception,e:
        print str(e), 'failed to pull pricing data'
    date, closep, highp, lowp, openp, volume = np.loadtxt(stockFile,delimiter=',', unpack=True,converters={ 0: mdates.strpdate2num('%Y-%m-%d %H:%M:%S')})
    return date, closep, highp, lowp, openp, volume



def pullData(stock, span="1y"):
    try:
        print 'Getting data for',stock
        print str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')), '\n'
        #Keep in mind this is close high low open data from Yahoo
        urlToVisit = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range='+span+'/csv'
        stockFile = []
        try:
            sourceCode = urllib2.urlopen(urlToVisit).read()
            splitSource = sourceCode.split('\n')
            for eachLine in splitSource:
                splitLine = eachLine.split(',')
                if len(splitLine)==6:
                    if 'values' not in eachLine:
                        stockFile.append(eachLine)
        except Exception, e:
            print str(e), 'failed to organize pulled data.'
    except Exception,e:
        print str(e), 'failed to pull pricing data'

    date, closep, highp, lowp, openp, volume = np.loadtxt(stockFile,delimiter=',', unpack=True,
                                                             converters={ 0: mdates.strpdate2num('%Y%m%d')})

    return date, closep, highp, lowp, openp, volume