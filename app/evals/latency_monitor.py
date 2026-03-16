# monitoring/latency_monitor.py
import time
from monitoring.metrics import metrics


class LatencyMonitor:
    def __init__(self):
        self.start_times = {}

    def start_timer(self, key: str):
        self.start_times[key] = time.time()

    def stop_timer(self, key: str):
        if key in self.start_times:
            duration = time.time() - self.start_times[key]
            print(f"[Monitoring] Latency for {key}: {duration:.2f}s")
            metrics.increment(f"latency_{key}_ms", int(duration * 1000))
            return duration
        return 0


monitor = LatencyMonitor()
