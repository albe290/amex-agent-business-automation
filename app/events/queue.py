import queue
from typing import Optional, List
from app.events.models import PlatformEvent

class EventQueue:
    """
    Simple thread-safe in-memory event queue.
    Wraps the standard library queue for platform-specific patterns.
    """
    def __init__(self, maxsize: int = 1000):
        self._queue = queue.Queue(maxsize=maxsize)
        self._history: List[PlatformEvent] = []

    def enqueue(self, event: PlatformEvent):
        """Adds an event to the queue."""
        self._queue.put(event)
        self._history.append(event)

    def dequeue(self) -> Optional[PlatformEvent]:
        """Pulls the next event from the queue."""
        try:
            return self._queue.get_nowait()
        except queue.Empty:
            return None

    def get_depth(self) -> int:
        """Returns the current number of pending events."""
        return self._queue.qsize()

    def peek_history(self, limit: int = 10) -> List[PlatformEvent]:
        """Returns recent events for diagnostic visibility."""
        return self._history[-limit:]

# Singleton queue instance for the platform
event_queue = EventQueue()
