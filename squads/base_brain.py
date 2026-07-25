import json
import os
import time
from typing import Dict, Any

class BaseMicroBrain:
    """
    Universal Base Engine for all Micro-Brains in the Swarm.
    Includes Local JSON Memory & Performance Score Index (PSI).
    """
    def __init__(self, brain_id: str, squad_code: str, role: str):
        self.brain_id = brain_id
        self.squad_code = squad_code
        self.role = role
        self.rank = "Brain"  # Hierarchy: Brain -> Unit Lead -> Sub-Group Cmd -> Group Cmd -> Squad Cmd
        
        self.total_predictions = 0
        self.correct_predictions = 0
        self.psi_score = 50.0  # Initial Base Performance Score Index (0 to 100)
        
        self.memory_dir = f"logs/{self.squad_code}"
        os.makedirs(self.memory_dir, exist_ok=True)
        self.memory_file_path = f"{self.memory_dir}/{self.brain_id}_memory.json"
        
        self.load_memory()

    def evaluate_prediction(self, predicted_direction: int, actual_direction: int):
        """Updates PSI score and triggers self-learning promotion check."""
        self.total_predictions += 1
        if predicted_direction == actual_direction:
            self.correct_predictions += 1
            self.psi_score = min(100.0, self.psi_score + 0.5)
        else:
            self.psi_score = max(0.0, self.psi_score - 0.8)
        
        self._check_auto_promotion()
        self.save_memory()

    def _check_auto_promotion(self):
        """Autonomous Promotion Engine based on PSI threshold."""
        if self.psi_score >= 92.0 and self.total_predictions >= 500:
            if self.rank == "Brain":
                self.rank = "Unit Lead"
                print(f"🔥 [PROMOTION] {self.brain_id} promoted to {self.rank}! (PSI: {self.psi_score:.2f})")

    def save_memory(self):
        """Saves compressed memory state to JSON."""
        state = {
            "brain_id": self.brain_id,
            "rank": self.rank,
            "psi_score": round(self.psi_score, 2),
            "total_predictions": self.total_predictions,
            "accuracy": round((self.correct_predictions / max(1, self.total_predictions)) * 100, 2),
            "last_updated": time.time()
        }
        with open(self.memory_file_path, "w") as f:
            json.dump(state, f, indent=2)

    def load_memory(self):
        """Loads state from local JSON if exists."""
        if os.path.exists(self.memory_file_path):
            try:
                with open(self.memory_file_path, "r") as f:
                    state = json.load(f)
                    self.rank = state.get("rank", "Brain")
                    self.psi_score = state.get("psi_score", 50.0)
                    self.total_predictions = state.get("total_predictions", 0)
            except Exception:
                pass
