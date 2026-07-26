import os
import time
from datetime import datetime, timedelta, timezone
import requests
import yfinance as yf
import pandas as pd
from core_bus.broker_and_notifier import InstitutionalBrokerAdapter

class QuantumMasterBot:
    def __init__(self):
        self.broker = InstitutionalBrokerAdapter()
        self.is_active = True
        self.last_update_id = 0
        self.positions = []
        self.token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()

    def clean_webhook(self):
        """Telegram Webhook clear karein taaki getUpdates sahi se kaam kare"""
        if self.token:
            try:
                url = f"https://api.telegram.org/bot{self.token}/deleteWebhook"
                requests.get(url, timeout=5)
                print("🧹 Telegram Webhook cleaned.")
            except Exception as e:
                print(f"⚠️ Webhook Cleanup Error: {e}")

    def send_startup_ping(self):
        """Bot start hote hi Telegram par alert bheje"""
        if self.token:
            print(f"🔑 Using Telegram Token: {self.token[:5]}...")
            self.broker.send_telegram_alert("🟢 *QUANTUM BOT IS NOW LIVE ON CLOUD!*\nSend `/status` to test connection.")
        else:
            print("❌ ERROR: TELEGRAM_BOT_TOKEN Environment Variable nahi mila!")

    def get_ist_time(self):
        utc_now = datetime.now(timezone.utc)
        return utc_now + timedelta(hours=5, minutes=30)

    def is_market_open(self):
        ist = self.get_ist_time()
        if ist.weekday() >= 5:
            return False
        market_start = ist.replace(hour=9, minute=15, second=0, microsecond=0)
        market_end = ist.replace(hour=15, minute=30, second=0, microsecond=0)
        return market_start <= ist <= market_end

    def check_telegram_commands(self):
        if not self.token:
            return
        
        try:
            url = f"https://api.telegram.org/bot{self.token}/getUpdates?offset={self.last_update_id + 1}&timeout=2"
            resp = requests.get(url, timeout=5).json()
            if resp.get("ok") and resp.get("result"):
                for update in resp["result"]:
                    self.last_update_id = update["update_id"]
                    msg = update.get("message", {})
                    text = msg.get("text", "").strip().lower()

                    print(f"📩 Telegram Command Received: {text}")

                    if text.startswith("/status"):
                        ist_str = self.get_ist_time().strftime("%Y-%m-%d %H:%M:%S IST")
                        mkt_status = "🟢 Open" if self.is_market_open() else "🔴 Closed (NSE)"
                        bot_status = "🟢 Running" if self.is_active else "⏸️ Paused"
                        reply = f"🤖 *QUANTUM BOT ENGINE STATUS*\n\n⏱ *IST Time:* `{ist_str}`\n📊 *NSE Market:* `{mkt_status}`\n⚙️ *Bot Engine:* `{bot_status}`\n💼 *Active Positions:* `{len(self.positions)}`"
                        self.broker.send_telegram_alert(reply)

                    elif text.startswith("/pnl"):
                        pnl_msg = f"📈 *QUANTUM LIVE P&L REPORT*\n\n🔢 *Active Positions:* {len(self.positions)}\n💰 *Realized P&L:* ₹0.00\n⚡ *Un-Realized P&L:* ₹0.00\n⚙️ *Mode:* `{self.broker.mode}`"
                        self.broker.send_telegram_alert(pnl_msg)

                    elif text.startswith("/stop"):
                        self.is_active = False
                        self.broker.send_telegram_alert("🛑 *EMERGENCY STOP TRIGGERED!*\nBot trading sequence paused.")

                    elif text.startswith("/start"):
                        self.is_active = True
                        self.broker.send_telegram_alert("▶️ *BOT RESTARTED!*\nTrading engine active again.")
        except Exception as e:
            print(f"⚠️ Telegram Listener Error: {e}")

    def calculate_signals(self, df):
        if len(df) < 25:
            return "NEUTRAL"
        
        df = df.copy()
        df['EMA9'] = df['Close'].ewm(span=9, adjust=False).mean()
        df['EMA21'] = df['Close'].ewm(span=21, adjust=False).mean()
        df['VWAP'] = (df['Volume'] * (df['High'] + df['Low'] + df['Close']) / 3).cumsum() / df['Volume'].cumsum()

        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))

        last = df.iloc[-1]
        prev = df.iloc[-2]

        ema_bullish = (prev['EMA9'] <= prev['EMA21']) and (last['EMA9'] > last['EMA21'])
        ema_bearish = (prev['EMA9'] >= prev['EMA21']) and (last['EMA9'] < last['EMA21'])

        if ema_bullish and float(last['Close']) > float(last['VWAP']) and (40 <= float(last['RSI']) <= 70):
            return "BUY"
        elif ema_bearish and float(last['Close']) < float(last['VWAP']):
            return "SELL"
        
        return "NEUTRAL"

    def run(self):
        print("🚀 Master Quantum Engine Booting Up...")
        self.clean_webhook()
        self.send_startup_ping()
        
        while True:
            self.check_telegram_commands()

            if self.is_active and self.is_market_open():
                try:
                    data = yf.download(tickers="RELIANCE.NS", period="1d", interval="5m", progress=False)
                    if not data.empty:
                        signal = self.calculate_signals(data)
                        if signal in ["BUY", "SELL"]:
                            price = float(data['Close'].iloc[-1])
                            self.broker.place_order("RELIANCE.NS", signal, 10, price)
                            self.positions.append({"symbol": "RELIANCE.NS", "action": signal, "price": price})
                except Exception as e:
                    print(f"Execution Error: {e}")
            
            time.sleep(5)
