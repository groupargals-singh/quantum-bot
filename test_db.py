from src.core.database import save_trade_db

print("🚀 --- TESTING TIMESCALEDB / POSTGRESQL ENGINE --- 🚀\n")

save_trade_db(
    symbol="BTCUSDT",
    side="BUY",
    entry=65000.0,
    sl=64000.0,
    tp=67000.0,
    status="OPEN_PAPER"
)

print("\n🎉 Database Module Test Complete!")
