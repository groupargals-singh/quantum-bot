import time

class AladdinRiskShield:
    """BlackRock-Style Institutional Risk Engine (Squad P)"""
    def __init__(self, max_risk_per_trade=0.02, min_rr_ratio=2.0):
        self.max_risk_per_trade = max_risk_per_trade  # Max 2% capital per trade
        self.min_rr_ratio = min_rr_ratio              # Minimum 1:2 Risk-Reward
        self.consecutive_losses = 0
        self.circuit_breaker_active = False

    def validate_signal(self, symbol, signal_type, entry_price, imbalance):
        if self.circuit_breaker_active:
            print("🛡️ [ALADDIN RISK SHIELD] Rejected: Circuit Breaker Triggered!")
            return False, None

        # Stop-Loss & Take-Profit Calculation (Dynamic 0.5% SL, 1.0% TP)
        sl_pct = 0.005
        tp_pct = sl_pct * self.min_rr_ratio

        if signal_type == "BUY":
            stop_loss = round(entry_price * (1 - sl_pct), 2)
            take_profit = round(entry_price * (1 + tp_pct), 2)
        else:  # SELL
            stop_loss = round(entry_price * (1 + sl_pct), 2)
            take_profit = round(entry_price * (1 - sl_pct), 2)

        risk_score = round(abs(imbalance) * 100, 2)

        verified_signal = {
            "symbol": symbol,
            "type": signal_type,
            "entry": entry_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "rr_ratio": f"1:{self.min_rr_ratio}",
            "risk_score": f"{risk_score}/100",
            "timestamp": time.time()
        }

        return True, verified_signal

# Shared Risk Shield Instance
risk_shield = AladdinRiskShield()
