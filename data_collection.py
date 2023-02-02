import nsepy
import numpy as np
import pandas as pd
import datetime
import requests
import io

url = 'https://archives.nseindia.com/content/equities/EQUITY_L.csv'
s = requests.get(url).content

stock_ticker_df = pd.read_csv(io.StringIO(s.decode('utf-8')))
tickers = stock_ticker_df['SYMBOL'][1:1000]

tickers = tickers.tolist()

s_data3 = pd.DataFrame()
today = datetime.datetime.today()

for t in tickers:
    s_data = nsepy.get_history(t, start=today-datetime.timedelta(days=30), end=today)  
    s_data = s_data.reset_index()
    s_data['Date'] = pd.to_datetime(s_data['Date'], format="%Y-%m-%d")
    
    offsets = [1, 2, 3,4,5,6,7,14,30,90,180,365,1095]

    s_data2 = s_data[['Symbol','Date']]

    
    for offset in offsets:
        col_name = f"cp_{offset}_days_ago" 
        s_data2[col_name] = s_data['Close'].shift(offset)

    # Forward fill the NaN values in the new columns
    s_data2.fillna(method='ffill', inplace=True)
    latest_date = s_data2['Date'].max()
    s_data2 = s_data2.loc[s_data2['Date'] == latest_date]
    s_data3 = s_data3.append(s_data2)


s_data3.to_json("s_data5.json", orient="records")


