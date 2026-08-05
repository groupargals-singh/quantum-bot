import time
import threading
import requests
import os

class SquadMMonitor:
    """Squad M: System Auto-Healer & Latency Monitor"""
    def __init__(self):
        self.last_tick_time = time.time()
        self.latency_ms = 0.0
        self.is_healthy = True

    def update_tick(self, timestamp):
        current_time = time.time()
        self.latency_ms = round((current_time - timestamp) * 1000, 2)
        self.last_tick_time = current_time
        self.is_healthy = True

    def start_keep_alive(self):
        app_url = os.environ.get("RENDER_EXTERNAL_URL")
        
        def ping_loop():
            while True:
                time.sleep(600)  # Ping every 10 minutes
                if app_url:
                    try:
                        requests.get(f"{app_url}/health", timeout=10)
                        print("📡 [SQUAD M] Self-Ping Sent. Keeping Server Alive!")
                    except Exception as e:
                        print(f"⚠️ [SQUAD M PING ERROR] {e}")

        t = threading.Thread(target=ping_loop, daemon=True)
        t.start()
        print("🛡️ [SQUAD M] Auto-Healing & Keep-Alive Guard Online!")

system_monitor = SquadMMonitor()
