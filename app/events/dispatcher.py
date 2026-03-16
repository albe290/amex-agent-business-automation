from typing import Dict, Any, Callable, Coroutine
from app.events.models import PlatformEvent, EventType
from app.events.lifecycle import lifecycle_manager

class EventDispatcher:
    """
    Internal router that sends platform events to their specific handlers.
    """
    def __init__(self):
        self._handlers: Dict[EventType, Callable[[PlatformEvent], Coroutine[Any, Any, None]]] = {}

    def register_handler(self, event_type: EventType, handler: Callable[[PlatformEvent], Coroutine[Any, Any, None]]):
        self._handlers[event_type] = handler

    async def dispatch(self, event: PlatformEvent):
        """
        Routes an event to its registered handler.
        """
        handler = self._handlers.get(event.event_type)
        if handler:
            print(f"[DISPATCHER] Routing event {event.event_id} (type: {event.event_type.value})")
            await handler(event)
        else:
            print(f"[DISPATCHER] WARNING: No handler registered for event type {event.event_type.value}")

# Singleton dispatcher instance
dispatcher = EventDispatcher()
