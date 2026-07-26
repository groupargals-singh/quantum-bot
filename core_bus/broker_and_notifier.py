class InstitutionalBrokerAdapter:
    def __init__(self, mode: str = "PAPER"):
        self.mode = mode

    def place_order(self, symbol: str, action: str, qty: int, price: float) -> dict:
        return {"status": "SUCCESS", "symbol": symbol, "action": action, "qty": qty, "price": price}
