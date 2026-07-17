import yfinance as yf

ticker = "VOO"
data = yf.download(ticker, period="1y")
close_data = data["Close"][ticker]
daily_return = close_data.pct_change()

best_day = daily_return.idxmax()
best_return = daily_return.max()
print (f"Best Day: {best_day}")
print (f"Return: {best_return:.2%}")