import requests
import json
import datetime
import pandas as pd

base_url = "https://sandbox.tradier.com/v1/"
account_id = #id
access_token = #token

def jsonGetStatus():
    response = requests.get(base_url + 'accounts/' + account_id + '/balances',
        params={},
        headers={'Authorization': 'Bearer ' + access_token, 'Accept': 'application/json'}
    )
    return response.json()

def getNetWorth():
    return jsonGetStatus()['balances']['total_equity']

def getStockBuyingPower():
    return jsonGetStatus()['balances']['total_cash']

def jsonGetSymbolData(symbol):
    response = requests.get(base_url + 'markets/quotes',
        params={'symbols': symbol},
        headers={'Authorization': 'Bearer ' + access_token, 'Accept': 'application/json'}
    )
    return response.json()

def jsonGetSymbolHistory(symbol, days):
    now = datetime.date.today()
    response = requests.get(base_url+'markets/history',
        params={'symbol': symbol, 'interval': 'daily', 'start': (now  - datetime.timedelta(days)).strftime("%Y-%m-%d"), 'end': now.strftime("%Y-%m-%d"), 'session_filter': 'all'},
        headers={'Authorization': 'Bearer ' + access_token, 'Accept': 'application/json'}
    )
    return response.json()

def jsonGetPositions():
    response = requests.get(base_url + 'accounts/' + account_id + '/positions',
        params={},
        headers={'Authorization': 'Bearer ' + access_token, 'Accept': 'application/json'}
    )
    return response.json()

def getPositions():
    try:
        pos = []
        js = jsonGetPositions()
        for i in js['positions']['position']:
            pos.append([i['symbol'], int(i['quantity'])])
        return pos
    except:
        return []
        

def buyEquity(symbol):
    response = requests.post(base_url + 'accounts/' + account_id + '/orders',
        data={'class': 'equity', 'symbol': symbol, 'side': 'buy', 'quantity': '1', 'type': 'market', 'duration': 'day'},
        headers={'Authorization': 'Bearer ' + access_token, 'Accept': 'application/json'}
    )
    json_response = response.json()
    
def sellEquity(symbol, amt):
    response = requests.post(base_url + 'accounts/' + account_id + '/orders',
        data={'class': 'equity', 'symbol': symbol, 'side': 'sell', 'quantity': str(amt), 'type': 'market', 'duration': 'day'},
        headers={'Authorization': 'Bearer ' + access_token, 'Accept': 'application/json'}
    )
    json_response = response.json()

def getCurrentSymbolPrice(symbol):
    data = jsonGetSymbolData(symbol)
    try:
        return data['quotes']['quote']['last']
    except:
        return None

def getPercentChange(symbol):
    data = jsonGetSymbolData(symbol)
    try:
        return data['quotes']['quote']['change_percentage']
    except:
        return None

def SMA(symbol, days):
    his = jsonGetSymbolHistory(symbol, days)
    if his['history'] == None:
        return None
    his = his['history']['day']
    tot = 0
    openDays = 0
    for h in his:
        tot += h['close']
        openDays += 1
    return float(tot) / openDays

def trend(symbol, days):
    sma = SMA(symbol, days)
    if sma == None:
        return "skip"
    currentPrice = jsonGetSymbolData(symbol)['quotes']['quote']['last']
    if currentPrice > sma:
        return "uptrend"
    else:
        return "downtrend"

def getMarketStatus():
    response = requests.get(base_url + 'markets/clock',
        params={'delayed': 'false'}, #remove parameter for real
        headers={'Authorization': 'Bearer <TOKEN>', 'Accept': 'application/json'}
    )
    return response.json()['clock']['state']

def currentSP500():
    table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    df = table[0]
    return list(df['Symbol'])