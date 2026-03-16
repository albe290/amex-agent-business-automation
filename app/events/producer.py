from typing import Dict, Any
from app.events.models import IncomingEvent, EventType, EventStatus
from app.events.queue import event_queue
from app.events.lifecycle import lifecycle_manager

class EventProducer:
    """
    Ingests raw request data and converts it into governed platform events.
    """
    def produce(self, payload: Dict[str, Any], source: str = "API") -> IncomingEvent:
        # 1. Create the event
        event = IncomingEvent(
            event_type=EventType.NEW_REQUEST,
            status=EventStatus.RECEIVED,
            payload=payload,
            source=source
        )
        
        # 2. Track initial state
        lifecycle_manager.transition(event, EventStatus.QUEUED)
        
        # 3. Place in queue
        event_queue.enqueue(event)
        
        print(f"[PRODUCER] Ingested event {event.event_id} from {source}")
        return event

# Singleton producer instance
producer = EventProducer()
