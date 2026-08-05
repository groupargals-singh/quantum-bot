from src.strategies.backtester import QuantitativeBacktester

if __name__ == "__main__":
    backtester = QuantitativeBacktester(initial_capital=10000.0)
    
    # Testing Strategy on Top Assets
    backtester.run(symbol="BTCUSDT", interval="5m", limit=1000)
    backtester.run(symbol="ETHUSDT", interval="5m", limit=1000)
    backtester.run(symbol="SOLUSDT", interval="5m", limit=1000)
