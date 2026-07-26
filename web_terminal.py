import threading
import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>🚀 Quantum Bot Server is Active & Running Live!</h1>"

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "Quantum Bot"})

# Bot ko background thread me start karne ka system
def launch_bot():
    try:
        from quantum_bot_main import QuantumMasterBot
        bot = QuantumMasterBot()
        bot.run()
    except Exception as e:
        print(f"⚠️ Bot Thread Error: {e}")

# Web server start hote hi bot background me chalao
bot_thread = threading.Thread(target=launch_bot, daemon=True)
bot_thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
