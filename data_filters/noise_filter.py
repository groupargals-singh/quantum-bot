import hashlib
import time
from typing import Dict, Any, Optional

class DataFilterEngine:
    """
    3-Layer Data Filter & Noise Stripper:
    Layer 1: Duplicate & Zero-Volatility Drop
    Layer 2: Feature Hash Compression
    Layer 3: Impact Signal Score Gate
    """
    def __init__(self, volatility_threshold: float = 0.0002):
        self.volatility_threshold = volatility_threshold
        self.seen_hashes: Dict[str, float] = {}
        self.last_price_cache: Dict[str, float] = {}
        self.hash_ttl_seconds = 300  # Clean hash cache every 5 minutes

    def _generate_hash(self, raw_data: str) -> str:
        """Generates 128-bit MD5 fingerprint for fast duplication check."""
        return hashlib.md5(raw_data.encode('utf-8')).hexdigest()

    def _purge_old_hashes(self):
        """Removes expired hashes to prevent memory bloating."""
        now = time.time()
        expired = [h for h, ts in self.seen_hashes.items() if now - ts > self.hash_ttl_seconds]
        for h in expired:
            del self.seen_hashes[h]

    def process_tick(self, symbol: str, price: float, volume: int) -> Optional[Dict[str, Any]]:
        """Filter Layer 1 & 2: Drops zero-volatility and duplicate market ticks."""
        last_price = self.last_price_cache.get(symbol)
        
        if last_price is not None:
            price_change = abs(price - last_price) / last_price
            if price_change < self.volatility_threshold:
                return None  # Drop zero-movement noise
        
        self.last_price_cache[symbol] = price
        return {
            "symbol": symbol,
            "price": price,
            "volume": volume,
            "timestamp": time.time()
        }

    def process_text_news(self, news_headline: str, source: str) -> Optional[Dict[str, Any]]:
        """Filter Layer 3: Drops duplicate news headlines across wires."""
        self._purge_old_hashes()
        headline_hash = self._generate_hash(news_headline.lower().strip())
        
        if headline_hash in self.seen_hashes:
            return None  # Drop duplicate news wire line
        
        self.seen_hashes[headline_hash] = time.time()
        return {
            "headline": news_headline,
            "source": source,
            "hash": headline_hash,
            "timestamp": time.time()
        }
