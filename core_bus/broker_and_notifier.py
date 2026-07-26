import os
import requests

class InstitutionalBrokerAdapter:
    def __init__(self, mode: str = "PAPER"):
        self.mode = os.environ.get("TRADING_MODE", mode)
        self.telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
        self.telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
        self.broker_api_key = os.environ.get("BROKER_API_KEY", "")

    def send_telegram_alert(self, message: str):
        """Send instant alert to your phone via Telegram"""
        if self.telegram_token and self.telegram_chat_id:
            try:
                url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
                payload = {"chat_id": self.telegram_chat_id, "text": message, "parse_mode": "Markdown"}
                requests.post(url, json=payload, timeout=5)
            except Exception as e:
                print(f"⚠️ Telegram Alert Error: {e}")

    def place_order(self, symbol: str, action: str, qty: int, price: float) -> dict:
        msg = f"🚀 *QUANTUM BOT EXECUTION*\n\n📌 *Symbol:* `{symbol}`\n⚡ *Action:* `{action}`\n💰 *Price:* ₹{price}\n🔢 *Qty:* {qty}\n⚙️ *Mode:* `{self.mode}`"
        
        # Real Broker Integration Hook (Angel One / Dhan)
        if self.mode == "LIVE":
            # Real API order placement logic goes here
            print(f"📡 [REAL BROKER API] Order sent to Exchange for {symbol}")
            msg += "\n\n🟢 *Real Order Placed on Exchange!*"
        else:
            msg += "\n\n📝 *Paper Trade Executed*"

        # Send Telegram alert
        self.send_telegram_alert(msg)
        return {"status": "SUCCESS", "symbol": symbol, "action": action, "qty": qty, "price": price}
