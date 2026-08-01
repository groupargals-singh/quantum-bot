import requests

class OptionChainAnalyzer:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }

    def calculate_pcr(self, total_put_oi: int, total_call_oi: int) -> float:
        if total_call_oi == 0:
            return 0.0
        return round(total_put_oi / total_call_oi, 2)

    def get_market_bias(self, pcr: float) -> str:
        if pcr > 1.2:
            return "BULLISH 🐂"
        elif pcr < 0.8:
            return "BEARISH 🐻"
        return "NEUTRAL ⚖️"
