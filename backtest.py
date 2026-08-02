import requests
import pandas as pd
import numpy as np

def run_quantitative_backtest(symbol="BTCUSDT", limit=1000):
    print("\n=========================================================")
    print(f"⏳ RUNNING QUANTITATIVE BACKTEST: {symbol} ({limit} CANDLES)")
    print("=========================================================")
    
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit={limit}"
    raw_data = requests.get(url).json()

    df = pd.DataFrame(raw_data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_vol', 'trades', 'taker_buy_base', 'taker_buy_quote', 'ignore'
    ])

    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)
    df['taker_buy'] = df['taker_buy_base'].astype(float)
    df['seller_vol'] = df['volume'] - df['taker_buy']
    df['order_flow_delta'] = (df['taker_buy'] - df['seller_vol']) / df['volume']

    # Vectorized RSI (14 Period)
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['rsi'] = 100 - (100 / (1 + rs))

    trades = []
    position = None

    for i in range(20, len(df)):
        price = df['close'].iloc[i]
        rsi = df['rsi'].iloc[i]
        delta_val = df['order_flow_delta'].iloc[i]

        if position is None:
            if rsi < 42 and delta_val > 0.1:
                position = {'type': 'BUY', 'entry': price, 'tp': price * 1.008, 'sl': price * 0.996}
            elif rsi > 58 and delta_val < -0.1:
                position = {'type': 'SELL', 'entry': price, 'tp': price * 0.992, 'sl': price * 1.004}
        else:
            if position['type'] == 'BUY':
                if price >= position['tp']:
                    trades.append(1)
                    position = None
                elif price <= position['sl']:
                    trades.append(0)
                    position = None
            elif position['type'] == 'SELL':
                if price <= position['tp']:
                    trades.append(1)
                    position = None
                elif price >= position['sl']:
                    trades.append(0)
                    position = None

    total_trades = len(trades)
    wins = sum(trades)
    losses = total_trades - wins
    win_rate = round((wins / total_trades) * 100, 2) if total_trades > 0 else 0.0

    print("📊 PERFORMANCE RESULTS:")
    print(f"  • Total Executed Signals : {total_trades}")
    print(f"  • Successful Trades (TP)  : {wins}")
    print(f"  • Stopped Out Trades (SL) : {losses}")
    print(f"  • Win Rate Efficiency     : {win_rate}%")
    print("=========================================================\n")

if __name__ == "__main__":
    run_quantitative_backtest()
