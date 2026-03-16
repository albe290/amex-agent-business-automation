from typing import Dict, Any
from collections import Counter

class OnlineEvalTracker:
    """
    Lightweight tracker for live platform performance signals.
    """
    
    def __init__(self):
        self.strategy_counts = Counter()
        self.review_count = 0
        self.total_count = 0
        self.policy_hits = Counter()

    def track_execution(self, strategy: str, requires_review: bool, policy_hits: list):
        """
        Records results of a live platform request.
        """
        self.total_count += 1
        self.strategy_counts[strategy] += 1
        if requires_review:
            self.review_count += 1
        for hit in policy_hits:
            self.policy_hits[hit] += 1

    def get_operational_summary(self) -> Dict[str, Any]:
        """
        Returns a summary of live behavior patterns.
        """
        if self.total_count == 0:
            return {"status": "NO_DATA"}
            
        return {
            "total_requests": self.total_count,
            "automation_rate": self.strategy_counts.get("AUTOMATE", 0) / self.total_count,
            "review_rate": self.review_count / self.total_count,
            "most_frequent_policy": self.policy_hits.most_common(1)[0] if self.policy_hits else None
        }
