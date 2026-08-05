import sqlite3
import os
import time

DB_FILE = "quantum_system.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Trades Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            type TEXT,
            entry_price REAL,
            exit_price REAL,
            stop_loss REAL,
            take_profit REAL,
            pnl REAL,
            reason TEXT,
            status TEXT,
            timestamp REAL
        )
    ''')
    
    # Signals Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            type TEXT,
            score REAL,
            entry REAL,
            stop_loss REAL,
            take_profit REAL,
            timestamp REAL
        )
    ''')
    
    conn.commit()
    conn.close()

def save_trade_db(symbol, trade_type, entry, sl, tp, status="OPEN", exit_p=0.0, pnl=0.0, reason=""):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO trades (symbol, type, entry_price, exit_price, stop_loss, take_profit, pnl, reason, status, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (symbol, trade_type, entry, exit_p, sl, tp, pnl, reason, status, time.time()))
    conn.commit()
    conn.close()

def update_trade_exit_db(trade_id, exit_p, pnl, reason):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE trades
        SET exit_price = ?, pnl = ?, reason = ?, status = 'CLOSED'
        WHERE id = ?
    ''', (exit_p, pnl, reason, trade_id))
    conn.commit()
    conn.close()

# Auto Init DB
init_db()
