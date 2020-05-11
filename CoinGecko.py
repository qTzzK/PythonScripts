import requests
import pandas as pd
from scipy import stats
import time
from datetime import date, timedelta
import json

from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
slack_token = '{hook}'
slack_alerts_hook = '{token}'
cryptos = ['bitcoin','ethereum']

def GetCoinPrices(crypto):
    df_90 = pd.DataFrame(cg.get_price(ids=crypto, vs_currencies='usd'))

    current_price = df_90[crypto].usd
    #daily_volume = df_90.volume_traded[0]

    previous_daily_price = GetCoinHistory(crypto, 0).market_data.current_price['usd']
    #previous_daily_volume = df_90.volume_traded[]

    price_30_days_ago =  GetCoinHistory(crypto, 30).market_data.current_price['usd']
    price_90_days_ago = GetCoinHistory(crypto, 90).market_data.current_price['usd']

    # calculate percentiles
    day_1_percentile = abs(current_price - previous_daily_price) / previous_daily_price * 100.0
    day_30_percentile = abs(current_price - price_30_days_ago) / price_30_days_ago * 100.0
    day_90_percentile = abs(current_price - price_90_days_ago) / price_90_days_ago * 100.0

    #format percentiles
    percentile_formatted1 = "{:.1%}".format(day_1_percentile/100)
    percentile_formatted30 = "{:.1%}".format(day_30_percentile/100)
    percentile_formatted90 = "{:.1%}".format(day_90_percentile/100)
    daily_price_formatted = '${:,.2f}'.format(current_price)

    MessageText = f'''{crypto} ({daily_price_formatted}) is {GetStatus(current_price, previous_daily_price)} {percentile_formatted1} from yesterdays closing price ({'${:,.2f}'.format(previous_daily_price)}).
    \n {crypto} is {GetStatus(current_price, price_30_days_ago)} {percentile_formatted30} in the last 30 days ({'${:,.2f}'.format(price_30_days_ago)}).
    \n {crypto} is {GetStatus(current_price, price_90_days_ago)} {percentile_formatted90} in the last 90 days ({'${:,.2f}'.format(price_90_days_ago)}).'''

    PushSlackMessage(MessageText)
    print(MessageText)

def PushSlackMessage(text):
    data = {'token': slack_token,
            'username': 'AlertBot',
            'text': text}
    # post message to crypto-alerts slack channel
    requests.post(url=slack_alerts_hook, data=json.dumps(data), headers={'Content-Type': 'application/json'})

def GetStatus(first_price, second_price):
    return "DOWN" if second_price > first_price else "UP" if second_price < first_price else "EQUAL"

#get history of coin from x days ago
def GetCoinHistory(crypto, days):
    dt = date.today() - timedelta(days)
    history = pd.DataFrame(cg.get_coin_history_by_id(crypto,dt.strftime('%d-%m-%Y')))
    return history

for crypto in cryptos:
    GetCoinPrices(crypto)
