class AladdinRiskShield:
    """Institutional Risk Control & Circuit Breaker Engine"""
    def __init__(self, max_daily_loss=2000.0, max_positions=5):
        self.max_daily_loss = max_daily_loss
        self.max_positions = max_positions
        self.daily_pnl = 0.0
        self.circuit_breaker_tripped = False
        self.positions = {}

    def can_open_trade(self) -> tuple[bool, str]:
        if self.circuit_breaker_tripped:
            return False, "🚨 CIRCUIT BREAKER ACTIVE: Max daily loss breached!"
        if len(self.positions) >= self.max_positions:
            return False, f"⚠️ POSITIONS FULL: Reached max limit ({self.max_positions})"
        if self.daily_pnl <= -self.max_daily_loss:
            self.circuit_breaker_tripped = True
            return False, f"🚨 MAX DAILY LOSS REACHED (-₹{abs(self.daily_pnl)}). HALTING TRADES."
        return True, "ALLOWED"

    def add_position(self, symbol: str, qty: int, buy_price: float):
        self.positions[symbol] = {
            "qty": qty,
            "buy_price": buy_price,
            "highest_price": buy_price,
            "stop_loss": round(buy_price * 0.99, 2),  # Initial 1% SL
            "target": round(buy_price * 1.02, 2)      # Initial 2% Target
        }

    def update_trailing_stop(self, symbol: str, current_price: float):
        """Dynamic Trailing Stop Loss Algorithm"""
        if symbol in self.positions:
            pos = self.positions[symbol]
            if current_price > pos["highest_price"]:
                pos["highest_price"] = current_price
                # Trail Stop Loss 1% below highest achieved price
                pos["stop_loss"] = round(current_price * 0.99, 2)

    def record_closed_pnl(self, pnl: float):
        self.daily_pnl += pnl
        if self.daily_pnl <= -self.max_daily_loss:
            self.circuit_breaker_tripped = True
            print(f"\n💥 [ALADDIN SHIELD TRIP] Daily Loss exceeded limit (-₹{self.max_daily_loss})! EMERGENCY HALT.")
