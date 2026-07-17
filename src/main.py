import yfinance as yf

ticker = "VOO"
data = yf.download(ticker, period="1y")
close_data = data["Close"][ticker]
daily_return = close_data.pct_change()

best_day = daily_return.idxmax()
best_return = daily_return.max()

worst_day = daily_return.idxmin()
worst_return = daily_return.min()

daily_volatility = daily_return.std()
annual_volatility = daily_volatility * (252 ** 0.5)

growth_factor = daily_volatility + 1
total_return = growth_factor.cumprod().iloc[-1] - 1

print (f"Best Day: {best_day}")
print (f"Best Return: {best_return:.2%}")

print (f"Worst Day: {worst_day}")
print (f"Worst Return: {worst_return:.2%}")

print (f"Daily Volatility: {daily_volatility:.2%}")
print (f"Annual Volatility: {annual_volatility:.2%}")

print (f"Total Return: {total_return:.2%}")