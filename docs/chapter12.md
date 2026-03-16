# Chapter 12: The Observation Deck (The `monitoring/` Layer)

## 1️⃣ Big Picture: The Observation Deck

Our factory is running at full speed. Robots are making decisions, humans are reviewing packets, and safety rails are preventing accidents. But as a factory owner, you don't want to walk to every room just to see how things are going. You want to sit in the **Observation Deck**.

Think of this as the "Mission Control" center. High above the factory floor, you have big screens that show you every move the robots make in real-time. If a robot in the Research Library finds a new fact, a light on your screen should blink.

In this chapter, we’ll meet the technology that powers these screens:
1.  **The Factory Heartbeat (`metrics.py`)**: A central system that pulses with every event in the factory and records how fast the robots are working.

---

## 2️⃣ Teach the Code

### 12.1 metrics.py – The Factory Heartbeat

How does a room in the "Context" layer send a message to the "Dashboard" layer without getting lost? It uses the **Event Bus**. The `metrics.py` file is our central communication hub.

### A. Full File Ingestion: `monitoring/metrics.py`

```python
14: class EventBus:
15:     """
16:     Async pub/sub event bus.
17:     Subscribers register async callbacks; events are broadcast to all of them.
18:     """
19:     def __init__(self):
20:         self._subscribers: List[Callable[[Dict[str, Any]], Coroutine[Any, Any, None]]] = []
21: 
22:     def subscribe(self, callback: Callable[[Dict[str, Any]], Coroutine[Any, Any, None]]):
23:         self._subscribers.append(callback)
...
28:     async def emit(self, event_type: str, data: Dict[str, Any]):
29:         payload = {"type": event_type, "data": data}
30:         for subscriber in list(self._subscribers):
31:             try:
32:                 await subscriber(payload)
33:             except Exception:
34:                 pass
...
38: event_bus = EventBus()
...
57: def log_execution_metrics(latency: float, success: bool, error: str = None):
58:     """
59:     Record execution telemetry for platform observability.
60:     """
61:     status = "SUCCESS" if success else "FAILURE"
62:     msg = f"[Metrics] Execution: status={status}, latency={latency:.3f}s"
...
66:     print(msg)
```

### B. File Purpose
The `metrics.py` file does two things:
1.  **Broadcasts News (`EventBus`)**: When something interesting happens (like a robot starting a task), the factory "Emits" an event. The Event Bus yells that news so that the Dashboard can hear it and update its graphs.
2.  **Records History (`log_execution_metrics`)**: It logs how long each task takes (latency) so we can see if our factory is getting slower over time.

### C. Line-by-Line Explanation

**Line 14: `class EventBus:`**
*   **The Radio Station:** This is the station that broadcasts factory news.
*   **Line 22 (`subscribe`):** This is how a "Listener" (like our Dashboard) tunes in to the station.
*   **Line 28 (`emit`):** This is how a "Reporter" (a robot) sends news to the station to be broadcast.

**Line 38: `event_bus = EventBus()`**
*   **The Singleton:** We only ever want ONE radio station for the whole factory. This line creates that one central station.

**Line 41: `sync_broadcast_event(...)`**
*   **The Quick Shout:** Sometimes a robot is in a rush and can't wait for the full async system. This helper function allows them to "Shout" a message to the bus quickly.

**Line 57: `log_execution_metrics(...)`**
*   **The Stopwatch Log:** Every time a major mission finishes, we call this to record the final result.
*   **Line 63 (`latency`):** Records exactly how many seconds it took. If it took 10 seconds, and it usually takes 2, we know we have a problem in the pipes!

---

### 🏁 Friendly Recap (The Observation Deck)

You've just learned how we **Monitor the Factory**!

You now understand:
1.  How the **Event Bus** broadcasts live news to our screens.
2.  Why we **Subscribe** to events to see them on the dashboard.
3.  How **Execution Metrics** tell us if our factory is healthy or slowing down.

**We can watch the factory, but how do we protect it from attackers? We're heading to the "Guard Towers"—the `security/` layer—next!**
