class MetricsRegistry:
    """
    A simple in-memory metrics registry to track agent performance,
    Sentinel intervention rates, and API usage.
    """

    def __init__(self):
        self.counters = {
            "api_requests_total": 0,
            "agent_decisions_allow": 0,
            "agent_decisions_block": 0,
            "agent_decisions_review": 0,
            "fraud_escalations": 0,
            "credit_escalations": 0,
        }

    def increment(self, metric_name: str, amount: int = 1):
        if metric_name in self.counters:
            self.counters[metric_name] += amount

    def get_metrics(self) -> dict:
        return self.counters


# Global registry instance
metrics = MetricsRegistry()
