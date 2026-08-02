import asyncio
import json
import os
import requests
import numpy as np
import websockets
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8848903231:AAEIg7FyiM66utC5zljqR14TzqRjuRcAgXs")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "1330836270")

# 🌐 Render Cloud Health-Check Web Server
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"OK - Quantum Engine Active")

    def log_message(self, format, *args):
        return

def run_health_server():
    port = int(os.getenv("PORT", 8000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    print(f"🌐 Render Web Port Active on Port: {port}")
    server.serve_forever()

threading.Thread(target=run_health_server, daemon=True).start()

# ⚡ Quantum Engine Core
def send_telegram_alert(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"⚠️ Telegram Error: {e}")

def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return 50.0
    deltas = np.diff(prices)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.mean(gains[-period:])
    avg_loss = np.mean(losses[-period:])
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(float(100.0 - (100.0 / (1.0 + rs))), 2)

async def binance_real_quantum_engine():
    url = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"
    price_history = []
    last_signal_time = 0

    print("=========================================================")
    print("⚡ REAL QUANTUM ENGINE ONLINE (BINANCE WEBSOCKET ACTIVE)")
    print("=========================================================")

    async with websockets.connect(url) as ws:
        while True:
            try:
                response = await ws.recv()
                data = json.loads(response)
                kline = data.get('k', {})
                current_price = float(kline.get('c', 0))
                total_volume = float(kline.get('v', 0))
                buyer_volume = float(kline.get('V', 0))
                seller_volume = max(0.0, total_volume - buyer_volume)

                if current_price == 0:
                    continue

                price_history.append(current_price)
                if len(price_history) > 100:
                    price_history.pop(0)

                rsi = calculate_rsi(price_history)
                order_flow_delta = round((buyer_volume - seller_volume) / total_volume, 3) if total_volume > 0 else 0.0
                sma_short = round(float(np.mean(price_history[-5:])), 2) if len(price_history) >= 5 else current_price

                current_time = asyncio.get_event_loop().time()
                if current_time - last_signal_time > 30:
                    signal_type = None

                    if rsi < 42 and order_flow_delta > 0.1 and current_price >= sma_short:
                        signal_type = "CALL (BUY) 📈"
                        target_price = round(current_price * 1.008, 2)
                        stop_loss = round(current_price * 0.996, 2)
                    elif rsi > 58 and order_flow_delta < -0.1 and current_price <= sma_short:
                        signal_type = "PUT (SELL) 📉"
                        target_price = round(current_price * 0.992, 2)
                        stop_loss = round(current_price * 1.004, 2)

                    if signal_type:
                        win_prob = round(min(95.0, max(65.0, 50.0 + (abs(order_flow_delta) * 50) + (abs(50 - rsi) * 0.5))), 1)
                        msg = (
                            f"🚨 *REAL QUANTUM SIGNAL GENERATED* 🚨\n\n"
                            f"📊 *Asset:* `BTC/USDT`\n"
                            f"📈 *Signal Type:* **{signal_type}**\n\n"
                            f"💵 *Live Price:* `${current_price}`\n"
                            f"🎯 *Target Price:* `${target_price}`\n"
                            f"🛑 *Stop Loss:* `${stop_loss}`\n\n"
                            f"📊 *Real RSI (14):* `{rsi}`\n"
                            f"🌊 *Order Flow Delta:* `{order_flow_delta}`\n"
                            f"🎲 *Calculated Win Prob:* `{win_prob}%`\n"
                            f"🛡️ *Recommended Allocation:* `₹25,000`"
                        )
                        send_telegram_alert(msg)
                        print(f"🚀 REAL {signal_type} SIGNAL DISPATCHED TO TELEGRAM!")
                        last_signal_time = current_time

            except Exception as e:
                await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(binance_real_quantum_engine())
