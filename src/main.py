import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


#download info 
def download_data(ticker, period):
    data = yf.download(ticker, period=period)
    close_data = data["Close"][ticker]
    daily_return = close_data.pct_change()
    return close_data, daily_return



def calculate_metrics(close_data, daily_return, period):
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
    initial_price = close_data.iloc[0]
    final_price = close_data.iloc[-1]
    total_return = (final_price / initial_price) - 1

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

    #CAGR
    years = int(period[:-1])
    cagr = (1 + total_return) ** (1 / years) - 1
    metrics["cagr"] = cagr

    #sharpe
    sharpe = calculate_sharpe(cagr, annual_volatility)
    metrics["sharpe_ratio"] = sharpe


    return metrics, moving_average_20, moving_average_50, daily_drawdown
    # Returned for future drawdown visualization

def calculate_sharpe(cagr, annual_volatility, risk_free_rate=0):
    if annual_volatility == 0:
        raise ValueError("Annual volatility cannot be zero.")
    sharpe = (cagr - risk_free_rate) / annual_volatility
    return sharpe

metrics_format = {"best_day" : "date", 
                  "best_return" : "percent", 
                  "worst_day" : "date",
                  "maximum_drawdown_day" : "date",
                  "maximum_drawdown" : "percent",
                  "worst_return" : "percent",
                  "daily_volatility" : "percent",
                  "annual_volatility" : "percent",
                  "total_return" : "percent",
                  "cagr" : "percent",
                  "20_day_moving_average" : "number",
                  "50_day_moving_average" : "number",
                  "sharpe_ratio" : "number"}


def print_metrics(metrics):
    for key, value in metrics.items():
        format_type = metrics_format.get(key)
        if format_type == "date":
            print(f"{key.replace('_', ' ').title()}: {value}")
        elif format_type == "percent":
            print(f"{key.replace('_', ' ').title()}: {value:.2%}")
        elif format_type == "number":
            print(f"{key.replace('_', ' ').title()}: {value:.2f}")
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

def plot_comparison(cumulative_results):
    for ticker, cumulative_returns in cumulative_results.items():
        cumulative_returns.plot(label = ticker, linewidth = 1)

    plt.gca().yaxis.set_major_formatter(PercentFormatter(1.0))
    plt.title("ETFs Comparison")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.grid()
    plt.legend()
    plt.show()

def get_tickers():
    ticker_list = []
    while True:
        ticker = input("Please enter ETF ticker(Press enter to finish): ")
        if ticker == "":
            break
        ticker = ticker.upper()
        ticker_list.append(ticker)
    
    return ticker_list 



def find_metric(results, desire_metric, mode):
    if mode not in ("max", "min"):
        raise ValueError(f"Invalid mode: {mode}. Mode must be 'max' or 'min'.")
    best_name = None
    best_metric = None
    for key, value in results.items():
        if best_metric is None:
            best_metric = value[desire_metric]
            best_name = key

        elif mode == "min" and value[desire_metric] < best_metric:
            best_metric = value[desire_metric]
            best_name = key

        elif mode == "max" and value[desire_metric] > best_metric:
            best_metric = value[desire_metric]
            best_name = key
        
    return best_name, best_metric

def rank_metrics(results, desire_metric):
    ranking = sorted(results.items(), key=lambda item: item[1][desire_metric], reverse=True,)
    return ranking

def print_rank(ranking, desire_metric):
    print(f"\n========== {desire_metric} Ranking ==========")
    format_type = metrics_format.get(desire_metric)
    for index, (ticker, metrics) in enumerate(ranking, start=1):
        if format_type == "date":
            print (f"{index}. {ticker}: {metrics[desire_metric]}")
        elif format_type == "percent":
            print (f"{index}. {ticker}: {metrics[desire_metric]:.2%}")
        elif format_type == "number":
            print (f"{index}. {ticker}: {metrics[desire_metric]:.2f}")
        else:
            print (f"{index}. {ticker}: {metrics[desire_metric]}")



def main(ticker, period):
    close_data, daily_return = download_data(ticker, period)

    metrics, moving_average_20, moving_average_50, daily_drawdown = calculate_metrics(close_data, daily_return, period)

    
    cumulative_return= close_data / close_data.iloc[0] - 1
    
    print(f"\n========== {ticker} ==========")
    print_metrics(metrics)

    #plot_chart(close_data, moving_average_20, moving_average_50, ticker)
    return metrics, cumulative_return

def calculate_excess_returns(results, benchmark):
    benchmark_return = results[benchmark]["total_return"]
    excess_return = {}
    for ticker, metrics in results.items():
        excess_return[ticker] = metrics["total_return"] - benchmark_return
    return excess_return

def print_excess_returns(excess_returns, benchmark):
    ranking = sorted(excess_returns.items(), key=lambda item: item[1], reverse=True,)
    print(f"\n========== Excess Return vs {benchmark} ==========")
    for index, (ticker, returns) in enumerate(ranking, start=1):
        print (f"{index}. {ticker}: {returns:.2%}")

    

if __name__ == "__main__":
    results = {}
    cumulative_results = {}
    tickers = get_tickers()
    period = input("Enter analysis period (1y/3y/5y/10y): ").lower()
    if period not in ("1y", "3y", "5y", "10y"):
        raise ValueError("Invalid analysis period.")
    benchmark = input("Enter benchmark ETF: ").upper()
    if benchmark not in tickers:
        raise ValueError("Benchmark must be one of the selected ETFs.")
    for ticker in tickers: 
        results[ticker], cumulative_results[ticker]= main(ticker, period)

    excess_returns = calculate_excess_returns(results, benchmark)
    print_excess_returns(excess_returns, benchmark)

    print("\n========== ETF Comparison ==========")
    best_return_ticker, best_return = find_metric(results, "total_return", "max")
    print(f"Highest Return: {best_return_ticker} ({best_return:.2%})")
    best_volatility_ticker, best_volatility = find_metric(results, "annual_volatility", "min")
    print(f"Lowest Annual Volatility: "f"{best_volatility_ticker} ({best_volatility:.2%})")
    ranking = rank_metrics(results, "sharpe_ratio")
    print_rank(ranking, "sharpe_ratio")
    plot_comparison(cumulative_results)
