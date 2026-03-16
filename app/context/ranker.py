from typing import List
from app.context.models import RetrievedEvidence

class EvidenceRanker:
    """
    Sorts and filters retrieved evidence to ensure context quality.
    """
    
    def rank_and_filter(self, evidence: List[RetrievedEvidence], top_k: int = 5) -> List[RetrievedEvidence]:
        """
        Sorts evidence by relevance score and trims to top_k.
        """
        # 1. Sort by score
        sorted_evidence = sorted(evidence, key=lambda x: x.relevance_score, reverse=True)
        
        # 2. Filter out duplicates or extremely low scores (threshold mock)
        filtered = [e for e in sorted_evidence if e.relevance_score > 0.5]
        
        # 3. Trim to Top K
        return filtered[:top_k]
