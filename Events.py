__author__ = 'Jared'

import stock
import csv
import matplotlib.dates as mdates


"""
Container class to hold all events for a specific stock.
"""
class Events:
    def __init__(self, symbol="NKE"):
        self.symbol = symbol
        self.percRets = []
        self.vwap = []
        self.pos = []
        self.dates = []
        self.closep = []
