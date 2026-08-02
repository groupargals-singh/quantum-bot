import os
import time
import threading
import requests
from core.state import system_state
from squads.squad_s_smart_executor import smart_executor

class SquadCCommandCenter:
    """Squad C: Interactive Telegram Controller & Remote Kill-Switch"""
    def __init__(self):
        self.bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        self.last_update_id = 0

    def start_polling(self):
        if not self.bot_token:
            print("⚠️ [SQUAD C] Telegram Bot Token Missing in .env")
            return

        def poll_loop():
            while True:
                try:
                    url = f"https://api.telegram.org/bot{self.bot_token}/getUpdates"
                    params = {"offset": self.last_update_id + 1, "timeout": 8}
                    response = requests.get(url, params=params, timeout=10)
                    data = response.json()

                    if data.get("ok"):
                        for update in data.get("result", []):
                            self.last_update_id = update["update_id"]
                            message = update.get("message", {})
                            text = message.get("text", "").strip()
                            chat_id = str(message.get("chat", {}).get("id"))

                            # Security: Verify Authorized Chat ID
                            if self.chat_id and chat_id != str(self.chat_id):
                                continue

                            self.handle_command(text)
                except Exception as e:
                    time.sleep(3)

        t = threading.Thread(target=poll_loop, daemon=True)
        t.start()
        print("🎮 [SQUAD C] Interactive Telegram Listener Online!")

    def send_msg(self, text):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        requests.post(url, json={"chat_id": self.chat_id, "text": text, "parse_mode": "Markdown"}, timeout=5)

    def handle_command(self, cmd):
        cmd = cmd.lower()
        if cmd in ["/start", "/help"]:
            msg = (
                "🤖 *QUANTUM BOT COMMAND CENTER*\n\n"
                "Available Controls:\n"
                "📊 `/pnl` - View Live Portfolio & Win Rate\n"
                "🎯 `/positions` - View Active Open Trades\n"
                "🛑 `/pause` - Activate Emergency Kill-Switch\n"
                "▶️ `/resume` - Resume Multi-Agent Signal Engine\n"
                "⚡ `/status` - Check Health & Trading State"
            )
            self.send_msg(msg)

        elif cmd == "/pnl":
            perf = smart_executor.get_performance_summary()
            msg = (
                "📈 *LIVE PERFORMANCE REPORT*\n\n"
                f"💵 *Balance:* `{perf['current_balance']}`\n"
                f"📊 *Total PnL:* `{perf['total_pnl']}`\n"
                f"🎯 *Win Rate:* `{perf['win_rate']}`\n"
                f"🔢 *Total Trades:* `{perf['total_trades']}`\n"
                f"⚡ *Active Trades:* `{perf['active_positions']}`"
            )
            self.send_msg(msg)

        elif cmd == "/positions":
            positions = smart_executor.positions
            if not positions:
                self.send_msg("ℹ️ *No active trades currently open.*")
                return

            msg = "📋 *ACTIVE OPEN POSITIONS*\n\n"
            for p in positions:
                msg += (
                    f"🔹 *{p['symbol']}* ({p['type']})\n"
                    f"  Entry: `${p['entry_price']}`\n"
                    f"  SL: `${p['stop_loss']}` | TP: `${p['take_profit']}`\n\n"
                )
            self.send_msg(msg)

        elif cmd == "/pause":
            system_state.is_paused = True
            self.send_msg("🚨 *EMERGENCY KILL-SWITCH ACTIVATED!* Signal generation and trade execution PAUSED.")

        elif cmd == "/resume":
            system_state.is_paused = False
            self.send_msg("✅ *TRADING RESUMED!* Multi-Agent Consensus Swarm is active.")

        elif cmd == "/status":
            state_str = "PAUSED 🛑" if system_state.is_paused else "ACTIVE 🟢"
            msg = (
                "⚡ *QUANTUM BOT SYSTEM STATUS*\n\n"
                f"⚙️ *Trading State:* `{state_str}`\n"
                f"🛰️ *Engine:* Phase 7 Command Swarm\n"
                f"📊 *Open Positions:* `{len(smart_executor.positions)}`"
            )
            self.send_msg(msg)

command_center = SquadCCommandCenter()
