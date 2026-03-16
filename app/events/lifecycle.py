from typing import Dict, List, Any
from datetime import datetime
from app.events.models import EventStatus, PlatformEvent

class EventLifecycle:
    """
    Tracks and manages the state transitions of a platform event.
    Provides a centralized audit of 'where' an event is in the pipeline.
    """
    def __init__(self):
        self._states: Dict[str, List[Dict[str, Any]]] = {}

    def transition(self, event: PlatformEvent, new_status: EventStatus):
        """
        Records a status transition for an event.
        """
        event_id = event.event_id
        if event_id not in self._states:
            self._states[event_id] = []
            
        old_status = event.status
        event.status = new_status
        
        self._states[event_id].append({
            "from": old_status,
            "to": new_status,
            "timestamp": datetime.utcnow()
        })
        
        print(f"[LIFECYCLE] Event {event_id}: {old_status} -> {new_status}")

    def get_history(self, event_id: str) -> List[Dict[str, Any]]:
        return self._states.get(event_id, [])

# Singleton lifecycle instance
lifecycle_manager = EventLifecycle()
