import pandas as pd

filePath = r"C:\Users\keano\Desktop\BTC historical data.xlsx"
xl = pd.ExcelFile(filePath)
df = xl.parse('3D', skiprows=2)
buySignalPrice = 0
sellSignalPrice = 0;
pricesAtSignal = []
percentChange = 5
countPercentChange = 0
countComparisons = 0

def GetPercentageChange(current, previous):
    if current == previous:
        return 0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return float('inf')

#populate array with buy/sell signals and their close prices
for index, row in df.iterrows():
    if(row['Sell Alert'] == 1):
        pricesAtSignal.append(("Sell Alert", row['close']))
    elif(row['Buy Alert'] == 1):
        pricesAtSignal.append(("Buy Alert", row['close']))

def CalculatePercentageChange(sellToBuy):
    global sellSignalPrice
    global buySignalPrice
    global countPercentChange
    global countComparisons
    if(sellSignalPrice != 0 and buySignalPrice != 0):
        countComparisons += 1
        result = round(GetPercentageChange(buySignalPrice, sellSignalPrice),1) if sellToBuy else round(GetPercentageChange(sellSignalPrice, buySignalPrice),1)
        less = sellSignalPrice > buySignalPrice if sellToBuy else buySignalPrice > sellSignalPrice
        print("Percentage Change: " + ("-" if less else "+")  +  str(result) + "%\n")     
        if(sellToBuy and less and result > percentChange or not sellToBuy and not less and result > percentChange):
            countPercentChange += 1
        buySignalPrice = 0
        sellSignalPrice = 0
        return result;

#buy to sell
for (alert,price) in pricesAtSignal:
        if(alert == "Buy Alert"):
            if(buySignalPrice == 0):
                buySignalPrice = price
                print("Buy Signal Price: " + str(price))
        elif(sellSignalPrice == 0):
            sellSignalPrice = price
            print("Sell Signal Price: " + str(price))
        CalculatePercentageChange(False)
print("\nBuy Signals followed by "+str(percentChange)+" percent increase: " + str(countPercentChange) + "/" + str(countComparisons) + "\n")

countPercentChange = 0           
countComparisons = 0
buySignalPrice = 0
sellSignalPrice = 0

#sell to buy
for (alert,price) in pricesAtSignal:
        if(alert == "Buy Alert"):
            if(sellSignalPrice != 0):
                buySignalPrice = price
                print("Buy Signal Price: " + str(price))
        elif(buySignalPrice == 0):
            sellSignalPrice = price
            print("Sell Signal Price: " + str(price))
        CalculatePercentageChange(True)
print("\nSell Signals followed by "+str(percentChange)+" percent decrease: " + str(countPercentChange) + "/" + str(countComparisons) + "\n")

