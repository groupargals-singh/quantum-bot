import time
from typing import Dict, Any

class AladdinRiskEngine:
    """
    Squad P: Risk & Capital Preservation Engine
    Monitors Max Drawdown, Position Limits, and activates Global Kill Switch if needed.
    """
    def __init__(self, max_daily_loss: float = 5000.0, max_position_value: float = 100000.0):
        self.max_daily_loss = max_daily_loss
        self.max_position_value = max_position_value
        self.current_daily_pnl = 0.0
        self.kill_switch_active = False

    def evaluate_trade_risk(self, symbol: str, price: float, quantity: int) -> Dict[str, Any]:
        """Checks if an outgoing trade signal passes capital preservation rules."""
        if self.kill_switch_active:
            return {
                "approved": False, 
                "reason": "🚨 KILL SWITCH ACTIVE: Max Daily Loss Breached! All Trading Halted."
            }

        order_value = price * quantity
        if order_value > self.max_position_value:
            return {
                "approved": False, 
                "reason": f"❌ RISK REJECT: Position size (₹{order_value}) exceeds max limit (₹{self.max_position_value})"
            }

        return {
            "approved": True, 
            "reason": "✅ RISK APPROVED: Trade within safety margins."
        }

    def update_pnl(self, pnl_delta: float):
        """Updates PnL and triggers Emergency Halt if loss limit crossed."""
        self.current_daily_pnl += pnl_delta
        if self.current_daily_pnl <= -self.max_daily_loss:
            self.kill_switch_active = True
            print(f"\n🚨 [KILL SWITCH TRIGGERED] Daily Loss Hit: ₹{self.current_daily_pnl:.2f}. System Locked!")
