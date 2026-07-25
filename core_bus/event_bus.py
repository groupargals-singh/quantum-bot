import asyncio
from typing import Callable, Dict, List, Any

class AsyncEventBus:
    """
    High-Speed Async Inter-Squad Communication Router.
    Routes data signals between Squad A through Squad T in micro-seconds.
    """
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable):
        """Subscribe a Squad Commander to a specific event topic."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    async def publish(self, event_type: str, data: Dict[str, Any]):
        """Publish signal across all subscribed Squads asynchronously."""
        if event_type in self._subscribers:
            tasks = [asyncio.create_task(callback(data)) for callback in self._subscribers[event_type]]
            await asyncio.gather(*tasks)
