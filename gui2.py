#!/usr/bin/env python

"""
Authored: Jared Hancock
Last Update: May 2015
"""

"""
    Known bugs: Consecutive buys will yield inaccurate results
"""



import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation

import Tkinter as tk
from ScrolledText import *
import ttk
from calcUtils import *
from stock import *
from graphStock import graphStock
from portManager import logResults, logEvent
from chartEvents import plotEvents

LARGE_FONT = ("Consolas", 16)
MONEY = '{:,.2f}'



def display_sell(stock, buyp, sellp):
    print "\n**ALERT** Sell triggered for ", stock.symbol
    print "Initial purchase price: $", MONEY.format(buyp)
    print "Sold at $", MONEY.format(sellp), "per share."
    print "Total profit per share from trade: $", MONEY.format(sellp-buyp)
    print
    text.insert(tk.END, "**ALERT** Sell triggered for ")
    text.insert(tk.END, stock.symbol)
    text.insert(tk.END, "\nInitial purchase price of $")
    text.insert(tk.END, MONEY.format(buyp))
    text.insert(tk.END, "\nSold at $")
    text.insert(tk.END, MONEY.format(sellp))
    text.insert(tk.END, " per share.\n")
    text.insert(tk.END, "Total profit per share from this trade: $")
    text.insert(tk.END, MONEY.format(sellp-buyp))
    text.insert(tk.END, "\n")
    text.pack()


def display_buy(stock, buyp):
    print "**ALERT** Buy triggered for ", stock.symbol, " at $", MONEY.format(buyp)
    print
    text.insert(tk.END, "\n**ALERT** Buy triggered for ")
    text.insert(tk.END, stock.symbol)
    text.insert(tk.END, "at $")
    text.insert(tk.END, MONEY.format(buyp))
    text.insert(tk.END, " per share.\n")
    text.insert(tk.END, "\n")
    text.pack()

def backTest(stock, span="1y"):
    """
    :param stock: Stock object
    """
    timeFrame = 20
    totalProfit = 0.0
    numTotalTrades = 0

    stock.date, stock.closep, stock.highp, stock.lowp, stock.openp, stock.vol = pullData(stock.symbol, span)

    position = 'hold'
    startp = stock.closep[0]
    buyp = stock.closep[0]
    holdings = []
    sellp = 0.0
    minGainPrice = buyp * .002 + buyp    # only sell if we make 2%
    tradeProfit = 0.0
    stockProfit = 0.0
    numTrades = 0

    rsi = rsiFunc(stock.closep)
    toss, topBand, botBand, midBand = bollingerBands(stock.date, stock.closep, 2, timeFrame)
    vwap = calc_vwap(stock.date, stock.vol, stock.highp, stock.lowp)
    perc_daily_rets = percent_daily_returns(stock.closep)

    i = 0
    for i in range(1, len(stock.closep)-1, 1):
        j = i+1
        k = i - timeFrame

        if position == 'hold':
            if 30 <= rsi[i] <= 70 and rsi[j] > 70 and stock.closep[j] >= minGainPrice:     # upper RSI bound was broken (overbought)
                if (timeFrame < i and stock.closep[j] > topBand[k]) or (stock.closep[j] > vwap[j]):
                    sellp = stock.closep[j]
                    tradeProfit = sellp - buyp
                    grossp = tradeProfit / buyp * 100
                    stockProfit += tradeProfit
                    numTrades += 1
                    position = 'none'

                    display_sell(stock, buyp, sellp)
                    eventLine = str(mdates.num2date(stock.date[j])) +','+ stock.symbol.upper() +','+ \
                                str(stock.closep[j]) +','+ str(perc_daily_rets[i]) +','+ str(tradeProfit) +','+\
                                str(grossp) + ',sell\n'
                    logEvent(eventLine)
                    # time.sleep(1)

        elif position == 'none':
            if 30 <= rsi[i] <= 70 and rsi[j] < 30:   # buy triggered, RSI lower bound broken (oversold)
                if (timeFrame < i and stock.closep[j] < botBand[k]) or (stock.closep[j] < vwap[j]):
                    buyp = stock.closep[j]
                    position = 'hold'
                    numTrades += 1

                    display_buy(stock, buyp)
                    eventLine = str(mdates.num2date(stock.date[j])) +','+ stock.symbol.upper() +','+ \
                                str(stock.closep[j]) +','+ str(perc_daily_rets[i]) +','+ str(0) +','+ str(0) +',buy\n'
                    logEvent(eventLine)
                    # time.sleep(1)

    totalProfit += stockProfit
    numTotalTrades += numTrades
    currentPrice = stock.closep[-1]
    daily_rets = daily_returns(stock.closep)
    avg_daily_rets = np.mean(daily_rets)
    perc_daily_rets = percent_daily_returns(stock.closep)
    grossProf = totalProfit/startp * 100
    volatility = np.std(daily_rets)
    sharpe = avg_daily_rets / volatility * np.sqrt(len(stock.closep))

    print "======= Backtest results for ", stock.symbol, " ======="
    print stock.symbol, "Total Gross Profit per share: $", MONEY.format(totalProfit)
    print "Gross profit: %", "{0:.2f}".format(totalProfit/startp * 100)
    if position == 'hold':
        print "     Currently holding from $", MONEY.format(buyp)
        print "     Most recent price: $", MONEY.format(currentPrice)
        print "     Percent return on current holding: %", "{0:.2f}".format((currentPrice-buyp)/buyp * 100)
    print "=========================================="
    print "Avg difference between closing price and VWAP: ", "{0:.2f}".format(np.mean(stock.closep - vwap))
    print "Sharpe Ratio: ", "{0:.2f}".format(sharpe)

    text.insert(tk.END, "\n\n=========================== ")
    text.insert(tk.END, stock.symbol)
    text.insert(tk.END, " ===========================\n\n")
    text.insert(tk.END, "Back-test complete, here are the results: \n")
    text.insert(tk.END, "Total Gross Profit per share: $")
    text.insert(tk.END, MONEY.format(totalProfit))
    text.insert(tk.END, "\nPercent Gross Profit: %")
    text.insert(tk.END, ('{0:.2f}'.format(totalProfit/startp * 100)))
    if position == 'hold':
        text.insert(tk.END, "\n    Currently holding at $")
        text.insert(tk.END, MONEY.format(buyp))
        text.insert(tk.END, " per share. \n")
        text.insert(tk.END, "    Most recent price: $")
        text.insert(tk.END, MONEY.format(currentPrice))
        text.insert(tk.END, "\n    Return on current equity: %")
        text.insert(tk.END, "{0:.2f}".format((currentPrice-buyp)/buyp * 100))
        text.pack()
    text.insert(tk.END, "\nAverage difference between closing price and VWAP: ")
    text.insert(tk.END, "{0:.2f}".format(np.mean(stock.closep - vwap)))
    text.insert(tk.END, "\nSharpe Ratio: ")
    text.insert(tk.END, "{0:.2f}".format(sharpe))
    text.insert(tk.END, "\n==============================================================\n\n")
    text.pack()

    graphStock(stock, 10, 50, rsi, vwap, events=1)

    return [totalProfit, grossProf, avg_daily_rets, volatility, sharpe]


class BackTestApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "BackTest App")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)    # fill in limits I set, expand if necessary
        container.grid_rowconfigure(0, weight=1)    # weight is like priority
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # for F in (StartPage):
        #     frame = F(container, self)
        #     self.frames[F] = frame
        #     frame.grid(row=0, column=0, sticky="nsew")
        frame = StartPage(container, self)
        self.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Back Tester", font=LARGE_FONT)
        label.pack(side="top", pady=10, padx=10)
        self.create_widgets(parent, controller)

    def create_widgets(self, parent, controller):

        self.info = tk.Label(self, text="Enter a stock ticker")
        self.info.pack()

        self.e = ttk.Entry(self)    # entry form for stock symbol
        self.e.pack()

        self.info2 = tk.Label(self, text="Enter timespan (6m, 1y, 3y)")
        self.info2.pack()

        self.span = tk.Entry(self)
        self.span.pack(side=tk.TOP)
        self.span.focus_set()

        self.b = ttk.Button(self, text='Submit', command=lambda: self.get_input())
        # self.b.grid(row=3, column=1, sticky=tk.N)
        self.b.pack(side=tk.TOP)

        self.info3 = tk.Label(self, text="Results")
        self.info3.pack(side=tk.LEFT)

        global text
        text = ScrolledText(self, font=("Consolas",10), padx=10, pady=10)
        text.insert(tk.INSERT, "\n")
        text.pack(side=tk.BOTTOM, expand=True)

        self.b1 = tk.Button(self, text='Event Plot', command=lambda: self.chart_events())
        self.b1.pack(side=tk.RIGHT)

    def get_input(self):
        sym = self.e.get()
        stock = Stock(sym.upper())
        span = self.span.get()
        if span == "":
            results = backTest(stock)
        else:
            results = backTest(stock, span)
        logResults(stock, results)

    def chart_events(self):
        span = self.span.get()

        result = plotEvents(span)
        if type(result) == str:
            text.insert(tk.END, result).pack()

result = None
app = BackTestApp()
app.geometry("1000x600")

app.mainloop()


