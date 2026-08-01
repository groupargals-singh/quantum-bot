import yfinance as yf
import pandas as pd
import numpy as np

class AIQuantumDecisionEngine:
    def __init__(self, symbol="^NSEBANK"):
        self.symbol = symbol

    def fetch_live_data(self):
        try:
            df = yf.download(self.symbol, period="5d", interval="5m", progress=False)
            if df.empty:
                return None
            
            # Multi-Index Column Flattening (Fixes float conversion error)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
                
            return df
        except Exception as e:
            print(f"Data Fetch Error: {e}")
            return None

    def calculate_atr(self, df, period=14):
        high_low = df['High'] - df['Low']
        high_close = np.abs(df['High'] - df['Close'].shift())
        low_close = np.abs(df['Low'] - df['Close'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        return tr.rolling(period).mean().iloc[-1]

    def analyze_market_momentum(self):
        df = self.fetch_live_data()
        if df is None or len(df) < 30:
            return {"status": "INSUFFICIENT_DATA"}

        df['EMA9'] = df['Close'].ewm(span=9, adjust=False).mean()
        df['EMA21'] = df['Close'].ewm(span=21, adjust=False).mean()
        df['Vol_Avg'] = df['Volume'].rolling(20).mean()

        current_price = float(df['Close'].iloc[-1])
        prev_high = float(df['High'].iloc[-2])
        prev_low = float(df['Low'].iloc[-2])
        ema9_val = float(df['EMA9'].iloc[-1])
        ema21_val = float(df['EMA21'].iloc[-1])
        atr_val = float(self.calculate_atr(df))

        # Direction Determination
        direction = "NEUTRAL"
        if ema9_val > ema21_val:
            direction = "BUY_CE"
        elif ema9_val < ema21_val:
            direction = "BUY_PE"

        # 1. SCALP MODE CALCULATIONS (Quick Small Move)
        scalp_move_pts = round(atr_val * 0.6, 2)
        if direction == "BUY_CE":
            scalp_target = round(current_price + scalp_move_pts, 2)
            scalp_sl = round(current_price - (scalp_move_pts * 0.7), 2)
        elif direction == "BUY_PE":
            scalp_target = round(current_price - scalp_move_pts, 2)
            scalp_sl = round(current_price + (scalp_move_pts * 0.7), 2)
        else:
            scalp_target = scalp_sl = current_price

        # 2. MOMENTUM MODE CALCULATIONS (Bada Move)
        momentum_move_pts = round(atr_val * 1.8, 2)
        if direction == "BUY_CE":
            momentum_target = round(current_price + momentum_move_pts, 2)
            momentum_sl = round(current_price - (atr_val * 0.9), 2)
        elif direction == "BUY_PE":
            momentum_target = round(current_price - momentum_move_pts, 2)
            momentum_sl = round(current_price + (atr_val * 0.9), 2)
        else:
            momentum_target = momentum_sl = current_price

        return {
            "symbol": "BANKNIFTY",
            "current_price": round(current_price, 2),
            "signal": direction,
            "scalp_pts": scalp_move_pts,
            "scalp_target": scalp_target,
            "scalp_sl": scalp_sl,
            "scalp_time": "5 - 15 Mins",
            "momentum_pts": momentum_move_pts,
            "momentum_target": momentum_target,
            "momentum_sl": momentum_sl,
            "momentum_time": "30 - 60 Mins"
        }

if __name__ == "__main__":
    engine = AIQuantumDecisionEngine()
    res = engine.analyze_market_momentum()
    print("\n⚡ QUANTUM DUAL-DECISION MATRIX ⚡")
    print(f"📊 Symbol: {res.get('symbol')} | Live Price: ₹{res.get('current_price')}")
    print(f"🎯 Preferred Action: {res.get('signal')}\n")
    print("─── ⚡ CHHOTA PROFIT (SCALPING MODE) ───")
    print(f"⏱ Expected Time: {res.get('scalp_time')}")
    print(f"📈 Quick Move: {res.get('scalp_pts')} Points")
    print(f"🎯 Scalp Target: ₹{res.get('scalp_target')} | SL: ₹{res.get('scalp_sl')}\n")
    print("─── 🚀 BADA PROFIT (MOMENTUM MODE) ───")
    print(f"⏱ Expected Time: {res.get('momentum_time')}")
    print(f"📈 Big Move: {res.get('momentum_pts')} Points")
    print(f"🎯 Big Target: ₹{res.get('momentum_target')} | SL: ₹{res.get('momentum_sl')}\n")
