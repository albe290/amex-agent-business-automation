# Event-Driven Architecture

The platform processes work through an asynchronous event-driven pipeline. This transforms it from a synchronous request-response system into a governed pipeline that can handle continuous work streams.

---

## Why Events?

A synchronous API ("send request, get response") is fine for one-at-a-time demos. Real financial platforms process thousands of cases per day, from multiple sources, with varying urgency.

An event-driven design provides:
- **Decoupling** — intake and processing are separate concerns
- **Asynchronous processing** — work is queued, not blocked
- **Lifecycle visibility** — every event has a trackable state
- **Retry readiness** — failed events can be requeued
- **Scale path** — maps directly to Kafka/SQS in production

---

## Event Lifecycle States

```
RECEIVED → QUEUED → PROCESSING → COMPLETED
                              ↘ REVIEW_PENDING
                              ↘ BLOCKED
                              ↘ FAILED
```

Every transition is recorded by `EventLifecycle` with a timestamp.

---

## Pipeline Components

### Producer (`app/events/producer.py`)
- Wraps incoming payloads into `IncomingEvent` objects
- Marks initial lifecycle state as `QUEUED`
- Places event into the `EventQueue`

### Queue (`app/events/queue.py`)
- Thread-safe in-memory FIFO queue
- Methods: `enqueue`, `dequeue`, `get_depth`, `peek_history`
- **Production mapping:** replace with Kafka topic or SQS queue

### Consumer (`app/events/consumer.py`)
- Async worker loop polling the queue
- Marks event as `PROCESSING`
- Passes payload through the full platform pipeline (Intake → Control Plane → Strategy)
- Updates lifecycle based on `ControlPlaneDecision`

### Dispatcher (`app/events/dispatcher.py`)
- Routes different `EventType` values to specific handlers
- `NEW_REQUEST` → full platform workflow
- `REVIEW_DECISION` → review completion handler
- Extensible: new event types can be registered without changing core logic

### Publisher (`app/events/publisher.py`)
- Emits `OutcomeEvent` after processing
- Sends to the central `event_bus` for real-time dashboard updates
- Outcome types: `COMPLETED`, `REVIEW_REQUIRED`, `BLOCKED`, `FAILED`

---

## Event Contracts

```python
class IncomingEvent(PlatformEvent):
    source: str         # API / batch / scheduled / fraud-alert
    event_type: EventType  = NEW_REQUEST

class OutcomeEvent(PlatformEvent):
    result_type: str    # COMPLETED / REVIEW_REQUIRED / BLOCKED
    trace_id: str       # Links back to original request_id
```

---

## Production Mapping

| Current Implementation | Production Equivalent |
|---|---|
| In-memory `EventQueue` | Kafka Topic / AWS SQS |
| Async `EventConsumer` loop | Kafka Consumer Group / Lambda |
| `EventPublisher` → `event_bus` | Kafka Producer → downstream topics |
| `EventLifecycle` dict | DynamoDB / Redis state store |

The architecture is designed so the in-memory components can be swapped for production infrastructure without changing the business logic layer.
