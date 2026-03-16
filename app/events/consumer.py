import asyncio
from typing import Optional
from app.events.models import PlatformEvent, EventStatus, EventType
from app.events.queue import event_queue
from app.events.lifecycle import lifecycle_manager
from app.events.dispatcher import dispatcher
from app.events.publisher import publisher
from app.intake.schemas import PlatformRequest
from app.control_plane.coordinator import ControlPlaneCoordinator

class EventConsumer:
    """
    The asynchronous worker that pulls events from the queue and processes them.
    This is the core execution loop of the event-driven platform.
    """
    def __init__(self):
        self.coordinator = ControlPlaneCoordinator()
        self._running = False

    async def start(self, once: bool = False):
        """
        Starts the consumption loop.
        """
        self._running = True
        print("[CONSUMER] Event worker started.")
        
        while self._running:
            event = event_queue.dequeue()
            if event:
                await self._process_event(event)
            else:
                if once:
                    break
                await asyncio.sleep(0.5)

    def stop(self):
        self._running = False
        print("[CONSUMER] Event worker stopping.")

    async def _process_event(self, event: PlatformEvent):
        """
        Executes the logic for a single event.
        """
        # 1. Update status
        lifecycle_manager.transition(event, EventStatus.PROCESSING)
        
        # 2. Dispatch to dedicated handler (if registered) or use default path
        # In Phase 6, we'll implement a default new_request handler
        if event.event_type == EventType.NEW_REQUEST:
            await self._handle_new_request(event)
        else:
            await dispatcher.dispatch(event)

    async def _handle_new_request(self, event: PlatformEvent):
        """
        The default processing path for platform requests.
        """
        try:
            # 1. Convert payload to PlatformRequest
            request_data = event.payload
            request = PlatformRequest(**request_data)
            
            print(f"[CONSUMER] Processing request {request.request_id} for event {event.event_id}")
            
            # 2. Execute control plane pipeline (sync call)
            decision = self.coordinator.process_request(request)
            
            # 3. Route lifecycle based on the ControlPlaneDecision
            if decision.block_reason or decision.validation_status == "FAILED":
                lifecycle_manager.transition(event, EventStatus.BLOCKED)
                result_type = "BLOCKED"
            elif decision.requires_review:
                lifecycle_manager.transition(event, EventStatus.REVIEW_PENDING)
                result_type = "REVIEW_REQUIRED"
            else:
                lifecycle_manager.transition(event, EventStatus.COMPLETED)
                result_type = "COMPLETED"
            
            # 4. Publish outcome event
            await publisher.publish_outcome(
                event_id=event.event_id,
                correlation_id=event.correlation_id,
                result=decision.model_dump(),
                trace_id=request.request_id
            )
            
            print(f"[CONSUMER] Event {event.event_id} resolved as: {result_type} (risk_score={decision.risk_score:.1f})")
            
        except Exception as e:
            print(f"[CONSUMER] ERROR processing event {event.event_id}: {str(e)}")
            lifecycle_manager.transition(event, EventStatus.FAILED)

# Singleton consumer instance
consumer = EventConsumer()
