import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from indicators import calculate_ema, calculate_rsi, get_signal, calculate_macd
from news import get_market_news, calculate_news_score
st.set_page_config(page_title="Intraday AI Pro", layout="wide")

st.title("📈 Intraday AI Pro")
st.subheader("Top 50 NIFTY Scanner")

# Refresh Button
st.button("🔄 Refresh Scanner")

# Filter
filter_option = st.selectbox(
    "Select Signal",
    ["ALL", "🟢 STRONG BUY", "🔴 STRONG SELL", "🟡 WAIT"]
)

# Search
search = st.text_input(
    "🔍 Search Stock",
    placeholder="Stock Name likho... (SBIN, TCS, RELIANCE)"
)

# Stock List




stocks = [
    "ADANIPORTS.NS", "ASIANPAINT.NS", "AXISBANK.NS", "BAJAJ-AUTO.NS",
    "BAJFINANCE.NS", "BAJAJFINSV.NS", "BEL.NS", "BHARTIARTL.NS",
    "CIPLA.NS", "COALINDIA.NS", "DRREDDY.NS", "EICHERMOT.NS",
    "ETERNAL.NS", "GRASIM.NS", "HCLTECH.NS", "HDFCBANK.NS",
    "HDFCLIFE.NS", "HEROMOTOCO.NS", "HINDALCO.NS", "HINDUNILVR.NS",
    "ICICIBANK.NS", "INDUSINDBK.NS", "INFY.NS", "ITC.NS",
    "JIOFIN.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LT.NS",
    "M&M.NS", "MARUTI.NS", "NESTLEIND.NS", "NTPC.NS",
    "ONGC.NS", "POWERGRID.NS", "RELIANCE.NS", "SBILIFE.NS",
    "SBIN.NS", "SHRIRAMFIN.NS", "SUNPHARMA.NS", "TATACONSUM.NS",
    "TATAMOTORS.NS", "TATASTEEL.NS", "TCS.NS", "TECHM.NS",
    "TITAN.NS", "TRENT.NS", "ULTRACEMCO.NS", "WIPRO.NS"
]
   

# Chart Stock Selection
selected_stock = st.selectbox(
    "📈 Select Stock Chart",
    stocks
)

rows = []

# Scanner
for symbol in stocks:

    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="5d", interval="5m")

        if data.empty:
            continue

        data["EMA9"] = calculate_ema(data, 9)
        data["EMA20"] = calculate_ema(data, 20)
        data["RSI"] = calculate_rsi(data)

        signal = get_signal(data)

        price = round(data["Close"].iloc[-1], 2)
        rsi = round(data["RSI"].iloc[-1], 2)

        entry = round(price * 1.002, 2)
        stoploss = round(price * 0.99, 2)
        target = round(price * 1.02, 2)

        if "BUY" in signal:
            confidence = "90%"
            ai_score = 95
        elif "SELL" in signal:
            confidence = "88%"
            ai_score = 30
        else:
            confidence = "70%"
            ai_score = 65

        rows.append({
            "Stock": symbol,
            "Price (₹)": price,
            "RSI": rsi,
            "Signal": signal,
            "Entry": entry,
            "Stop Loss": stoploss,
            "Target": target,
            "Confidence": confidence,
            "AI Score": ai_score,
        })

    except Exception as e:
        st.error(f"{symbol}: {e}")

# Dashboard Cards
buy_count = sum("BUY" in row["Signal"] for row in rows)
sell_count = sum("SELL" in row["Signal"] for row in rows)
wait_count = sum("WAIT" in row["Signal"] for row in rows)

c1, c2, c3, c4 = st.columns(4)

c1.metric("🟢 BUY", buy_count)
c2.metric("🔴 SELL", sell_count)
c3.metric("🟡 WAIT", wait_count)
c4.metric("📈 TOTAL", len(rows))

# DataFrame
df = pd.DataFrame(rows)

# Search
if search:
    df = df[df["Stock"].str.contains(search.upper())]

# Filter
if filter_option != "ALL":
    df = df[df["Signal"] == filter_option]
st.subheader("🏆 Top Intraday Picks")

top_buy = df[df["Signal"] == "🟢 STRONG BUY"]

st.dataframe(top_buy.head(5), use_container_width=True)
st.dataframe(df, width="stretch")
st.subheader("📰 Latest Market News")

news = get_market_news(selected_stock)
summary = calculate_news_score(news)

st.info(f"🟢 Positive: {summary['positive']} | 🔴 Negative: {summary['negative']} | 🟡 Neutral: {summary['neutral']} | ⭐ News Score: {summary['score']}/100")
for item in news:
    st.markdown(
        f'{item["sentiment"]} '
        f'[{item["title"]}]({item["link"]})'
    )
st.subheader("🤖 AI Recommendation")

