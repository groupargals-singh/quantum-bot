import os
from src.execution.binance_live_api import binance_live_api

if __name__ == "__main__":
    print("🔑 Testing HMAC-SHA256 Signature Connection...")
    balance = binance_live_api.get_account_balance("USDT")
    print(f"💼 Account Balance Response: {balance}")
