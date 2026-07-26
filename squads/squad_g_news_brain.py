class NewsSentimentBrain:
    """Squad G: News & NLP Sentiment Analysis Brain"""
    def evaluate(self, headlines: list) -> dict:
        positive_words = ["soar", "gain", "profit", "plan", "overhaul", "growth", "active"]
        negative_words = ["wobbly", "fall", "loss", "drop", "tax", "crash", "down"]
        
        score = 0
        for item in headlines:
            title = item.get("title", "").lower()
            score += sum(1 for w in positive_words if w in title)
            score -= sum(1 for w in negative_words if w in title)
            
        signal = 1 if score > 0 else (-1 if score < 0 else 0)
        return {"signal": signal, "confidence": 0.80, "sentiment_score": score}
