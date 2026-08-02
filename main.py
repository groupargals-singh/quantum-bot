import os
import sys
import time
import threading
from flask import Flask, jsonify

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from core.event_bus import event_bus
from core.level2_engine import BinanceLevel2Engine
import squads.squad_t_master_commander
from squads.squad_s_smart_executor import smart_executor

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
        "system": "Quantum Bot - Phase 4 Live Trading Engine",
        "master_commander": "Squad T Active",
        "smart_execution": "Squad S Active (Paper Trading)",
        "performance_summary": smart_executor.get_performance_summary(),
        "latest_snapshot": latest_l2_snapshot
    }), 200

def start_phase4_engine():
    print("🚀 [QUANTUM BOT] Launching Phase 4 Automated Execution & Performance Engine...")
    time.sleep(1)
    l2_engine.start()

if __name__ == "__main__":
    engine_thread = threading.Thread(target=start_phase4_engine, daemon=True)
    engine_thread.start()

    port = int(os.environ.get("PORT", 10000))
    print(f"🌐 [RENDER SERVER] Listening on Port {port}...")
    app.run(host="0.0.0.0", port=port)
