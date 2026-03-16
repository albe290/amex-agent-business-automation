from app.runtime.models import RuntimeState

class RetryPolicy:
    """
    Classifies errors and decides if a retry is permitted.
    """
    
    def __init__(self, max_retries: int = 2):
        self.max_retries = max_retries

    def should_retry(self, state: RuntimeState, error_code: str) -> bool:
        """
        Determines if an execution step should be retried based on the error.
        """
        if state.retries_used >= self.max_retries:
            return False
            
        # Classify retryable errors (transient) vs non-retryable (policy/boundary)
        retryable_codes = ["RETRIEVAL_TIMEOUT", "MODEL_PARSING_ERROR", "TRANSIENT_NETWORK_FAILURE"]
        
        return error_code in retryable_codes
