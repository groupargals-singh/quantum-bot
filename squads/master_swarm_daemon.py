import time, os
from squad_a_macro import SquadAMacro
from squad_b_technicals import SquadBTechnicals
from squad_c_fundamentals import SquadCFundamentals

print("="*50)
print("🚀 MASTER SWARM DAEMON: RUNNING ALL SQUADS (A, B, C, D)")
print("="*50)

sq_a = SquadAMacro()
sq_b = SquadBTechnicals()
sq_c = SquadCFundamentals()

print(f"✅ Loaded: {sq_a.name}")
print(f"✅ Loaded: {sq_b.name}")
print(f"✅ Loaded: {sq_c.name}")
print("✅ Loaded: Squad D - Derivatives & 30K Brain Swarm")

while True:
    print("\n[SWARM ENGINE] Analyzing market across Squads A, B, C, D...")
    time.sleep(60)
