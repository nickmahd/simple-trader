from datetime import datetime
import io
from os import environ as env
import requests as rq

from bs4 import BeautifulSoup as BS
import pandas as pd

class Request:
    base_url = "https://api.unibit.ai/v2/stock/historical"
    defaults = {'interval': 1,
                'selectedFields': 'all',
                'dataType': 'csv',
                'accessKey': env['REQUEST_API_KEY']
                }

    def __init__(self, start: datetime, end: datetime, tickers: list):
        start_str = start.strftime("%Y-%m-%d")
        end_str = end.strftime("%Y-%m-%d")
        self.params = {'tickers': ','.join(tickers),
                       'startDate': start_str,
                       'endDate': end_str
                       }
        self.params.update(Request.defaults)

    @property
    def content(self):
        try:
            self.r
        except AttributeError:
            self._fetch()
        
        return self.r

    def _fetch(self):
        self.r = rq.get(f"{Request.base_url}", params=self.params).content

ticker_list = ['MSFT', 'AMZN', 'AAPL', 'GOOG', 'FB']
call = Request(start=datetime(2020, 1, 1),
               end=datetime(2021, 12, 1),
               tickers=ticker_list
               )

with open('data.csv', 'wb') as f:
    f.write(call.content)

df = pd.read_csv('data.csv')
df[['date', 'ticker', 'close']].to_csv('selected.csv')