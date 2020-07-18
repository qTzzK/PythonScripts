import requests
import json
import csv

pathToCsv = r"C:\Users\keano\Desktop\bitmex.csv"

def createCSV():
    data = {'binSize': '1d',
           'symbol': 'XBTUSD',
           'partial': False,
           'reverse' : True,
           'startTime' : 2018,
           'EndTime':2020, 
           'count':1000}
    
    with open(pathToCsv,'w', newline='') as csvFile:
        response = requests.get(url="https://www.bitmex.com/api/v1/trade/bucketed", data=json.dumps(data), headers={'Content-Type': 'application/json'}).json();
        header = ['timestamp', 'symbol', 'open','high','low','close','trades','volume','vwap','lastSize', 'turnover', 'homeNotional', 'foreignNotional']
        writer=csv.DictWriter(csvFile, fieldnames = header)
        writer.writeheader()
        for i in response:
            writer.writerow(i)
     
createCSV()