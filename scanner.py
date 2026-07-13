import yfinance as yf
from indicators import calculate_ema, calculate_rsi, get_signal

stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "SBIN.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "ITC.NS",
    "LT.NS",
    "BHARTIARTL.NS",
    "AXISBANK.NS"
]

print("=" * 80)
print("                 TOP 10 INTRADAY STOCK SCANNER")
print("=" * 80)

print(f"{'STOCK':18} {'PRICE':10} {'RSI':8} {'SIGNAL'}")
print("-" * 80)

for symbol in stocks:
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="5d", interval="5m")

        if data.empty:
            print(f"{symbol:18} No Data")
            continue

        data["EMA9"] = calculate_ema(data, 9)
        data["EMA20"] = calculate_ema(data, 20)
        data["RSI"] = calculate_rsi(data)

        signal = get_signal(data)

        price = round(data["Close"].iloc[-1], 2)
        rsi = round(data["RSI"].iloc[-1], 2)

        print(f"{symbol:18} ₹{price:<9} {rsi:<8} {signal}")

    except Exception as e:
        print(f"{symbol:18} ERROR : {e}")

print("=" * 80)
print("Scan Completed")
print("=" * 80)