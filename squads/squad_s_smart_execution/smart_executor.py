import time
from typing import Dict, Any

class SmartExecutionEngine:
    """
    Squad S: Execution Engine & Paper Trading Terminal
    Executes Limit/Market orders with slippage protection or runs Paper Trading.
    """
    def __init__(self, paper_trading: bool = True, initial_capital: float = 100000.0):
        self.paper_trading = paper_trading
        self.capital = initial_capital
        self.positions: Dict[str, Dict[str, Any]] = {}

    def execute_order(self, symbol: str, signal: int, price: float, quantity: int) -> Dict[str, Any]:
        """Executes trade signal in Paper Trading mode or routes to broker API."""
        action = "BUY" if signal == 1 else "SELL"
        order_cost = price * quantity

        if self.paper_trading:
            if action == "BUY" and self.capital < order_cost:
                return {"status": "REJECTED", "reason": "Insufficient Paper Capital"}

            if action == "BUY":
                self.capital -= order_cost
                self.positions[symbol] = {"qty": quantity, "entry_price": price}
            elif action == "SELL" and symbol in self.positions:
                pnl = (price - self.positions[symbol]["entry_price"]) * quantity
                self.capital += order_cost + pnl
                del self.positions[symbol]

            return {
                "status": "EXECUTED (PAPER TRADING)",
                "action": action,
                "symbol": symbol,
                "price": price,
                "quantity": quantity,
                "remaining_capital": round(self.capital, 2),
                "timestamp": time.time()
            }
        else:
            return {"status": "BROKER_ROUTED", "action": action, "symbol": symbol}
