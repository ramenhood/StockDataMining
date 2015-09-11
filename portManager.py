#!/usr/bin/env python

"""
Authored by: Jared Hancock
Last Update: May 2015
"""


# daily rets = sum ( stock.closep * % of portfolio ) for each stock in port


import datetime
from calcUtils import *
from stock import *
from graphStock import *

MONEY = '{:,.2f}'




# def getEvents():
#     fromfile = open("events.txt", 'r')
#     fileData = csv.reader(fromfile)
#     dates = []
#     symbols = []
#     closep = []
#     percRets = []
#     tradeProfit = []
#     grossp = []
#     pos = []
#
#     for line in fileData:
#         dates.append(mdates.datestr2num(line[0]))
#         symbols.append(line[1])
#         closep.append(float(line[2]))
#         percRets.append(float(line[3]))
#         tradeProfit.append(float(line[4]))
#         grossp.append(float(line[5]))
#         pos.append(line[6])
#         print line
#     fromfile.close()
#     return dates, symbols, closep, percRets, tradeProfit, grossp, pos

def logResults(stock, results):
    """
    :param results: list of calculated attributes of a stock
        ex: [totalProfit, avg_daily_rets, volatility, sharpe]
    """
    tofile = open("results.txt", 'a')
    tofile.write(str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))+'\n')
    lines = stock.symbol+'\n'
    lines += "Profit per share:"+str(results[0])+'\n'
    lines += "Gross Profit %"+str(results[1])+'\n'
    lines += "Average daily return:"+str(results[2])+'\n'
    lines += "Volatility:"+str(results[3])+'\n'
    lines += "Sharpe Ratio:"+str(results[4])+'\n'
    tofile.write(lines)
    tofile.write('#')

    tofile.close()


def logEvent(eventLine):
    tofile = open("events.txt", 'a')
    tofile.write(eventLine)
    tofile.close()



    # TODO: vol
    # TODO: tweak event criteria
def backTest(stock):
    """
    :param stock: Stock object
    """
    timeFrame = 20
    totalProfit = 0.0
    numTotalTrades = 0

    stock.date, stock.closep, stock.highp, stock.lowp, stock.openp, stock.vol = pullData(stock.symbol)

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

    i = 0
    for i in range(1, len(stock.closep)-1, 1):
        j = i+1
        k = i - timeFrame

        if position == 'hold':
            if 30 <= rsi[i] <= 70 and rsi[j] > 70 and stock.closep[j] >= minGainPrice:     # upper RSI bound was broken (overbought)
                if timeFrame < i and stock.closep[j] > topBand[k]:
                    print "**ALERT** Sell triggered for ", stock.symbol
                    print "Initial purchase price: $", MONEY.format(buyp)

                    sellp = stock.closep[j]
                    tradeProfit = sellp - buyp
                    stockProfit += tradeProfit
                    numTrades += 1
                    position = 'none'

                    eventLine = str(mdates.num2date(stock.date[j])) +','+ stock.symbol.upper() +','+ str(stock.closep[j]) + ',sell\n'
                    logEvent(eventLine)
                    print "Sold at $", MONEY.format(sellp), "per share."
                    print "Total profit per share from trade: $", MONEY.format(tradeProfit)
                    print
                    time.sleep(1)

        elif position == 'none':
            if 30 <= rsi[i] <= 70 and rsi[j] < 30:   # buy triggered, RSI lower bound broken (oversold)
                if timeFrame < i and stock.closep[j] < botBand[k]:
                    print "**ALERT** Buy triggered for ", stock.symbol, " at $", MONEY.format(stock.closep[j])

                    buyp = stock.closep[j]
                    holdings.append(buyp)
                    position = 'hold'
                    numTrades += 1

                    eventLine = str(mdates.num2date(stock.date[j])) +','+ stock.symbol.upper() +','+ str(stock.closep[j]) + ',buy\n'
                    logEvent(eventLine)
                    print
                    time.sleep(1)

    stock.price = stock.closep[-1]
    totalProfit += stockProfit  # profit for a single stock in the portfolio
    numTotalTrades += numTrades

    daily_rets = daily_returns(stock.closep)
    avg_daily_rets = np.mean(daily_rets)
    perc_daily_rets = percent_daily_returns(stock.closep)
    volatility = np.std(daily_rets)
    sharpe = avg_daily_rets / volatility * np.sqrt(len(stock.closep))




    # TODO: current holdings and value
    print "======= Backtest results for ", stock.symbol, " ======="
    # print "Currently Holding at $", MONEY.format(holdings[0])
    print stock.symbol, "Total Gross Profit per share: $", MONEY.format(totalProfit)
    print "Gross profit: %", "{0:.2f}".format(totalProfit/startp * 100)
    print "=========================================="

    print "Avg difference between closing price and VWAP: ", np.mean(stock.closep - vwap)
    print "Sharpe Ratio: ", sharpe

    graphStock(stock, 10, 50, rsi, vwap, events=1)

    return [totalProfit, avg_daily_rets, volatility, sharpe]





# TODO: getData for whole port, normalize stuff
def main():

    sym = raw_input("Enter a stock symbol to backtest: ")
    stock = Stock(sym.upper())
    results = backTest(stock)
    logResults(stock, results)


if __name__ == "__main__":
    main()



