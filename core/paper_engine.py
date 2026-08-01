class PaperEngine:
    def __init__(self, initial_capital: float = 100000.0):
        self.capital = initial_capital
        self.positions = {}
        self.pnl = 0.0

    def execute_order(self, symbol: str, qty: int, price: float, order_type: str):
        cost = qty * price
        if order_type == "BUY":
            if self.capital >= cost:
                self.capital -= cost
                self.positions[symbol] = self.positions.get(symbol, 0) + qty
                print(f"[PAPER ENGINE] BUY Executed: {qty} x {symbol} @ ₹{price}")
            else:
                print("[PAPER ENGINE] Error: Insufficient Virtual Funds!")
        elif order_type == "SELL":
            if self.positions.get(symbol, 0) >= qty:
                self.capital += cost
                self.positions[symbol] -= qty
                print(f"[PAPER ENGINE] SELL Executed: {qty} x {symbol} @ ₹{price}")

    def get_portfolio_status(self):
        return {"Virtual Capital": self.capital, "Positions": self.positions}
