import time
from typing import List, Dict, Any
from squads.base_brain import BaseMicroBrain

class BaseSquadCommander:
    """
    Squad Commander Engine:
    Aggregates signals from all Micro-Brains in the squad,
    applies PSI weighting, and outputs single Squad Consensus Signal.
    """
    def __init__(self, squad_code: str, squad_name: str):
        self.squad_code = squad_code
        self.squad_name = squad_name
        self.brains: List[BaseMicroBrain] = []

    def register_brain(self, brain: BaseMicroBrain):
        """Registers a Micro-Brain into this Squad Swarm."""
        self.brains.append(brain)

    def calculate_squad_consensus(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculates weighted consensus signal based on Brains' PSI scores."""
        if not self.brains:
            return {"squad": self.squad_code, "signal": 0, "confidence": 0.0}

        weighted_signal = 0.0
        total_weight = 0.0

        for brain in self.brains:
            weight = brain.psi_score / 100.0  # Higher PSI = Higher Weight
            # Simulated brain directional output (-1 Sell, 0 Hold, +1 Buy)
            brain_signal = 1 if market_data.get("price", 0) > 2500 else -1
            
            weighted_signal += brain_signal * weight
            total_weight += weight

        final_score = weighted_signal / max(0.001, total_weight)
        
        return {
            "squad_code": self.squad_code,
            "squad_name": self.squad_name,
            "consensus_signal": 1 if final_score > 0.3 else (-1 if final_score < -0.3 else 0),
            "confidence_score": round(abs(final_score) * 100, 2),
            "active_brains_voted": len(self.brains),
            "timestamp": time.time()
        }
