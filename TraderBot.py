# imports
import importlib
import functionality as fn
import pause
import datetime

# algorithm
importlib.reload(fn)
print("algorithm start")
while True:
    if fn.getMarketStatus() != "open":
        pause.until(datetime.datetime.now().replace(hour=8, minute=31) + datetime.timedelta(days=1))
    else:
        try:
            sp500 = fn.currentSP500()
            accepted = []
            for equity in sp500:
                pause.seconds(1)
                if fn.trend(equity, 30) == "uptrend" and fn.trend(equity, 100) == "downtrend":
                    accepted.append(equity)
            # print("completed equity list")
            for equity in accepted:
                pause.seconds(1)
                change = fn.getPercentChange(equity)
                if fn.getStockBuyingPower() <= fn.getCurrentSymbolPrice(equity) and change != None and change > -2:
                    continue
                else:
                    fn.buyEquity(equity)
            # print("completed buy phase")
            while fn.getMarketStatus() == "open":
                positions = fn.getPositions()
                for i in positions:
                    change = fn.getPercentChange(i[0])
                    print(i[0], change)
                    if change != None and change <= -2:
                        fn.sellEquity(i[0], i[1])
                pause.minutes(15)
            print("completed sell phase, trading day complete")
            print(fn.getPositions())
        except:
            pause.until(datetime.datetime.now().replace(hour=8, minute=31) + datetime.timedelta(days=1))