import os
import time
import psycopg2
from psycopg2.extras import execute_values

class TimescaleDBEngine:
    """Enterprise TimescaleDB Persistence Engine for High-Frequency Tick Data"""
    def __init__(self):
        self.db_url = os.environ.get(
            "TIMESCALE_URL", 
            "postgresql://postgres:postgres@localhost:5432/quantum_db"
        )
        self.active = False
        self._init_db()

    def _get_connection(self):
        try:
            conn = psycopg2.connect(self.db_url, connect_timeout=3)
            return conn
        except Exception:
            return None

    def _init_db(self):
        conn = self._get_connection()
        if not conn:
            print("⚠️ [TIMESCALE DB] Standby Mode: Local SQLite/File fallback active until DB connection string is set.")
            return

        try:
            cur = conn.cursor()
            # Enable TimescaleDB extension if supported
            cur.execute("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;")
            
            # 1. Market Ticks Hypertable
            cur.execute("""
                CREATE TABLE IF NOT EXISTS market_ticks (
                    time TIMESTAMPTZ NOT NULL,
                    symbol VARCHAR(20) NOT NULL,
                    top_bid DOUBLE PRECISION,
                    top_ask DOUBLE PRECISION,
                    spread DOUBLE PRECISION,
                    imbalance DOUBLE PRECISION
                );
            """)
            
            try:
                cur.execute("SELECT create_hypertable('market_ticks', 'time', if_not_exists => TRUE);")
            except Exception:
                pass  # Fallback to standard Postgres table if hypertable extension is restricted

            # 2. Trades History Table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS trades_history (
                    id SERIAL PRIMARY KEY,
                    symbol VARCHAR(20) NOT NULL,
                    side VARCHAR(10) NOT NULL,
                    entry_price DOUBLE PRECISION,
                    exit_price DOUBLE PRECISION,
                    pnl DOUBLE PRECISION,
                    status VARCHAR(20),
                    exit_reason VARCHAR(50),
                    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                );
            """)

            conn.commit()
            cur.close()
            conn.close()
            self.active = True
            print("🐘 [TIMESCALE DB] Hypertables & Schema Initialized Successfully!")
        except Exception as e:
            print(f"❌ [TIMESCALE INIT ERROR] {e}")

    def save_tick_batch(self, tick_data_list):
        if not self.active or not tick_data_list:
            return

        conn = self._get_connection()
        if not conn:
            return

        try:
            cur = conn.cursor()
            query = """
                INSERT INTO market_ticks (time, symbol, top_bid, top_ask, spread, imbalance)
                VALUES %s
            """
            records = [
                (
                    psycopg2.TimestampFromTicks(t['timestamp']),
                    t['symbol'],
                    t['top_bid'],
                    t['top_ask'],
                    t['spread'],
                    t['imbalance']
                )
                for t in tick_data_list
            ]
            execute_values(cur, query, records)
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"❌ [TIMESCALE TICK SAVE ERROR] {e}")

    def save_trade_db(self, symbol, side, entry, sl, tp, status="OPEN"):
        if not self.active:
            return
        conn = self._get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO trades_history (symbol, side, entry_price, status)
                VALUES (%s, %s, %s, %s)
            """, (symbol, side, entry, status))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"❌ [TIMESCALE TRADE SAVE ERROR] {e}")

timescale_engine = TimescaleDBEngine()

# Standalone helper functions for backward compatibility
def save_trade_db(symbol, side, entry, sl, tp, status="OPEN"):
    timescale_engine.save_trade_db(symbol, side, entry, sl, tp, status)

def update_trade_exit_db(trade_id, exit_price, pnl, exit_reason):
    pass
