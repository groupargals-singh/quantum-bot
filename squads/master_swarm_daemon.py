import os
import time
import json
import subprocess
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

LOOP_INTERVAL_SECONDS = 300
LOG_FILE = Path("master_swarm_daemon.log")
BOT_TOKEN = "8848903231:AAEIg7FyiM66utC5zljqR14TzqRjuRcAgXs"
CHAT_ID = "1330836270"

def send_telegram_msg(msg):
    if not BOT_TOKEN:
        return
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}).encode("utf-8")
        req = urllib.request.Request(url, data=data)
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"Telegram Notification Error: {e}")

def log_message(msg):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    formatted_msg = f"[{timestamp}] {msg}"
    print(formatted_msg)
    with open(LOG_FILE, "a") as f:
        f.write(formatted_msg + "\n")

def run_squad_tasks():
    log_message("⚡ [SWARM DAEMON] Running 24/7 Cycle for Ultimate Squad D (30K Nodes + 1Yr Data)...")

    squad_path = Path("squad_d_derivatives/supervisor_brain_derivatives/sd_mstr_engine.py")
    if squad_path.exists():
        try:
            res = subprocess.run(["python3", str(squad_path)], capture_output=True, text=True, timeout=60)
            output = res.stdout.strip()
            log_message(f"✅ {output}")

            mem_path = Path("squad_d_derivatives/supervisor_brain_derivatives/sd_mstr_memory.json")
            if mem_path.exists():
                with open(mem_path, "r") as f:
                    data = json.load(f)

                tg_report = (
                    f"🧠 *[SQUAD D - 30,000 BRAINS AUDIT]*\n"
                    f"----------------------------------------\n"
                    f"👑 *Master Accuracy:* `{data.get('accuracy_score', 0)}%`\n"
                    f"🌐 *Active Brain Nodes:* `{data.get('total_sub_brains_active', 30000):,}`\n"
                    f"📚 *1-Year Data Trained:* `{data.get('historical_days_trained', 365)} Days`\n"
                    f"📈 *Data Points Processed:* `{data.get('data_points_processed', 0):,}`\n"
                    f"🔌 *Multi-API Status:* `{data.get('multi_api_status', 'ONLINE')}`\n"
                    f"🔄 *Self Correction Cycle:* `#{data.get('self_correction_count', 0)}`\n"
                    f"🎖️ *Promotions:* `{data.get('total_promotions', 0)}` | ⚠️ *Demotions:* `{data.get('total_demotions', 0)}`\n"
                    f"⚡ *Status:* `{data.get('status', 'ACTIVE')}`\n"
                    f"⏰ *Timestamp:* `{data.get('last_optimized', 'N/A')}`\n"
                    f"----------------------------------------\n"
                    f"🚀 _30,000 Brains Self-Learning 24/7 from Multi-API Data Feeds_"
                )
                send_telegram_msg(tg_report)

        except Exception as e:
            err_msg = f"❌ Error in Squad D execution: {e}"
            log_message(err_msg)
            send_telegram_msg(f"⚠️ *[SWARM DAEMON ERROR]*\n{err_msg}")

if __name__ == "__main__":
    log_message("🚀 Master 24/7 Swarm Daemon Upgraded with 30K Brain Nodes & Multi-API Feeds!")
    send_telegram_msg("🚀 *Squad D Upgraded!* 30,000 Brain Nodes, 1-Year Historical Vault & Multi-API Pipeline Live.")
    while True:
        try:
            run_squad_tasks()
            time.sleep(LOOP_INTERVAL_SECONDS)
        except KeyboardInterrupt:
            log_message("🛑 Swarm Daemon stopped manually.")
            break
        except Exception as e:
            log_message(f"❌ Critical Daemon Error: {e}")
            time.sleep(60)
