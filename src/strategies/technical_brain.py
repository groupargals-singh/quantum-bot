import time
from collections import deque

class SquadBTechnicalBrain:
    """Squad B: Real-time Price Velocity & Technical Momentum Engine"""
    def __init__(self, window_size=20):
        self.prices = deque(maxlen=window_size)

    def update_price(self, price):
        self.prices.append(price)

    def analyze_momentum(self):
        if len(self.prices) < 5:
            return "NEUTRAL", 50.0

        # Calculate Price Velocity over last 5 ticks
        start_p = self.prices[-5]
        end_p = self.prices[-1]
        pct_change = ((end_p - start_p) / start_p) * 100

        if pct_change > 0.05:
            return "BULLISH", round(min(50 + pct_change * 100, 95), 2)
        elif pct_change < -0.05:
            return "BEARISH", round(min(50 + abs(pct_change) * 100, 95), 2)
        else:
            return "NEUTRAL", 50.0

# Shared Technical Brain Instance
technical_brain = SquadBTechnicalBrain()
