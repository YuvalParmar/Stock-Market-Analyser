import yfinance as yf
import pandas as pd

tickers = ["AAPL","MSFT","GOOGL","AMZN","TSLA","NVDA","^GSPC","^IXIC","^FTSE","^DJI"]
all_data = {}

for ticker in tickers:
    stock = yf.Ticker(ticker)
    data = stock.history(period="10y")

    # Skip empty datasets
    if data.empty:
        print(ticker, "has no data, skipping")
        continue

    # Clean data
    data = data.sort_index(ascending=True)  # oldest to newest
    data = data[~data.index.duplicated(keep="first")]
    data = data.dropna(subset=["Open","High","Low","Close","Volume"])
    data = data[(data["Close"] > 0) & (data["Volume"] > 0)]
    if len(data) < 250:
        print(ticker, "doesn't have enough history, skipping")
        continue

    # Calculate indicators
    data["MA20"] = data["Close"].rolling(20).mean()
    data["MA50"] = data["Close"].rolling(50).mean()
    data["MA200"] = data["Close"].rolling(200).mean()

    all_data[ticker] = data

# Check last rows for one stock
print(all_data["AAPL"][["Close", "MA20", "MA50", "MA200"]].tail())