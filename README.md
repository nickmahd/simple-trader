# simple-trader
A small SMA-based algotrading model.

For each stock ticker, the strategy checks the average price of the last n=200 days and compares it to the average price of the last m=50 days. If the two differ by a certain factor (in this case 1.1), then the model buys or sells s=50 shares. Using this strategy from 2020-2022 on the tickers MSFT, AMZN, AAPL, GOOG, and FB would have made a net profit of roughly $1.3M.
