import urllib.request
import json
from typing import List, Optional

class UniversalDataEngine:
    @staticmethod
    def get_live_price(symbol: str) -> Optional[float]:
        """Fetch Real-Time Live Market Price from Yahoo Finance API for NSE Stocks"""
        try:
            formatted_symbol = f"{symbol}.NS" if not symbol.endswith(".NS") else symbol
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{formatted_symbol}?interval=1m&range=1d"
            
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=4) as response:
                data = json.loads(response.read().decode('utf-8'))
                meta = data['chart']['result'][0]['meta']
                price = meta.get('regularMarketPrice')
                return round(float(price), 2) if price else None
        except Exception:
            return None

    @staticmethod
    def calculate_pure_python_rsi(prices: List[float], period: int = 14) -> float:
        if len(prices) < period + 1:
            return 50.0
        gains, losses = [], []
        for i in range(1, len(prices)):
            change = prices[i] - prices[i - 1]
            if change > 0:
                gains.append(change)
                losses.append(0.0)
            else:
                gains.append(0.0)
                losses.append(abs(change))
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        if avg_loss == 0:
            return 100.0
        rs = avg_gain / avg_loss
        return round(100 - (100 / (1 + rs)), 2)
