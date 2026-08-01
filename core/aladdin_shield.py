import config

class AladdinShield:
    def __init__(self):
        self.daily_pnl = 0.0
        self.is_kill_switch_active = False

    def check_risk_limits(self, current_vix: float) -> bool:
        if self.is_kill_switch_active:
            print("[ALADDIN SHIELD] Kill-switch ACTIVE! Trading blocked.")
            return False

        if self.daily_pnl <= -config.MAX_DAILY_LOSS:
            self.trigger_kill_switch("Daily Max Loss Reached")
            return False

        if current_vix > config.VIX_HIGH_THRESHOLD:
            print("[ALADDIN SHIELD] Warning: High Volatility (VIX). Position sizing reduced.")

        return True

    def trigger_kill_switch(self, reason: str):
        self.is_kill_switch_active = True
        print(f"[KILL-SWITCH TRIGGERED] Reason: {reason}. All trades blocked!")
