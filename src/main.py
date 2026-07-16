import yfinance as yf

print ("Hello ETF Portfolio Analyzer")

ticker = "VOO"
data = yf.download(ticker, period="1y")
VOO_close_data = data["Close"]
print(VOO_close_data.iloc[0])
print(type(data))
print(type(VOO_close_data))