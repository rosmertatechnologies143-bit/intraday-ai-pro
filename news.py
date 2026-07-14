import feedparser

def get_market_news():
    url = "https://news.google.com/rss/search?q=Indian+stock+market&hl=en-IN&gl=IN&ceid=IN:en"

    feed = feedparser.parse(url)

    news = []

    for item in feed.entries[:5]:
        news.append({
            "title": item.title,
            "link": item.link
        })

    return news