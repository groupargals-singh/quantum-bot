import sqlite3
from datetime import datetime

class QuantumDatabase:
    def __init__(self, db_name="quantum_bot.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                symbol TEXT,
                action TEXT,
                price REAL,
                quantity INTEGER,
                pnl REAL,
                status TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def log_trade(self, symbol: str, action: str, price: float, quantity: int, pnl: float = 0.0, status: str = "OPEN"):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO trades (timestamp, symbol, action, price, quantity, pnl, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (now, symbol, action, price, quantity, pnl, status))
        conn.commit()
        conn.close()
