import threading
import os
import time
import requests
from web_terminal import app
from quantum_bot_main import QuantumMasterBot

def run_bot():
    try:
        bot = QuantumMasterBot()
        bot.run()
    except Exception as e:
        print(f"⚠️ Bot Thread Error: {e}")

def keep_alive():
    render_url = os.environ.get("RENDER_EXTERNAL_URL")
    while True:
        time.sleep(600)
        if render_url:
            try:
                requests.get(render_url, timeout=5)
                print("⏰ [KEEP-ALIVE] Ping successful.")
            except Exception as e:
                print(f"⚠️ Ping Error: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Starting Unified Quantum Bot on Port: {port}")
    
    # 1. Start Bot Thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # 2. Start Keep-Alive Thread
    ping_thread = threading.Thread(target=keep_alive, daemon=True)
    ping_thread.start()
    
    # 3. Start Web Server
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
