import pandas as pd
import json
import io
import requests
import numpy as np
import yfinance as yf
from datetime import date
from dateutil.relativedelta import relativedelta

url = 'https://archives.nseindia.com/content/equities/EQUITY_L.csv'
s = requests.get(url).content

df = pd.read_csv(io.StringIO(s.decode('utf-8')))

data_file = pd.DataFrame(columns=['stock_name','Close'],index=['Date'])
data_file['Close'] = data_file['Close'].astype(float)

test_trigs = np.array([df['SYMBOL'][35], df['SYMBOL'][36], df['SYMBOL'][37], df['SYMBOL'][38]])

test_trigs = pd.Series(test_trigs)

for trig in test_trigs:
    data_trig = trig +'.NS'
    mod_data = yf.download(data_trig,start = date.today() + relativedelta(months=-1) , end = date.today())
    mod_data['stock_name'] = trig
    mod_data = mod_data[['stock_name','Close']]
    data_file = data_file.append(mod_data)

data_file = data_file.dropna(subset=['stock_name','Close'])
data_file = data_file.reset_index()
data_file_json = data_file.to_json(orient="records")

with open("data.json", "w") as file:
    json.dump(data_file_json, file)