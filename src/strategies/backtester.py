import requests
import time
import numpy as np

class QuantitativeBacktester:
    """Enterprise Backtesting Engine with Real Exchange Fees & Slippage Models"""
    def __init__(self, initial_capital=10000.0, fee_rate=0.0004, slippage=0.0001):
        self.initial_capital = initial_capital
        self.fee_rate = fee_rate       # 0.04% Binance Taker Fee
        self.slippage = slippage       # 0.01% Market Slippage
        
    def fetch_historical_klines(self, symbol="BTCUSDT", interval="5m", limit=1000):
        print(f"📥 [BACKTEST Engine] Fetching historical {interval} candles for {symbol} from Binance API...")
        url = "https://api.binance.com/api/v3/klines"
        params = {"symbol": symbol.upper(), "interval": interval, "limit": limit}
        try:
            res = requests.get(url, params=params, timeout=10)
            data = res.json()
            candles = []
            for item in data:
                candles.append({
                    "timestamp": item[0],
                    "open": float(item[1]),
                    "high": float(item[2]),
                    "low": float(item[3]),
                    "close": float(item[4]),
                    "volume": float(item[5])
                })
            return candles
        except Exception as e:
            print(f"❌ [BACKTEST ERROR] Failed to fetch data: {e}")
            return []

    def run(self, symbol="BTCUSDT", interval="5m", limit=1000):
        candles = self.fetch_historical_klines(symbol, interval, limit)
        if not candles:
            return

        capital = self.initial_capital
        position = None
        trades = []
        equity_curve = [capital]
        prices = []

        for i, candle in enumerate(candles):
            close_price = candle['close']
            prices.append(close_price)

            if len(prices) < 25:  # Indicator Warmup Period
                continue

            # 1. Technical Indicators (EMA & RSI Simulation)
            ema_fast = np.mean(prices[-9:])
            ema_slow = np.mean(prices[-21:])
            
            returns = np.diff(prices[-15:])
            gains = [r for r in returns if r > 0]
            losses = [-r for r in returns if r < 0]
            avg_gain = np.mean(gains) if gains else 0.0001
            avg_loss = np.mean(losses) if losses else 0.0001
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

            # 2. Simulated Orderbook Imbalance from Candle Volume Momentum
            price_change = close_price - candle['open']
            candle_range = candle['high'] - candle['low'] + 1e-8
            imbalance = np.clip((price_change / candle_range), -1.0, 1.0)

            # 3. Consensus Strategy Rules
            signal = None
            if imbalance > 0.25 and rsi < 65 and ema_fast > ema_slow:
                signal = "BUY"
            elif imbalance < -0.25 and rsi > 35 and ema_fast < ema_slow:
                signal = "SELL"

            # 4. Trade Execution Engine
            if position is None and signal is not None:
                trade_size = capital * 0.10  # 10% Risk Allocation
                entry_price = close_price * (1 + self.slippage if signal == "BUY" else 1 - self.slippage)
                entry_fee = trade_size * self.fee_rate
                capital -= entry_fee

                sl_dist = entry_price * 0.015  # 1.5% Stop Loss
                tp_dist = entry_price * 0.030  # 3.0% Take Profit

                stop_loss = entry_price - sl_dist if signal == "BUY" else entry_price + sl_dist
                take_profit = entry_price + tp_dist if signal == "BUY" else entry_price - tp_dist

                position = {
                    "type": signal,
                    "entry": entry_price,
                    "size": trade_size,
                    "stop_loss": stop_loss,
                    "take_profit": take_profit,
                    "time": candle['timestamp']
                }

            elif position is not None:
                pos_type = position['type']
                entry = position['entry']
                size = position['size']
                sl = position['stop_loss']
                tp = position['take_profit']

                exit_price = None
                exit_reason = None

                if pos_type == "BUY":
                    if candle['low'] <= sl:
                        exit_price = sl
                        exit_reason = "STOP_LOSS"
                    elif candle['high'] >= tp:
                        exit_price = tp
                        exit_reason = "TAKE_PROFIT"
                elif pos_type == "SELL":
                    if candle['high'] >= sl:
                        exit_price = sl
                        exit_reason = "STOP_LOSS"
                    elif candle['low'] <= tp:
                        exit_price = tp
                        exit_reason = "TAKE_PROFIT"

                if exit_price:
                    pnl = (size / entry) * (exit_price - entry) if pos_type == "BUY" else (size / entry) * (entry - exit_price)
                    exit_fee = size * self.fee_rate
                    net_pnl = pnl - exit_fee
                    capital += net_pnl
                    equity_curve.append(capital)

                    trades.append({
                        "symbol": symbol,
                        "type": pos_type,
                        "entry": entry,
                        "exit": exit_price,
                        "pnl": net_pnl,
                        "reason": exit_reason
                    })
                    position = None

        # 5. Metrics & Reporting
        total_trades = len(trades)
        wins = [t for t in trades if t['pnl'] > 0]
        losses = [t for t in trades if t['pnl'] <= 0]
        win_rate = (len(wins) / total_trades * 100) if total_trades > 0 else 0.0
        
        gross_profit = sum([t['pnl'] for t in wins])
        gross_loss = abs(sum([t['pnl'] for t in losses]))
        profit_factor = round(gross_profit / gross_loss, 2) if gross_loss > 0 else (gross_profit if gross_profit > 0 else 0.0)

        # Max Drawdown Calculation
        peak = self.initial_capital
        max_dd = 0.0
        for eq in equity_curve:
            if eq > peak:
                peak = eq
            dd = (peak - eq) / peak * 100
            if dd > max_dd:
                max_dd = dd

        ret_pct = ((capital - self.initial_capital) / self.initial_capital) * 100

        print("\n" + "="*55)
        print("📊 INSTITUTIONAL QUANT BACKTEST REPORT")
        print("="*55)
        print(f"🪙 Symbol Tested: {symbol} ({interval} interval, {len(candles)} candles)")
        print(f"💵 Initial Capital: ${self.initial_capital:.2f}")
        print(f"💰 Final Capital:   ${capital:.2f}")
        print(f"📈 Total Return:    {ret_pct:+.2f}%")
        print(f"🔢 Total Trades:    {total_trades}")
        print(f"🎯 Win Rate:        {win_rate:.2f}% ({len(wins)} Wins / {len(losses)} Losses)")
        print(f"⚖️ Profit Factor:   {profit_factor}")
        print(f"🛑 Max Drawdown:    {max_dd:.2f}%")
        print(f"💸 Fees & Slippage: Applied ({self.fee_rate*100}% Fee + {self.slippage*100}% Slippage)")
        print("="*55 + "\n")
