import pandas as pd

# EMA
def calculate_ema(data, period):
    return data["Close"].ewm(span=period, adjust=False).mean()


# RSI
def calculate_rsi(data, period=14):
    delta = data["Close"].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


# Signal
def get_signal(data):
    last = data.iloc[-1]

    if last["EMA9"] > last["EMA20"] and last["RSI"] > 55:
        return "🟢 STRONG BUY"

    elif last["EMA9"] < last["EMA20"] and last["RSI"] < 45:
        return "🔴 STRONG SELL"

    else:
        return "🟡 WAIT"


# MACD
def calculate_macd(data):
    ema12 = data["Close"].ewm(span=12, adjust=False).mean()
    ema26 = data["Close"].ewm(span=26, adjust=False).mean()

    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()

    data["MACD"] = macd
    data["MACD_SIGNAL"] = signal

    return data