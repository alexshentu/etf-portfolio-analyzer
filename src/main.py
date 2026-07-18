import yfinance as yf
import matplotlib.pyplot as plt

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

#moving average
moving_average_20 = close_data.rolling(20).mean()
moving_average_50 = close_data.rolling(50).mean()

#data output
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
print()
print(f"20-Day Moving Average: {moving_average_20.iloc[-1]:.2f}")
print(f"50-Day Moving Average: {moving_average_50.iloc[-1]:.2f}")

#plot
close_data.plot(label = "Close Price", 
                color = "black", 
                linewidth = 2)

moving_average_20.plot(label = "20-Day MA", 
                       color = "blue", 
                       linewidth = 1.5, 
                       linestyle = "--")

moving_average_50.plot(label = "50-Day MA", 
                       color = "red", 
                       linewidth = 1.5, 
                       linestyle = "--")

#golden cross
golden_cross = (
    (moving_average_20 > moving_average_50)
    & (moving_average_20.shift(1) <= moving_average_50.shift(1)))

plt.scatter(close_data[golden_cross].index,
            close_data[golden_cross],
            color="green",
            s=120,
            label="Golden Cross", 
            marker = "^")

#death cross
death_cross = (
    (moving_average_20 < moving_average_50)
    & (moving_average_20.shift(1) >= moving_average_50.shift(1)))

plt.scatter(close_data[death_cross].index,
            close_data[death_cross],
            color="red",
            s=120,
            label="Death Cross", 
            marker = "v")

plt.title("VOO Price Analysis")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.grid()
plt.legend()
plt.show()

