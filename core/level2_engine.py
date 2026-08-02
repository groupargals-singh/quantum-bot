import json
import time
import threading
import websocket
from core.event_bus import event_bus

class BinanceLevel2Engine:
    """Fetches 100ms Order Book Depth (Top 20 Bids/Asks) and computes Imbalance"""
    def __init__(self, symbol="btcusdt"):
        self.symbol = symbol.lower()
        self.ws_url = f"wss://stream.binance.com:9443/ws/{self.symbol}@depth20@100ms"
        self.is_running = False
        self.last_imbalance = 0.0

    def process_depth_data(self, data):
        try:
            bids = data.get('bids', [])
            asks = data.get('asks', [])

            if not bids or not asks:
                return

            total_bid_vol = sum(float(b[1]) for b in bids)
            total_ask_vol = sum(float(a[1]) for a in asks)

            denominator = total_bid_vol + total_ask_vol
            if denominator == 0:
                return

            imbalance = (total_bid_vol - total_ask_vol) / denominator
            self.last_imbalance = round(imbalance, 4)

            top_bid = float(bids[0][0])
            top_ask = float(asks[0][0])
            spread = round(top_ask - top_bid, 2)

            payload = {
                "symbol": self.symbol.upper(),
                "top_bid": top_bid,
                "top_ask": top_ask,
                "spread": spread,
                "bid_vol": round(total_bid_vol, 4),
                "ask_vol": round(total_ask_vol, 4),
                "imbalance": self.last_imbalance,
                "timestamp": time.time()
            }

            event_bus.publish("level2_depth_update", payload)

        except Exception as e:
            print(f"❌ [L2 ENGINE ERROR] Data Processing Failed: {e}")

    def _on_message(self, ws, message):
        data = json.loads(message)
        self.process_depth_data(data)

    def _on_error(self, ws, error):
        print(f"⚠️ [L2 WS ERROR] {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        print("🔴 [L2 WS] Depth Stream Connection Closed. Reconnecting in 3s...")
        time.sleep(3)
        if self.is_running:
            self.start()

    def start(self):
        self.is_running = True
        def run():
            while self.is_running:
                try:
                    ws = websocket.WebSocketApp(
                        self.ws_url,
                        on_message=self._on_message,
                        on_error=self._on_error,
                        on_close=self._on_close
                    )
                    ws.run_forever()
                except Exception as e:
                    print(f"❌ [L2 ENGINE EXCEPTION] {e}")
                    time.sleep(3)

        threading.Thread(target=run, daemon=True).start()
        print(f"⚡ [L2 ENGINE] Real-Time Level-2 Stream Connected for {self.symbol.upper()} (100ms)")
