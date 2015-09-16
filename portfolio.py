#!/usr/bin/env python
__author__ = 'Jared'

import pandas as pd
from stock import Stock
import csv
import matplotlib.dates as mdates

"""
Class containing instances of Stocks.
NOTE: move toward using methods that explicitly use the Stock class. Other functionality will be deprecated
"""
class Portfolio:
    def __init__(self):
        self.stocks = []    # deprecated array
        self.myStocks =  [] # array of Stock objects
        self.cash = 0.0

    def calcStocksVal(self):
        stocksValue = 0
        for s in self.stocks:
            stocksValue += s.lastPrice * s.volume
        return stocksValue

    def calcTotalVal(self):
        totalValue = 0
        for s in self.stocks:
            totalValue += s.lastPrice * s.volume
        return totalValue + self.cash

    def addStock(self, stock):
        self.myStocks.append(stock)



'''
Scan through a file possibly containing events from multiple stocks
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

    return dates, symbols, closep, percRets, e_vwap, pos