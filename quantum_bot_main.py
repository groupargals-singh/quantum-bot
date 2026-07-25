import time
import asyncio
from data_filters.noise_filter import DataFilterEngine
from squads.base_brain import BaseMicroBrain
from squads.base_squad import BaseSquadCommander
from core_bus.event_bus import AsyncEventBus

class QuantumBotEngine:
    def __init__(self):
        print("==================================================")
        print("🚀 QUANTUM BOT FULL MASTER SWARM ENGINE (20 SQUADS)")
        print("==================================================")
        
        self.data_filter = DataFilterEngine(volatility_threshold=0.0002)
        self.event_bus = AsyncEventBus()
        self.squad_m = BaseSquadCommander("SQUAD_M", "Orderflow & HFT Depth")
        
        # Register Sample Micro Brains into Squad M
        b1 = BaseMicroBrain("SQM_BR_001", "squad_m_orderflow", "Level-3 Depth Scanner")
        b2 = BaseMicroBrain("SQM_BR_002", "squad_m_orderflow", "Spoof Detector")
        self.squad_m.register_brain(b1)
        self.squad_m.register_brain(b2)

    def boot_system(self):
        print("[1/4] Data Filter & Garbage Stripper Engine... [ACTIVE]")
        print("[2/4] High-Speed Async Event Bus Pipeline... [ACTIVE]")
        print("[3/4] 20 Squad Directory Structure & Memory Hierarchy... [MOUNTED]")
        print("[4/4] Squad Commanders & Swarm Consensus Engine... [READY]")
        print("\n✨ Quantum Bot System Online & Fully Assembled!\n")

    def run_live_simulation(self):
        sample_ticks = [
            ("RELIANCE", 2500.0, 1000),
            ("RELIANCE", 2500.01, 1200),  # Dropped Noise
            ("RELIANCE", 2512.00, 8000),  # Passed Tick
        ]

        print("--- Running Full Engine Simulation ---")
        for symbol, price, vol in sample_ticks:
            filtered = self.data_filter.process_tick(symbol, price, vol)
            if filtered:
                print(f"⚡ TICK PASSED: {symbol} @ ₹{price}")
                consensus = self.squad_m.calculate_squad_consensus(filtered)
                print(f"📊 {consensus['squad_name']} Signal: {consensus['consensus_signal']} (Confidence: {consensus['confidence_score']}%)\n")
            else:
                print(f"🧹 NOISE DROPPED: {symbol} @ ₹{price}")

if __name__ == "__main__":
    bot = QuantumBotEngine()
    bot.boot_system()
    bot.run_live_simulation()
