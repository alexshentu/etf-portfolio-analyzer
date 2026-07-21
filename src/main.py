import yfinance as yf
import matplotlib.pyplot as plt

#download info 
def download_data(ticker):
    data = yf.download(ticker, period="1y")
    close_data = data["Close"][ticker]
    daily_return = close_data.pct_change()
    return close_data, daily_return



def calculate_metrics(close_data, daily_return):
    metrics = {}

    #best/worst day
    best_day = daily_return.idxmax()
    best_return = daily_return.max()

    metrics ["best_day"] = best_day.date()
    metrics ["best_return"] = best_return

    worst_day = daily_return.idxmin()
    worst_return = daily_return.min()

    metrics["worst_day"] = worst_day.date()
    metrics["worst_return"] = worst_return

    #volatility 
    daily_volatility = daily_return.std()
    annual_volatility = daily_volatility * (252 ** 0.5)

    metrics["daily_volatility"] = daily_volatility
    metrics["annual_volatility"] = annual_volatility

    #total return 
    growth_factor = daily_return + 1
    total_return = growth_factor.cumprod().iloc[-1] - 1

    metrics["total_return"] = total_return

    #maximum drawdown 
    historical_high = close_data.cummax()
    daily_drawdown = (close_data - historical_high) / historical_high
    maximum_drawdown = daily_drawdown.min()
    MDD_day = daily_drawdown.idxmin()

    metrics["maximum_drawdown_day"] = MDD_day.date()
    metrics["maximum_drawdown"] = maximum_drawdown

    #moving average
    moving_average_20 = close_data.rolling(20).mean()
    moving_average_50 = close_data.rolling(50).mean()

    metrics["20_day_moving_average"] = moving_average_20.iloc[-1]
    metrics["50_day_moving_average"] = moving_average_50.iloc[-1]

    return metrics, moving_average_20, moving_average_50, daily_drawdown
    # Returned for future drawdown visualization

def print_metrics(metrics):
    for key, value in metrics.items():
        if "day" in key:
            print(f"{key.replace('_', ' ').title()}: {value}")
        elif "return" in key or "volatility" in key or "drawdown" in key:
            print(f"{key.replace('_', ' ').title()}: {value:.2%}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")

def plot_chart(close_data, moving_average_20, moving_average_50, ticker):
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

    golden_cross = ((moving_average_20 > moving_average_50)
    & (moving_average_20.shift(1) <= moving_average_50.shift(1)))

    plt.scatter(close_data[golden_cross].index,
            close_data[golden_cross],
            color="green",
            s=120,
            label="Golden Cross", 
            marker = "^")

    #death cross
    death_cross = ((moving_average_20 < moving_average_50)
    & (moving_average_20.shift(1) >= moving_average_50.shift(1)))

    plt.scatter(close_data[death_cross].index,
            close_data[death_cross],
            color="red",
            s=120,
            label="Death Cross", 
            marker = "v")    
    

    plt.title(f"{ticker} Price Analysis")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.grid()
    plt.legend()
    plt.show()

def main(ticker):
    close_data, daily_return = download_data(ticker)

    metrics, moving_average_20, moving_average_50, daily_drawdown = calculate_metrics(close_data, daily_return)
    
    print(f"\n========== {ticker} ==========")
    print_metrics(metrics)

    #plot_chart(close_data, moving_average_20, moving_average_50, ticker)

def get_tickers():
    ticker_list = []
    while True:
        ticker = input("Please enter ETF ticker(Press enter to finish): ")
        if ticker == "":
            break
        ticker = ticker.upper()
        ticker_list.append(ticker)
    
    return ticker_list 

if __name__ == "__main__":
    tickers = get_tickers()
    
    for ticker in tickers:
        main(ticker)