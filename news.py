import feedparser
def get_sentiment(title):
    title = title.lower()

    positive_words = [
    "gain",
    "surge",
    "rise",
    "profit",
    "growth",
    "record high",
    "strong buy",
    "bullish",
    "expansion",
    "beats",
    "jumps",
    "rally"
]

    negative_words = [
    "fall",
    "falls",
    "drop",
    "drops",
    "loss",
    "crash",
    "bearish",
    "decline",
    "slip",
    "lower",
    "weak",
    "sell",
    "plunge",
    "tumbles"
] 

    for word in positive_words:
        if word in title:
            return "🟢 Positive"

    for word in negative_words:
        if word in title:
            return "🔴 Negative"

    return "🟡 Neutral"
def get_market_news(stock_name="Indian stock market"):
    query = stock_name.replace(".NS", "").replace("&", " ")

url = f"https://news.google.com/rss/search?q={query}+India+stock&hl=en-IN&gl=IN&ceid=IN:en"

    feed = feedparser.parse(url)

    news = []

    for item in feed.entries[:5]:
        news.append({
            "title": item.title,
            "link": item.link,
            "sentiment": get_sentiment(item.title)
        })

    return news