import json
import time
import threading
import websocket
from core.event_bus import event_bus

class BinanceMultiLevel2Engine:
    """Binance L2 Depth Engine - Multi-Symbol Support (BTC, ETH, SOL)"""
    def __init__(self, symbols=["btcusdt", "ethusdt", "solusdt"]):
        self.symbols = [s.lower() for s in symbols]
        streams = "/".join([f"{s}@depth5@100ms" for s in self.symbols])
        self.ws_url = f"wss://stream.binance.com:9443/stream?streams={streams}"
        self.ws = None

    def on_message(self, ws, message):
        try:
            raw_data = json.loads(message)
            stream_name = raw_data.get("stream", "")
            data = raw_data.get("data", {})

            symbol = stream_name.split("@")[0].upper()
            bids = data.get("bids", [])
            asks = data.get("asks", [])

            if not bids or not asks:
                return

            top_bid = float(bids[0][0])
            top_ask = float(asks[0][0])
            bid_vol = sum(float(b[1]) for b in bids)
            ask_vol = sum(float(a[1]) for a in asks)

            # Level-2 Order Book Imbalance Calculation
            imbalance = round((bid_vol - ask_vol) / (bid_vol + ask_vol), 4)

            payload = {
                "symbol": symbol,
                "top_bid": top_bid,
                "top_ask": top_ask,
                "bid_vol": round(bid_vol, 3),
                "ask_vol": round(ask_vol, 3),
                "imbalance": imbalance,
                "spread": round(top_ask - top_bid, 4),
                "timestamp": time.time()
            }

            # Publish event with dynamic symbol
            event_bus.publish("level2_depth_update", payload)

        except Exception as e:
            print(f"❌ [MULTI-L2 ENGINE ERROR] {e}")

    def on_error(self, ws, error):
        print(f"⚠️ [L2 WS ERROR] {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("🔄 [L2 WS] Connection Closed. Reconnecting in 3s...")
        time.sleep(3)
        self.start()

    def start(self):
        def run():
            self.ws = websocket.WebSocketApp(
                self.ws_url,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )
            self.ws.run_forever()

        t = threading.Thread(target=run, daemon=True)
        t.start()
        print(f"📡 [MULTI-L2 ENGINE] Connected to Binance Multi-Stream for {self.symbols}")
