import pandas as pd
import xlrd

filePath = r"C:\Users\keano\Desktop\BTC historical data.xlsx"
xl = pd.ExcelFile(filePath)
df = xl.parse('3D', skiprows=2)
buySignalPrice = 0
sellSignalPrice = 0;
pricesAtSignal = []
countFivePercentIncrease = 0
totalSignals = 0

def get_change(current, previous):
    if current == previous:
        return 0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return float('inf')

for index, row in df.iterrows():
    if(row['Sell Alert'] == 1):
        pricesAtSignal.append(("Sell Alert", row['close']))
    elif(row['Buy Alert'] == 1):
        pricesAtSignal.append(("Buy Alert", row['close']))
        
for (alert,price) in pricesAtSignal:
    totalSignals += 1
    if(alert == "Buy Alert"):
        if(buySignalPrice == 0):
            buySignalPrice = price
            print("Buy Signal Price: " + str(price))
    elif(sellSignalPrice == 0):
        sellSignalPrice = price
        print("Sell Signal Price: " + str(price))

    if(sellSignalPrice != 0 and buySignalPrice != 0):
        less = buySignalPrice > sellSignalPrice
        percentChange = round(get_change(buySignalPrice, sellSignalPrice),1)
        print("Percentage Change: " + ("-" if less else "+")  +  str(percentChange) + "%\n")
        buySignalPrice = 0
        sellSignalPrice = 0
        if(not less and percentChange > 5):
            countFivePercentIncrease += 1

print("\nBuy Signals followed by 5 percent increase: " + str(countFivePercentIncrease) + "/" + str(totalSignals) + "\n")

