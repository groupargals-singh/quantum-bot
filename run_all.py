import threading
import os
import time
import requests
from web_terminal import app
from quantum_bot_main import QuantumMasterBot

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

def run_bot():
    bot = QuantumMasterBot()
    bot.run()

def keep_alive():
    """Prevent Render Free Service from going to sleep"""
    render_url = os.environ.get("RENDER_EXTERNAL_URL")
    while True:
        time.sleep(600) # Ping every 10 minutes
        if render_url:
            try:
                requests.get(render_url, timeout=5)
                print("⏰ [KEEP-ALIVE] Self-ping successful. Server kept awake!")
            except Exception as e:
                print(f"⚠️ Keep-Alive Ping Failed: {e}")

if __name__ == "__main__":
    print("🚀 Starting Unified Quantum Bot & Web Terminal on Cloud...")
    
    # 1. Start Bot Thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # 2. Start Keep-Alive Thread
    ping_thread = threading.Thread(target=keep_alive, daemon=True)
    ping_thread.start()
    
    # 3. Start Web Terminal (Main Thread)
    run_flask()
