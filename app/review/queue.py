from typing import List, Dict, Optional
from app.review.models import ReviewPacket, ReviewQueueItem

class ReviewQueue:
    """
    In-memory management of the human review queue.
    Operational interface for enqueuing and retrieving review cases.
    """
    
    def __init__(self):
        self._queue: Dict[str, ReviewQueueItem] = {}
        self._packets: Dict[str, ReviewPacket] = {}

    def enqueue_review(self, packet: ReviewPacket, priority: int = 2):
        """
        Adds a new review case to the platform queue.
        """
        item = ReviewQueueItem(
            review_id=packet.review_id,
            request_id=packet.request_id,
            priority=priority,
            status="PENDING"
        )
        self._queue[packet.review_id] = item
        self._packets[packet.review_id] = packet

    def get_pending_reviews(self) -> List[ReviewQueueItem]:
        """
        Returns all cases currently awaiting human action.
        """
        return [item for item in self._queue.values() if item.status == "PENDING"]

    def get_packet(self, review_id: str) -> Optional[ReviewPacket]:
        """
        Retrieves the full evidence packet for a specific review case.
        """
        return self._packets.get(review_id)

    def update_status(self, review_id: str, status: str, assigned_to: Optional[str] = None):
        """
        Transitions a case through the review lifecycle.
        """
        if review_id in self._queue:
            item = self._queue[review_id]
            item.status = status
            if assigned_to:
                item.assigned_to = assigned_to
