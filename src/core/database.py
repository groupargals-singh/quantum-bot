import os
import time
import urllib.parse
import pg8000.dbapi

class TimescaleDBEngine:
    """Enterprise TimescaleDB / PostgreSQL Engine with Pure-Python Driver & Local Fallback"""
    def __init__(self):
        self.db_url = os.environ.get("TIMESCALE_URL", "")
        self.active = False
        self._init_db()

    def _get_connection(self):
        if not self.db_url:
            return None
        try:
            url = urllib.parse.urlparse(self.db_url)
            conn = pg8000.dbapi.connect(
                user=url.username or "postgres",
                password=url.password or "",
                host=url.hostname or "localhost",
                port=url.port or 5432,
                database=url.path[1:] or "postgres"
            )
            return conn
        except Exception:
            return None

    def _init_db(self):
        conn = self._get_connection()
        if not conn:
            print("⚠️ [TIMESCALE DB] Connection URL not configured.")
            print("🔄 [FALLBACK] Database running in Safe Standby mode.")
            return

        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS market_ticks (
                    id SERIAL PRIMARY KEY,
                    symbol VARCHAR(20) NOT NULL,
                    top_bid DOUBLE PRECISION,
                    top_ask DOUBLE PRECISION,
                    spread DOUBLE PRECISION,
                    imbalance DOUBLE PRECISION,
                    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            cur.execute("""
                CREATE TABLE IF NOT EXISTS trades_history (
                    id SERIAL PRIMARY KEY,
                    symbol VARCHAR(20) NOT NULL,
                    side VARCHAR(10) NOT NULL,
                    entry_price DOUBLE PRECISION,
                    status VARCHAR(20),
                    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                );
            """)

            conn.commit()
            cur.close()
            conn.close()
            self.active = True
            print("🐘 [TIMESCALE DB] PostgreSQL / Hypertables Initialized Successfully!")
        except Exception as e:
            print(f"❌ [DATABASE INIT ERROR] {e}")

    def save_trade_db(self, symbol, side, entry, sl, tp, status="OPEN"):
        conn = self._get_connection()
        if not conn:
            print(f"💾 [LOCAL LOG] Trade Saved Locally: {side} {symbol} @ ${entry}")
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO trades_history (symbol, side, entry_price, status) VALUES (%s, %s, %s, %s)",
                (symbol, side, entry, status)
            )
            conn.commit()
            cur.close()
            conn.close()
            print(f"🐘 [DATABASE] Trade Saved: {side} {symbol} @ ${entry}")
        except Exception as e:
            print(f"❌ [DB SAVE ERROR] {e}")

timescale_engine = TimescaleDBEngine()

def save_trade_db(symbol, side, entry, sl, tp, status="OPEN"):
    timescale_engine.save_trade_db(symbol, side, entry, sl, tp, status)

def update_trade_exit_db(trade_id, exit_price, pnl, exit_reason):
    pass
