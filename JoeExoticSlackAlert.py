import requests
import pandas as pd
from scipy import stats
import time

coin_api_key = '113F2850-04D9-4C82-A23A-37D0B69EE954'
slack_token = 'xoxb-1085245199701-1086847255443-72fh2uX7tdfyzRBr7soIuAww'
headers = {'X-CoinAPI-Key' : coin_api_key}
api_base_url = 'https://rest.coinapi.io/v1/'
cryptos = ['BTC']

def GetStatus(first_price, second_price):
    return "DOWN" if second_price > first_price else "UP" if second_price < first_price else "EQUAL"

def GetCoinPrices(crypto):
    priceHistoryUri = f'ohlcv/{crypto}/USD/latest?period_id=1DAY&limit=90'
    # get historical prices (90 days)
    response = requests.get(api_base_url + priceHistoryUri, headers = headers).json()
    df_90 = pd.DataFrame(response)

    daily_price = df_90.price_close[0]
    daily_volume = df_90.volume_traded[0]

    previous_daily_price = df_90.price_close[1]
    previous_daily_volume = df_90.volume_traded[1]

    price_30_days_ago = df_90.price_close[29]
    price_90_days_ago = df_90.price_close[89]

    # calculate percentiles
    day_1_percentile = abs(daily_price - previous_daily_price) / previous_daily_price * 100.0
    day_30_percentile = abs(daily_price - price_30_days_ago) / price_30_days_ago * 100.0
    day_90_percentile = abs(daily_price - price_90_days_ago) / price_90_days_ago * 100.0

    #format percentiles
    percentile_formatted1 = "{:.1%}".format(day_1_percentile/100)
    percentile_formatted30 = "{:.1%}".format(day_30_percentile/100)
    percentile_formatted90 = "{:.1%}".format(day_90_percentile/100)
    daily_price_formatted = '${:,.2f}'.format(daily_price)

    message = f'''{crypto} ({daily_price_formatted}) is {GetStatus(daily_price, previous_daily_price)} {percentile_formatted1} from yesterdays closing price ({'${:,.2f}'.format(previous_daily_price)}).
    \n {GetStatus(daily_price, price_30_days_ago)} {percentile_formatted30} in the last 30 days ({'${:,.2f}'.format(price_30_days_ago)}).
    \n {GetStatus(daily_price, price_90_days_ago)} {percentile_formatted90} in the last 90 days ({'${:,.2f}'.format(price_90_days_ago)}).'''

    PushSlackMessage(message)
    print(message)

def PushSlackMessage(text):
    slack_api_url = 'https://slack.com/api/chat.postMessage'
    data = {'token': slack_token,
            "channel": "C012JQUEC9H", "text": text}
    # post message to crypto-alerts slack channel
    requests.post(url = slack_api_url, data = data)

for crypto in cryptos:
    GetCoinPrices(crypto)
