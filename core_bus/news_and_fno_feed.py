import feedparser
import requests

class NewsAndFnOFeedManager:
    """Lightweight & Super-Fast Feed Manager"""
    def __init__(self):
        self.news_urls = [
            "https://www.moneycontrol.com/rss/MCtopnews.xml",
            "https://economictimes.indiatimes.com/markets/rssfeeds/2146842.cms"
        ]

    def fetch_latest_market_news(self) -> list:
        headlines = []
        for url in self.news_urls:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:2]:
                    headlines.append({
                        "title": entry.title,
                        "source": feed.feed.get("title", "Market News")
                    })
            except Exception:
                continue
        return headlines

    def fetch_nse_market_sentiment(self) -> dict:
        try:
            url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EINDIAVIX"
            headers = {'User-Agent': 'Mozilla/5.0'}
            resp = requests.get(url, headers=headers, timeout=3)
            if resp.status_code == 200:
                data = resp.json()
                vix = round(data['chart']['result'][0]['meta']['regularMarketPrice'], 2)
                return {"india_vix": vix, "status": "LIVE"}
        except Exception:
            pass
        return {"india_vix": 14.2, "status": "DEFAULT"}
