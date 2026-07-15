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
def calculate_news_score(news):
    positive = sum(1 for item in news if "Positive" in item["sentiment"])
    negative = sum(1 for item in news if "Negative" in item["sentiment"])
    neutral = sum(1 for item in news if "Neutral" in item["sentiment"])

    score = (positive * 20) + (neutral * 10)

    if score > 100:
        score = 100

    return {
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "score": score
    }
def get_hindi_summary(title):
    title = title.lower()

    if "bullish" in title or "buy" in title:
        return "🟢 यह खबर शेयर के लिए सकारात्मक मानी जा रही है। खरीदारी का माहौल बन सकता है।"

    elif "target" in title:
        return "🎯 ब्रोकरेज ने शेयर का लक्ष्य मूल्य बढ़ाया है। यह निवेशकों के लिए सकारात्मक संकेत हो सकता है।"

    elif "jump" in title or "surge" in title or "rise" in title:
        return "📈 शेयर में तेजी देखने को मिली है। बाजार में खरीदारी का रुझान दिखाई दे रहा है।"

    elif "fall" in title or "lower" in title or "drop" in title or "tumble" in title:
        return "📉 शेयर या बाजार में गिरावट आई है। निवेशकों को सावधानी बरतनी चाहिए।"

    elif "sell" in title:
        return "⚠️ कंपनी से जुड़ी बिक्री की खबर है। इसका असर शेयर की कीमत पर पड़ सकता है।"

    else:
        return "📰 यह एक सामान्य बाजार समाचार है। निवेश करने से पहले पूरी जानकारी देखें।"
    
def get_general_market_news():
    url = "https://news.google.com/rss/search?q=Indian+Stock+Market+OR+Sensex+OR+Nifty+OR+RBI+OR+Crude+Oil&hl=en-IN&gl=IN&ceid=IN:en"

    feed = feedparser.parse(url)

    news = []

    for item in feed.entries[:5]:
        news.append({
            "title": item.title,
            "link": item.link,
            "sentiment": get_sentiment(item.title)
        })

    return news
def calculate_market_mood(news):
    positive = 0
    negative = 0
    neutral = 0

    for item in news:
        if item["sentiment"] == "🟢 Positive":
            positive += 1
        elif item["sentiment"] == "🔴 Negative":
            negative += 1
        else:
            neutral += 1

    score = positive * 20 + neutral * 10

    if score >= 70:
        trend = "🟢 Bullish"
    elif score >= 40:
        trend = "🟡 Neutral"
    else:
        trend = "🔴 Bearish"

    return {
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "score": score,
        "trend": trend,
    }