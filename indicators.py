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

    ema9 = last["EMA9"]
    ema20 = last["EMA20"]
    rsi = last["RSI"]
    macd = last["MACD"]
    macd_signal = last["MACD_SIGNAL"]
    adx = last["ADX"]
    volume = last["Volume"]
    avg_volume = last["AVG_VOLUME"]

    # STRONG BUY
    if (
        ema9 > ema20
        and 55 <= rsi <= 70
        and macd > macd_signal
        and adx > 25
        and volume > avg_volume
    ):
        return "🟢 STRONG BUY"

    # BUY
    elif (
        ema9 > ema20
        and rsi > 50
        and macd > macd_signal
    ):
        return "🟢 BUY"

    # STRONG SELL
    elif (
        ema9 < ema20
        and rsi < 45
        and macd < macd_signal
        and adx > 25
    ):
        return "🔴 STRONG SELL"

    # SELL
    elif (
        ema9 < ema20
        and rsi < 50
    ):
        return "🔴 SELL"

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
from ta.trend import ADXIndicator

def calculate_adx(data):
    adx = ADXIndicator(
        high=data["High"],
        low=data["Low"],
        close=data["Close"],
        window=14
    )

    data["ADX"] = adx.adx()

    return data
def calculate_support_resistance(data):

    resistance = data["High"].rolling(20).max()

    support = data["Low"].rolling(20).min()

    data["Resistance"] = resistance

    data["Support"] = support

    return data
def calculate_volume(data):
    data["AVG_VOLUME"] = data["Volume"].rolling(20).mean()
    return data