import requests
import pandas as pd
from scipy import stats
import time

coin_api_key = '113F2850-04D9-4C82-A23A-37D0B69EE954'
slack_token = 'xoxb-1085245199701-1086847255443-72fh2uX7tdfyzRBr7soIuAww'
headers = {'X-CoinAPI-Key' : coin_api_key}
api_base_url = 'https://rest.coinapi.io/v1/'
cryptos = ['BTC']


def GetHistoricalPrices(crypto, days):
    uri = f'ohlcv/{crypto}/USD/latest?period_id=1DAY&limit={days}'
    return requests.get(api_base_url + uri, headers = headers).json()

def COINprices(crypto):
    # get historical prices (30 days)
    df_30 = pd.DataFrame(GetHistoricalPrices(crypto, days=30))

    #volume
    daily_volume = df_30.volume_traded[0]
    previous_daily_volume = df_30.volume_traded[1]
    #price
    daily_price = df_30.price_close[0]
    previous_daily_price = df_30.price_close[1]

    # get historical prices (90 days)
    df_90 = pd.DataFrame(GetHistoricalPrices(crypto, days=90))

    # calculate percentiles
    day_1_percentile = abs(daily_price - previous_daily_price) / previous_daily_price * 100.0
    day_30_percentile = stats.percentileofscore(df_30.price_close, daily_price)
    day_90_percentile = stats.percentileofscore(df_90.price_close, daily_price)

    #format percentiles
    percentile_formatted1 = "{:.1%}".format(day_1_percentile/100)
    percentile_formatted30 = "{:.1%}".format(day_30_percentile/100)
    percentile_formatted90 = "{:.1%}".format(day_90_percentile/100)

    status = "lower than" if previous_daily_price > daily_price else "higher than" if previous_daily_price < daily_price else "equal to"

    message = f"{crypto} ({'${:,.2f}'.format(daily_price)}) is {percentile_formatted1} {status} yesterdays closing price ({'${:,.2f}'.format(previous_daily_price)}),\n BTC is up {percentile_formatted30} in the last 30 days and {percentile_formatted90} in the last 90 days."
    SLACKmessage(message)
    print(message)

def SLACKmessage(text):
    slack_api_url = 'https://slack.com/api/chat.postMessage'
    data = {'token': slack_token,
            "channel": "C012JQUEC9H", "text": text}
    # post message to crypto-alerts slack channel
    requests.post(url = slack_api_url, data = data)

for crypto in cryptos:
    time.sleep(4)
    result = COINprices(crypto)
