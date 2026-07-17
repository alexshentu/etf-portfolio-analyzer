import yfinance as yf

#download info 
ticker = "VOO"
data = yf.download(ticker, period="1y")
close_data = data["Close"][ticker]
daily_return = close_data.pct_change()

#best/worst day
best_day = daily_return.idxmax()
best_return = daily_return.max()

worst_day = daily_return.idxmin()
worst_return = daily_return.min()

#volatility 
daily_volatility = daily_return.std()
annual_volatility = daily_volatility * (252 ** 0.5)

#total return 
growth_factor = daily_return + 1
total_return = growth_factor.cumprod().iloc[-1] - 1

#maximum drawdown 
historical_high = close_data.cummax()
daily_drawdown = (close_data - historical_high) / historical_high
maximum_drawdown = daily_drawdown.min()
MDD_day = daily_drawdown.idxmin()

#output
print (f"Best Day: {best_day}")
print (f"Best Return: {best_return:.2%}")
print()
print (f"Worst Day: {worst_day}")
print (f"Worst Return: {worst_return:.2%}")
print()
print (f"Daily Volatility: {daily_volatility:.2%}")
print (f"Annual Volatility: {annual_volatility:.2%}")
print()
print (f"Total Return: {total_return:.2%}")
print()
print (f"Maximum Drawdown Day: {MDD_day}")
print(f"Maximum Drawdown: {maximum_drawdown:.2%}")