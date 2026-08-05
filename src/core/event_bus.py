import queue
import threading
import time
from collections import defaultdict

class SwarmEventBus:
    """High-Performance In-Memory Pub/Sub Message Broker for 20 Squads"""
    def __init__(self):
        self._subscribers = defaultdict(list)
        self._lock = threading.Lock()

    def subscribe(self, topic: str, callback):
        with self._lock:
            self._subscribers[topic].append(callback)

    def publish(self, topic: str, data: dict):
        with self._lock:
            listeners = list(self._subscribers.get(topic, []))
        
        for callback in listeners:
            try:
                threading.Thread(target=callback, args=(data,), daemon=True).start()
            except Exception as e:
                print(f"❌ [EVENT BUS ERROR] Sub Callback Failed ({topic}): {e}")

# Global Shared Instance
event_bus = SwarmEventBus()
