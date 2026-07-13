from indicators import calculate_ema, calculate_rsi, get_signal
import yfinance as yf

# Stock Symbol
symbol = "RELIANCE.NS"

# Download Data
stock = yf.Ticker(symbol)
data = stock.history(period="5d", interval="5m")

# Calculate EMA
data["EMA9"] = calculate_ema(data, 9)
data["EMA20"] = calculate_ema(data, 20)
data["RSI"] = calculate_rsi(data)
# Latest Close Price
close_price = data["Close"].iloc[-1]

# Signal
signal = get_signal(data)

print("=" * 40)
print("Stock :", symbol)
print("Close Price :", round(close_price, 2))
print("EMA 9 :", round(data["EMA9"].iloc[-1], 2))
print("EMA 20 :", round(data["EMA20"].iloc[-1], 2))
print("RSI :", round(data["RSI"].iloc[-1], 2))
print("Signal :", signal)
print("=" * 40)