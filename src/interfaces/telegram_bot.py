import os
import time
import requests
import threading
from src.core.state import system_state
from src.execution.smart_executor import smart_executor

class CommandCenter:
    """Telegram Bot Command & Emergency Kill-Switch Interface"""
    def __init__(self):
        self.bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        self.last_update_id = 0

    def send_telegram_message(self, text):
        if not self.bot_token or not self.chat_id:
            return
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": text, "parse_mode": "Markdown"}
        try:
            requests.post(url, json=payload, timeout=5)
        except Exception as e:
            print(f"❌ [COMMAND CENTER MSG ERROR] {e}")

    def handle_command(self, text):
        cmd = text.strip().lower()

        if cmd == "/start" or cmd == "/help":
            msg = (
                "🤖 *QUANTUM ENGINE COMMAND CENTER*\n\n"
                "Available Commands:\n"
                "🔹 `/status` - Check Engine Health & System State\n"
                "🔹 `/pnl` - View Live Portfolio Balance & Win-Rate\n"
                "🔹 `/pause` - Emergency Kill-Switch (Stop Trading)\n"
                "🔹 `/resume` - Reactivate Trading Engine"
            )
            self.send_telegram_message(msg)

        elif cmd == "/status":
            state_str = "PAUSED 🛑" if system_state.is_paused else "ACTIVE 🟢"
            msg = f"⚙️ *SYSTEM STATUS:* `{state_str}`"
            self.send_telegram_message(msg)

        elif cmd == "/pnl":
            summary = smart_executor.get_performance_summary()
            msg = (
                "📊 *QUANTUM PORTFOLIO SUMMARY*\n\n"
                f"💵 *Initial Capital:* `{summary['initial_capital']}`\n"
                f"💰 *Current Balance:* `{summary['current_balance']}`\n"
                f"📈 *Total PnL:* `{summary['total_pnl']}`\n"
                f"🎯 *Win Rate:* `{summary['win_rate']}`\n"
                f"🔢 *Total Trades:* `{summary['total_trades']}`\n"
                f"⚡ *Active Positions:* `{summary['active_positions']}`"
            )
            self.send_telegram_message(msg)

        elif cmd == "/pause":
            system_state.is_paused = True
            self.send_telegram_message("🛑 *EMERGENCY KILL-SWITCH ACTIVATED!* System is now PAUSED.")

        elif cmd == "/resume":
            system_state.is_paused = False
            self.send_telegram_message("🟢 *SYSTEM RESUMED!* Trading engine is back online.")

    def poll_updates(self):
        if not self.bot_token:
            return

        url = f"https://api.telegram.org/bot{self.bot_token}/getUpdates"
        params = {"offset": self.last_update_id + 1, "timeout": 10}

        try:
            res = requests.get(url, params=params, timeout=12)
            if res.status_code == 200:
                data = res.json()
                if "result" in data:
                    for update in data["result"]:
                        self.last_update_id = update["update_id"]
                        if "message" in update and "text" in update["message"]:
                            text = update["message"]["text"]
                            sender_chat_id = str(update["message"]["chat"]["id"])
                            if self.chat_id and sender_chat_id == str(self.chat_id):
                                self.handle_command(text)
        except Exception as e:
            pass

    def start_polling(self):
        if not self.bot_token or not self.chat_id:
            print("⚠️ [COMMAND CENTER] TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID missing. Polling skipped.")
            return

        def loop():
            print("🎮 [COMMAND CENTER] Interactive Telegram Control Online!")
            while True:
                self.poll_updates()
                time.sleep(1)

        t = threading.Thread(target=loop, daemon=True)
        t.start()

command_center = CommandCenter()
