# monitoring/token_monitor.py
from monitoring.metrics import metrics


class TokenMonitor:
    def __init__(self):
        self.total_tokens = 0

    def log_usage(self, model: str, prompt_tokens: int, completion_tokens: int):
        usage = prompt_tokens + completion_tokens
        self.total_tokens += usage
        print(f"[Monitoring] Token Usage Logged: {usage} total ({model})")
        # In a real app, this would hit a DB or Prometheus
        metrics.increment("total_tokens_used", usage)


monitor = TokenMonitor()
