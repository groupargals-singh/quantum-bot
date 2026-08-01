import requests
import config

class TelegramControlCenter:
    def __init__(self, aladdin_shield, paper_engine):
        self.token = config.TELEGRAM_TOKEN
        self.chat_id = config.TELEGRAM_CHAT_ID
        self.shield = aladdin_shield
        self.paper = paper_engine
        self.last_update_id = 0

    def send_alert(self, message: str):
        if self.token == "YOUR_BOT_TOKEN_HERE":
            print(f"[TELEGRAM SIMULATION]: {message}")
            return
        
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        try:
            requests.post(url, json={"chat_id": self.chat_id, "text": message}, timeout=5)
        except Exception as e:
            print(f"[TELEGRAM ERROR] Failed to send message: {e}")

    def poll_commands(self):
        if self.token == "YOUR_BOT_TOKEN_HERE":
            return

        url = f"https://api.telegram.org/bot{self.token}/getUpdates?offset={self.last_update_id + 1}&timeout=2"
        try:
            resp = requests.get(url, timeout=5).json()
            for update in resp.get("result", []):
                self.last_update_id = update["update_id"]
                msg = update.get("message", {})
                text = msg.get("text", "")
                
                if text:
                    reply = self.handle_command(text)
                    self.send_alert(reply)
        except Exception:
            pass

    def handle_command(self, command: str) -> str:
        cmd = command.strip().lower()
        if cmd == "/status":
            status = "PAUSED 🛑" if self.shield.is_kill_switch_active else "ACTIVE 🟢"
            mode = "Paper Mode 📝" if config.PAPER_TRADING else "Live Execution ⚡"
            return f"🤖 Quantum Bot Status:\n• State: {status}\n• Mode: {mode}"
        elif cmd == "/pnl":
            return f"📊 P&L Metrics:\n• Daily PnL: ₹{self.shield.daily_pnl}\n• Virtual Funds: ₹{self.paper.capital}"
        elif cmd == "/close_all":
            self.shield.trigger_kill_switch("Manual Emergency Close via Telegram")
            return "🚨 EMERGENCY: All positions closed and Kill-Switch activated!"
        else:
            return "❓ Unknown command. Try: /status, /pnl, or /close_all"
