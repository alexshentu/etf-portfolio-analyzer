import yfinance as yf

print ("Hello ETF Portfolio Analyzer")

ticker = "VOO"
data = yf.download(ticker, period="1y")
close_data = data["Close"]
print(close_data.iloc[0])
print(type(data))
print(type(close_data))

daily_return = close_data.pct_change(1)
print(daily_return.mean())