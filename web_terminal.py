from flask import Flask, render_template_string, jsonify
import sqlite3

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚡ QUANTUM BOT | Institutional Terminal</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #0b0e14; color: #c9d1d9; font-family: 'Segoe UI', monospace; }
        .card-custom { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 15px; margin-bottom: 15px; }
        .metric-val { font-size: 1.4rem; font-weight: bold; color: #58a6ff; }
        .text-green { color: #3fb950; }
        .text-red { color: #f85149; }
    </style>
</head>
<body class="p-3">
    <div class="container-fluid">
        <div class="row text-center mb-3">
            <div class="col-md-3 col-6"><div class="card-custom"><div>💰 CAPITAL</div><div class="metric-val">₹87,220.00</div></div></div>
            <div class="col-md-3 col-6"><div class="card-custom"><div>🎯 SCOPE</div><div class="metric-val text-green">NIFTY 50</div></div></div>
            <div class="col-md-3 col-6"><div class="card-custom"><div>📊 ENGINE</div><div class="metric-val text-green">GREEKS + RSI</div></div></div>
            <div class="col-md-3 col-6"><div class="card-custom"><div>🛡️ ALADDIN</div><div class="metric-val text-green">ACTIVE</div></div></div>
        </div>
        <div class="row">
            <div class="col-12">
                <div class="card-custom">
                    <h6 class="text-warning mb-3">📋 NIFTY 50 LIVE TRADES HISTORY</h6>
                    <div class="table-responsive">
                        <table class="table table-dark table-hover text-center align-middle m-0">
                            <thead>
                                <tr class="text-secondary">
                                    <th>TIME</th><th>SYMBOL</th><th>ACTION</th><th>PRICE</th><th>QTY</th><th>STATUS</th>
                                </tr>
                            </thead>
                            <tbody id="tradesTable"></tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script>
        function fetchDatabaseState() {
            fetch('/api/db_trades')
                .then(res => res.json())
                .then(trades => {
                    let html = '';
                    trades.forEach(t => {
                        let actionClass = t[3] === 'BUY' ? 'text-green' : 'text-red';
                        html += `<tr>
                            <td class="text-secondary">${t[1]}</td>
                            <td class="fw-bold">${t[2]}</td>
                            <td class="${actionClass} fw-bold">${t[3]}</td>
                            <td>₹${t[4]}</td>
                            <td>${t[5]}</td>
                            <td><span class="badge bg-secondary">${t[7]}</span></td>
                        </tr>`;
                    });
                    document.getElementById('tradesTable').innerHTML = html || '<tr><td colspan="6" class="text-secondary">Scanning...</td></tr>';
                });
        }
        setInterval(fetchDatabaseState, 2000);
        fetchDatabaseState();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/db_trades')
def db_trades():
    try:
        conn = sqlite3.connect('quantum_bot.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM trades ORDER BY id DESC LIMIT 10")
        rows = cursor.fetchall()
        conn.close()
        return jsonify(rows)
    except Exception:
        return jsonify([])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
