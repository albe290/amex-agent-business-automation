import time
import functools


class TelemetryTracer:
    """
    Simulates a distributed tracing system (like Jaeger or Datadog APM)
    to monitor agent latency and step execution times.
    """

    def __init__(self):
        self.traces = []

    def start_trace(self, span_name: str):
        print(f"[Telemetry] Starting trace: {span_name}")
        return time.time()

    def end_trace(self, span_name: str, start_time: float):
        duration = time.time() - start_time
        print(f"[Telemetry] Ended trace: {span_name} | Duration: {duration:.4f}s")
        self.traces.append({"span": span_name, "duration": duration})


tracer = TelemetryTracer()


def trace_execution(span_name: str):
    """Decorator to automatically trace a function's execution time."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = tracer.start_trace(span_name)
            result = func(*args, **kwargs)
            tracer.end_trace(span_name, start)
            return result

        return wrapper

    return decorator
