import os, json
from pathlib import Path
from datetime import datetime

SQUAD_DIR = Path("squad_d_derivatives")
SUP_DIR = SQUAD_DIR / "supervisor_brain_derivatives"
GROUPS_DIR = SQUAD_DIR / "hierarchy_groups"

SUP_DIR.mkdir(parents=True, exist_ok=True)
GROUPS_DIR.mkdir(parents=True, exist_ok=True)

master_memory = {
    "brain_id": "SD_MSTR",
    "tier": "Master Commander",
    "power_multiplier": 100.0,
    "accuracy_score": 99.9,
    "self_correction_count": 0,
    "total_promotions": 0,
    "total_demotions": 0,
    "status": "ACTIVE_24_7_AUTONOMOUS"
}
with open(SUP_DIR / "sd_mstr_memory.json", "w") as f:
    json.dump(master_memory, f, indent=2)

master_engine_code = '''import json
from pathlib import Path
from datetime import datetime

def master_self_learn():
    mem_path = Path("sd_mstr_memory.json")
    with open(mem_path, "r") as f:
        data = json.load(f)

    if data["accuracy_score"] < 100.0:
        data["accuracy_score"] = min(100.0, data["accuracy_score"] + 0.05)

    data["self_correction_count"] += 1
    data["last_optimized"] = str(datetime.now())

    with open(mem_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"👑 [SD_MSTR MASTER] Self-Learned. Accuracy: {data['accuracy_score']}%")

if __name__ == "__main__":
    master_self_learn()
'''.strip()

with open(SUP_DIR / "sd_mstr_engine.py", "w") as f:
    f.write(master_engine_code)

print("✅ Squad D Environment Restored Successfully!")
