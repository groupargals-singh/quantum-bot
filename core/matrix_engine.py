import numpy as np

class CompleteMatrixMathEngine:
    def __init__(self):
        print("🧮 Complete Matrix Math Engine Initialized.")

    def calculate_full_matrix(self, market_feed):
        # Extract market feed indicators
        pcr = market_feed.get("pcr", 1.0)
        vix = market_feed.get("vix", 15.0)
        momentum = market_feed.get("momentum", 50.0)
        delta_flow = market_feed.get("delta_flow", 0.0)

        # Multi-factor Matrix Weighting
        pcr_weight = 85.0 if pcr > 1.2 else 50.0
        vix_weight = 80.0 if vix < 20.0 else 40.0
        momentum_weight = min(momentum, 100.0)
        delta_weight = min(delta_flow, 100.0)

        # Calculate Matrix Consensus Score
        king_consensus = (pcr_weight * 0.25) + (vix_weight * 0.20) + (momentum_weight * 0.30) + (delta_weight * 0.25)

        return {
            "king_consensus_pct": round(king_consensus, 2),
            "matrix_state": "BULLISH_CONVERGENCE" if king_consensus > 75.0 else "NEUTRAL",
            "eigen_signal": "STRONG_BUY" if king_consensus > 80.0 else "HOLD"
        }
