import json
import time
import threading
import websocket
from src.core.event_bus import event_bus

class BinanceMultiLevel2Engine:
    def __init__(self, symbols=None):
        if symbols is None:
            self.symbols = ["btcusdt", "ethusdt", "solusdt"]
        else:
            self.symbols = [s.lower() for s in symbols]
        
        stream_names = "/".join([f"{s}@depth20@100ms" for s in self.symbols])
        self.ws_url = f"wss://stream.binance.com:9443/ws/{stream_names}"
        self.ws = None

    def on_message(self, ws, message):
        data = json.loads(message)
        if 's' in data and 'bids' in data and 'asks' in data:
            symbol = data['s'].upper()
            bids = data['bids']
            asks = data['asks']
            
            if not bids or not asks:
                return

            top_bid = float(bids[0][0])
            top_ask = float(asks[0][0])
            bid_vol = sum([float(b[1]) for b in bids[:5]])
            ask_vol = sum([float(a[1]) for a in asks[:5]])
            
            total_vol = bid_vol + ask_vol
            imbalance = (bid_vol - ask_vol) / total_vol if total_vol > 0 else 0.0

            snapshot = {
                "symbol": symbol,
                "top_bid": top_bid,
                "top_ask": top_ask,
                "spread": round(top_ask - top_bid, 4),
                "imbalance": round(imbalance, 4),
                "timestamp": time.time()
            }

            event_bus.publish("level2_depth_update", snapshot)

    def on_error(self, ws, error):
        print(f"⚠️ [L2 ENGINE ERROR] {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("🔌 [L2 ENGINE] Connection closed. Reconnecting in 3s...")
        time.sleep(3)
        self.start()

    def on_open(self, ws):
        print(f"🟢 [L2 ENGINE] Binance L2 Depth Stream Connected ({', '.join(self.symbols).upper()})")

    def start(self):
        def run():
            self.ws = websocket.WebSocketApp(
                self.ws_url,
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )
            self.ws.run_forever()

        t = threading.Thread(target=run, daemon=True)
        t.start()
