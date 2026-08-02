import os
import sys
import time
import threading
from flask import Flask, jsonify, render_template_string

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from core.event_bus import event_bus
from core.level2_engine import BinanceMultiLevel2Engine
from core.state import system_state
import squads.squad_t_master_commander
from squads.squad_s_smart_executor import smart_executor
from squads.squad_c_command_center import command_center
from squads.squad_m_monitor import system_monitor

app = Flask(__name__)
l2_engine = BinanceMultiLevel2Engine(["btcusdt", "ethusdt", "solusdt"])

multi_snapshots = {}

def update_multi_snapshots(data):
    symbol = data['symbol']
    multi_snapshots[symbol] = data
    system_monitor.update_tick(data['timestamp'])

event_bus.subscribe("level2_depth_update", update_multi_snapshots)

HTML_DASHBOARD = """
<!DOCTYPE html>
<html>
<head>
    <title>Quantum Bot - Enterprise Terminal</title>
    <meta http-equiv="refresh" content="2">
    <style>
        body { background: #0a0e17; color: #d1d5db; font-family: 'Segoe UI', Tahoma, sans-serif; margin: 0; padding: 20px; }
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1f293d; padding-bottom: 15px; }
        .title { color: #00f2fe; font-size: 24px; font-weight: bold; }
        .status-badge { background: #059669; color: #fff; padding: 5px 12px; border-radius: 20px; font-size: 14px; }
        .status-paused { background: #dc2626; color: #fff; padding: 5px 12px; border-radius: 20px; font-size: 14px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 20px; }
        .card { background: #111827; border: 1px solid #1f293d; border-radius: 10px; padding: 15px; }
        .card-title { font-size: 12px; color: #9ca3af; text-transform: uppercase; }
        .card-value { font-size: 22px; font-weight: bold; margin-top: 5px; color: #f9fafb; }
        .green { color: #10b981; }
        .red { color: #ef4444; }
        .cyan { color: #06b6d4; }
        .table-container { margin-top: 25px; background: #111827; border-radius: 10px; padding: 15px; border: 1px solid #1f293d; }
        table { width: 100%; border-collapse: collapse; text-align: left; }
        th, td { padding: 12px; border-bottom: 1px solid #1f293d; font-size: 14px; }
        th { color: #6b7280; }
    </style>
</head>
<body>
    <div class="header">
        <div class="title">⚡ QUANTUM BOT | Enterprise Swarm</div>
        {% if is_paused %}
        <div class="status-paused">SYSTEM PAUSED 🛑</div>
        {% else %}
        <div class="status-badge">AUTO-HEALING ACTIVE 🟢</div>
        {% endif %}
    </div>

    <div class="grid">
        <div class="card">
            <div class="card-title">Current Balance</div>
            <div class="card-value cyan">{{ perf.current_balance }}</div>
        </div>
        <div class="card">
            <div class="card-title">Total PnL</div>
            <div class="card-value {% if '-' in perf.total_pnl %}red{% else %}green{% endif %}">{{ perf.total_pnl }}</div>
        </div>
        <div class="card">
            <div class="card-title">Win Rate</div>
            <div class="card-value green">{{ perf.win_rate }}</div>
        </div>
        <div class="card">
            <div class="card-title">Active Positions</div>
            <div class="card-value cyan">{{ perf.active_positions }}</div>
        </div>
        <div class="card">
            <div class="card-title">Stream Latency</div>
            <div class="card-value green">{{ latency }} ms</div>
        </div>
    </div>

    <div class="table-container">
        <h3 style="margin-top:0; color:#00f2fe;">📊 Live Orderbook Depth Stream</h3>
        <table>
            <tr>
                <th>Symbol</th>
                <th>Top Bid</th>
                <th>Top Ask</th>
                <th>Spread</th>
                <th>Imbalance</th>
            </tr>
            {% for symbol, snap in snaps.items() %}
            <tr>
                <td><b>{{ symbol }}</b></td>
                <td class="green">${{ snap.top_bid }}</td>
                <td class="red">${{ snap.top_ask }}</td>
                <td>${{ snap.spread }}</td>
                <td class="{% if snap.imbalance > 0 %}green{% else %}red{% endif %}"><b>{{ snap.imbalance }}</b></td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    perf = smart_executor.get_performance_summary()
    return render_template_string(
        HTML_DASHBOARD, 
        perf=perf, 
        snaps=multi_snapshots, 
        is_paused=system_state.is_paused,
        latency=system_monitor.latency_ms
    )

@app.route('/health')
def health_check():
    return jsonify({
        "status": "online",
        "paused": system_state.is_paused,
        "latency_ms": system_monitor.latency_ms,
        "performance": smart_executor.get_performance_summary(),
        "snaps": multi_snapshots
    }), 200

def start_phase8_engine():
    print("🚀 [QUANTUM BOT] Launching Phase 8 Enterprise Architecture...")
    command_center.start_polling()
    system_monitor.start_keep_alive()
    time.sleep(1)
    l2_engine.start()

if __name__ == "__main__":
    engine_thread = threading.Thread(target=start_phase8_engine, daemon=True)
    engine_thread.start()

    port = int(os.environ.get("PORT", 10000))
    print(f"🌐 [RENDER SERVER] Listening on Port {port}...")
    app.run(host="0.0.0.0", port=port)
