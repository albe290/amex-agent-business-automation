from typing import Dict, Any, Optional
from app.events.models import OutcomeEvent, EventType, EventStatus
from monitoring.metrics import event_bus

class EventPublisher:
    """
    Emits final platform outcomes to downstream collectors and dashboard telemetry.
    """
    async def publish_outcome(self, event_id: str, correlation_id: str, result: Dict[str, Any], trace_id: Optional[str] = None):
        # 1. Determine result type for classification
        result_type = result.get("strategy_path", "UNKNOWN")
        
        # 2. Create outcome event
        outcome = OutcomeEvent(
            event_type=EventType.COMPLETED,
            status=EventStatus.COMPLETED,
            correlation_id=correlation_id,
            payload=result,
            result_type=result_type,
            trace_id=trace_id
        )
        
        # 3. Emit to real-time event bus (Dashboard/Analytics)
        await event_bus.emit("OUTCOME_PUBLISHED", outcome.model_dump())
        
        print(f"[PUBLISHER] Emitted outcome for event {event_id} with trace {trace_id}")
        return outcome

# Singleton publisher instance
publisher = EventPublisher()
