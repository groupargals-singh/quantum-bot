import os
import requests
from core.event_bus import event_bus
from core.risk_shield import risk_shield

class SquadMOrderflow:
    """Squad M: Real-time Orderbook Imbalance Engine"""
    def __init__(self):
        self.bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        self.last_signal_time = 0
        self.cooldown_seconds = 30  # Avoid alert spamming

        # Subscribe to Level-2 Depth Stream
        event_bus.subscribe("level2_depth_update", self.on_depth_update)

    def send_telegram_alert(self, signal_data):
        if not self.bot_token or not self.chat_id:
            print("⚠️ [SQUAD M] Telegram Credentials Missing in .env")
            return

        msg = (
            f"⚡ *INSTITUTIONAL QUANT SIGNAL* ⚡\n\n"
            f"🎯 *Symbol:* `{signal_data['symbol']}`\n"
            f"🚦 *Action:* `{signal_data['type']}`\n"
            f"💵 *Entry:* `${signal_data['entry']}`\n"
            f"🛑 *Stop Loss:* `${signal_data['stop_loss']}`\n"
            f"🎯 *Take Profit:* `${signal_data['take_profit']}`\n"
            f"📊 *RR Ratio:* `{signal_data['rr_ratio']}`\n"
            f"🛡️ *Risk Score:* `{signal_data['risk_score']}`\n\n"
            f"🧠 *Engine:* Squad M (Orderflow) + Squad P (Aladdin Shield)"
        )
        
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {"chat_id": self.chat_id, "text": msg, "parse_mode": "Markdown"}
            requests.post(url, json=payload, timeout=5)
            print(f"✅ [SQUAD M] Telegram Alert Sent for {signal_data['type']}!")
        except Exception as e:
            print(f"❌ [SQUAD M TELEGRAM ERROR] {e}")

    def on_depth_update(self, data):
        current_time = data['timestamp']
        if current_time - self.last_signal_time < self.cooldown_seconds:
            return

        imb = data['imbalance']
        price = data['top_ask'] if imb > 0 else data['top_bid']

        # Threshold Trigger: Imbalance > +0.35 (Buy) or < -0.35 (Sell)
        if imb > 0.35:
            valid, signal = risk_shield.validate_signal(data['symbol'], "BUY", price, imb)
            if valid:
                self.last_signal_time = current_time
                self.send_telegram_alert(signal)

        elif imb < -0.35:
            valid, signal = risk_shield.validate_signal(data['symbol'], "SELL", price, imb)
            if valid:
                self.last_signal_time = current_time
                self.send_telegram_alert(signal)

# Auto Initialize Squad M Listener
squad_m = SquadMOrderflow()