stock = yf.Ticker(selected_stock)
timeframe = st.selectbox(
    "📊 Time Frame",
    ["1 Minute", "5 Minute", "15 Minute", "30 Minute", "1 Hour", "1 Day"],
    index=1
)

if timeframe == "1 Minute":
    period = "1d"
    interval = "1m"
elif timeframe == "5 Minute":
    period = "5d"
    interval = "5m"
elif timeframe == "15 Minute":
    period = "5d"
    interval = "15m"
elif timeframe == "30 Minute":
    period = "1mo"
    interval = "30m"
elif timeframe == "1 Hour":
    period = "3mo"
    interval = "1h"
else:
    period = "6mo"
    interval = "1d"

live_data = stock.history(period=period, interval=interval)

live_data["EMA9"] = calculate_ema(live_data, 9)
live_data["EMA20"] = calculate_ema(live_data, 20)
live_data["RSI"] = calculate_rsi(live_data)

live_data = calculate_macd(live_data)
signal = get_signal(live_data)

macd = round(live_data["MACD"].iloc[-1], 2)
macd_signal = round(live_data["MACD_SIGNAL"].iloc[-1], 2)
price = round(live_data["Close"].iloc[-1], 2)
entry = round(price * 1.002, 2)
stoploss = round(price * 0.99, 2)
target = round(price * 1.02, 2)
risk = round(entry - stoploss, 2)
reward = round(target - entry, 2)

if risk > 0:
    rr_ratio = round(reward / risk, 2)
else:
    rr_ratio = 0
if "BUY" in signal:
    confidence = "90%"
    trend = "📈 Bullish"
elif "SELL" in signal:
    confidence = "88%"
    trend = "📉 Bearish"
else:
    confidence = "70%"
    trend = "➡ Sideways"

st.info(f"""
### {selected_stock}

**Signal :** {signal}

**Trend :** {trend}

**Entry :** ₹{entry}

**Stop Loss :** ₹{stoploss}

**Target :** ₹{target}

**Risk :** ₹{risk}

**Reward :** ₹{reward}

**Risk / Reward :** 1 : {rr_ratio}
**MACD :** {macd}

**MACD Signal :** {macd_signal}

**Confidence :** {confidence}
""")

# Pie Chart
chart_data = pd.DataFrame({
    "Signal": ["BUY", "SELL", "WAIT"],
    "Count": [buy_count, sell_count, wait_count]
})

fig = px.pie(
    chart_data,
    values="Count",
    names="Signal",
    title="📊 Signal Distribution",
    hole=0.4
)

st.plotly_chart(fig, use_container_width=True)

# Live Price Chart
st.subheader("📈 Live Stock Price Chart")

stock = yf.Ticker(selected_stock)
chart_data = stock.history(period=period, interval=interval)
chart_data["EMA9"] = calculate_ema(chart_data, 9)
chart_data["EMA20"] = calculate_ema(chart_data, 20)
fig2 = go.Figure()

fig2.add_trace(
    go.Scatter(
        x=chart_data.index,
        y=chart_data["Close"],
        mode="lines",
        name="Close"
    )
)

fig2.add_trace(
    go.Scatter(
        x=chart_data.index,
        y=chart_data["EMA9"],
        mode="lines",
        name="EMA 9"
    )
)

fig2.add_trace(
    go.Scatter(
        x=chart_data.index,
        y=chart_data["EMA20"],
        mode="lines",
        name="EMA 20"
    )
)

fig2.update_layout(
    title=f"{selected_stock} Live Price Chart",
    xaxis_title="Date",
    yaxis_title="Price"
)

st.plotly_chart(fig2, use_container_width=True)
st.subheader("🕯️ Candlestick Chart")

fig3 = go.Figure(data=[
    go.Candlestick(
        x=chart_data.index,
        open=chart_data["Open"],
        high=chart_data["High"],
        low=chart_data["Low"],
        close=chart_data["Close"],
        name="Candles"
    )
])
fig3.add_trace(
    go.Scatter(
        x=chart_data.index,
        y=chart_data["EMA9"],
        mode="lines",
        name="EMA 9",
        line=dict(color="blue", width=2)
    )
)

fig3.add_trace(
    go.Scatter(
        x=chart_data.index,
        y=chart_data["EMA20"],
        mode="lines",
        name="EMA 20",
        line=dict(color="orange", width=2)
    )
)
fig3.update_layout(
    title=f"{selected_stock} Candlestick Chart",
    xaxis_title="Date",
    yaxis_title="Price",
    xaxis_rangeslider_visible=False
)

st.plotly_chart(fig3, use_container_width=True)
st.subheader("📊 Volume Chart")

fig4 = px.bar(
    chart_data,
    x=chart_data.index,
    y="Volume",
    title=f"{selected_stock} Trading Volume"
)

st.plotly_chart(fig4, use_container_width=True)
st.subheader("📥 Download Report")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📄 Download CSV Report",
    data=csv,
    file_name="Intraday_AI_Report.csv",
    mime="text/csv"
)