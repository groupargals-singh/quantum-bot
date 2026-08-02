import os
import sys
import time
import threading
from flask import Flask, jsonify

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from core.event_bus import event_bus
from core.level2_engine import BinanceLevel2Engine
import squads.squad_m_orderflow  # Load Squad M & Aladdin Risk Listener

app = Flask(__name__)
l2_engine = BinanceLevel2Engine("btcusdt")

latest_l2_snapshot = {}

def update_snapshot(data):
    global latest_l2_snapshot
    latest_l2_snapshot = data

event_bus.subscribe("level2_depth_update", update_snapshot)

@app.route('/')
@app.route('/health')
def health_check():
    return jsonify({
        "status": "online",
        "system": "Quantum Bot - Phase 2 Enterprise Core",
        "squad_m_orderflow": "Active",
        "squad_p_aladdin_risk": "Active",
        "latest_snapshot": latest_l2_snapshot
    }), 200

def start_phase2_engine():
    print("🚀 [QUANTUM BOT] Launching Phase 2 Multi-Agent Execution...")
    time.sleep(1)
    l2_engine.start()

if __name__ == "__main__":
    engine_thread = threading.Thread(target=start_phase2_engine, daemon=True)
    engine_thread.start()

    port = int(os.environ.get("PORT", 10000))
    print(f"🌐 [RENDER SERVER] Web Server Active on Port {port}...")
    app.run(host="0.0.0.0", port=port)
