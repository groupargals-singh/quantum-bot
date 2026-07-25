import time
import os
import logging
from dotenv import load_dotenv
import yfinance as yf
from typing import Callable, List, Dict, Any

# Suppress Yahoo Finance error spam & warnings
logging.getLogger('yfinance').setLevel(logging.CRITICAL)

class MultiFeedManager:
    """
    Unified Data Feed Switchboard:
    Cleans stock ticks and routes them to Quantum Bot Data Filter.
    """
    def __init__(self, on_tick_callback: Callable[[str, float, int], None]):
        load_dotenv()
        self.data_source = os.getenv("DATA_SOURCE", "YAHOO").upper()
        self.on_tick_callback = on_tick_callback
        
        # Valid Active Nifty Top Stocks
        default_symbols = "RELIANCE.NS,TCS.NS,INFY.NS,HDFCBANK.NS,SBIN.NS,ICICIBANK.NS,BHARTIARTL.NS,AXISBANK.NS"
        raw_symbols = os.getenv("YAHOO_SYMBOLS", default_symbols)
        self.symbols = [s.strip() for s in raw_symbols.split(",") if s.strip()]

    def start_feed(self, iterations: int = 3):
        """Starts multi-stock stream without error noise."""
        clean_names = [s.replace('.NS', '') for s in self.symbols]
        print(f"📡 [DATA FEED] Active Source: {self.data_source}")
        print(f"📋 [WATCHLIST - {len(clean_names)} STOCKS]: {', '.join(clean_names)}\n")
        
        self._fetch_yahoo_batch_ticks(iterations)

    def _fetch_yahoo_batch_ticks(self, count: int):
        """Fetch real-time price snapshot for watchlist."""
        for i in range(count):
            print(f"--- 🔄 Live Market Scan #{i+1} ---")
            for symbol in self.symbols:
                try:
                    ticker = yf.Ticker(symbol)
                    fast_info = ticker.fast_info
                    price = round(fast_info.get('lastPrice', 0.0), 2)
                    volume = int(fast_info.get('lastVolume', 1000))
                    
                    if price > 0:
                        clean_symbol = symbol.replace(".NS", "")
                        self.on_tick_callback(clean_symbol, price, volume)
                except Exception:
                    continue
            time.sleep(1)
