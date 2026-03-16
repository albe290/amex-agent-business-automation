from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum
import uuid

class EventType(str, Enum):
    NEW_REQUEST = "NEW_REQUEST"
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    REVIEW_DECISION = "REVIEW_DECISION"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"

class EventStatus(str, Enum):
    RECEIVED = "RECEIVED"
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    REVIEW_PENDING = "REVIEW_PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"

class PlatformEvent(BaseModel):
    """
    Base contract for all platform events.
    """
    event_id: str = Field(default_factory=lambda: f"EVT-{uuid.uuid4().hex[:8].upper()}")
    correlation_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    event_type: EventType
    status: EventStatus
    payload: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class IncomingEvent(PlatformEvent):
    """
    Represents work entering the system.
    """
    source: str = "API"

class OutcomeEvent(PlatformEvent):
    """
    Represents a final decision or result emitted by the system.
    """
    result_type: str  # e.g., "APPROVED", "REJECTED", "ESCALATED"
    trace_id: Optional[str] = None
