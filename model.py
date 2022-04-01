from datetime import datetime, timedelta
from typing import Any
import pandas as pd

df = pd.read_csv('selected.csv')
df.date = df.date.apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

class EvalStrategy:
    def __init__(self, data: pd.DataFrame, span_days: int, span_2: int,
                 devation_upper: float, deviation_lower: float,
                 n_shares: int = 50) -> None:
        self.data = data
        self.n_shares = n_shares
        self.deviation_upper = devation_upper
        self.deviation_lower = deviation_lower
        self.span_days = span_days
        self.span_2 = span_2
        self.start_date = self.data['date'].min()
        self.cur_date = self.start_date
        self.shares = {ticker: 0 for ticker in self.data['ticker'].unique()}
        self.profit = 0
        self.last_sold = self.cur_date
    
    @property
    def elapsed(self) -> int:
        return (self.cur_date - self.start_date).days

    def reset(self) -> None:
        self.profit = 0
        self.shares = {ticker: 0 for ticker in self.data['ticker'].unique()}
        self.cur_date = self.start_date
        self.last_sold = self.cur_date

    def last_n(self, ticker: str, span) -> pd.DataFrame:
        date_upper = self.cur_date
        date_lower = self.cur_date - timedelta(days=span)
        return self.data[self.data['ticker'] == ticker][self.data['date'].between(date_lower, date_upper)]
    
    def stock_action(self, ticker: str) -> tuple[int, int]:
        last_period = self.last_n(ticker, self.span_days)
        last_period2 = self.last_n(ticker, self.span_2)
        last_avg = last_period['close'].mean()
        last_avg2 = last_period2['close'].mean()
        if self.elapsed < self.span_days:
            return (0, 0)
        try:
            today_price = last_period[last_period['date'] == (self.cur_date - timedelta(days=1))]['close'].iloc[0]
            if last_avg2 > last_avg * self.deviation_upper:
                return (self.n_shares, -self.n_shares * today_price)
            elif (last_avg2 < last_avg * self.deviation_lower) and self.shares[ticker] > 0:
                return (-self.n_shares, self.n_shares * today_price)
            else:
                return (0, 0)
        except Exception as e:
            return (0, 0)

    def timestep(self, steps=1):
        for _ in range(steps):
            self.cur_date += timedelta(days=1)
            for ticker in self.shares:
                action, cost = self.stock_action(ticker)
                self.shares[ticker] += action
                self.profit += cost

strat = EvalStrategy(data=df, span_days=150, span_2=50, devation_upper=1.1, deviation_lower=1.1)