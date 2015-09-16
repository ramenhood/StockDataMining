#!/usr/bin/env python
__author__ = 'Jared'

"""
Authored by: Jared Hancock
Last Update: September 2015
"""

import urllib2
import matplotlib.dates as mdates
import time
import datetime
import numpy as np
import csv
import Events


"""
Class for a specific stock (i.e. "NKE")
Contains arrays of data and an Events object that contains data about when an event was triggered
"""
class Stock:
    def __init__(self, symbol="NKE"):
        self.symbol = symbol
        self.price = 0.0
        self.closep = []
        self.date = []
        self.vol = []
        self.highp = []
        self.lowp = []
        self.openp = []
        self.events = Events(symbol)

    def getEventsForStock(self):
        fromfile = open("events.txt", 'r')
        fileData = csv.reader(fromfile)
        for line in fileData:
            if self.symbol == line[1]:
                self.events.closepappend(float(line[2]))
                self.events.percRets.append(float(line[3]))
                self.events.vwap.append(float(line[4]))
                self.events.pos.append(line[5])

        return self.events



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