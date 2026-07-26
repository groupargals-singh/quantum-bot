import threading
import os
from web_terminal import app
from quantum_bot_main import QuantumMasterBot

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

def run_bot():
    bot = QuantumMasterBot()
    bot.run()

if __name__ == "__main__":
    print("🚀 Starting Unified Quantum Bot & Web Terminal on Cloud...")
    
    # Trading bot ko background thread me start karein
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Flask web server ko main thread par start karein
    run_flask()
