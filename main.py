import os
import sys
import time
import threading
from flask import Flask, jsonify

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from core.event_bus import event_bus
from core.level2_engine import BinanceLevel2Engine

app = Flask(__name__)
l2_engine = BinanceLevel2Engine("btcusdt")

latest_l2_snapshot = {}

def l2_data_listener(data):
    global latest_l2_snapshot
    latest_l2_snapshot = data
    
    imb = data['imbalance']
    if imb > 0.35:
        print(f"🔥 [SQUAD M - WHALE BUY] Imbalance: +{imb} | Bid Vol: {data['bid_vol']} BTC")
    elif imb < -0.35:
        print(f"🚨 [SQUAD M - WHALE SELL] Imbalance: {imb} | Ask Vol: {data['ask_vol']} BTC")

event_bus.subscribe("level2_depth_update", l2_data_listener)

@app.route('/')
@app.route('/health')
def health_check():
    return jsonify({
        "status": "online",
        "system": "Quantum Bot - Phase 1 Engine",
        "event_bus": "Active (High-Speed)",
        "level2_stream": "Connected (100ms Feed)",
        "latest_orderbook_snapshot": latest_l2_snapshot
    }), 200

def start_phase1_engine():
    print("🚀 [QUANTUM ENGINE] Starting Phase 1 High-Speed Data Architecture...")
    time.sleep(2)
    l2_engine.start()

if __name__ == "__main__":
    engine_thread = threading.Thread(target=start_phase1_engine, daemon=True)
    engine_thread.start()

    port = int(os.environ.get("PORT", 10000))
    print(f"🌐 [RENDER SERVER] Listening on port {port}...")
    app.run(host="0.0.0.0", port=port)
