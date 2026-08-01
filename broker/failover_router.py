import config

class BrokerRouter:
    def __init__(self, paper_engine):
        self.primary = config.PRIMARY_BROKER
        self.secondary = config.SECONDARY_BROKER
        self.paper_engine = paper_engine

    def send_order(self, symbol: str, qty: int, price: float, side: str):
        if config.PAPER_TRADING:
            self.paper_engine.execute_order(symbol, qty, price, side)
            return

        try:
            print(f"[BROKER] Routing order to Primary ({self.primary})...")
        except Exception as e:
            print(f"[BROKER FAILOVER] Primary failed: {e}. Switching to Secondary ({self.secondary})...")
