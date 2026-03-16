from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

class PlatformRequest(BaseModel):
    """
    Standardized request object that flows through the entire AI platform.
    Ensures normalized intake regardless of the source.
    """
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    use_case_type: str = Field(..., description="The type of financial request (e.g., credit_limit_increase, fraud_check)")
    customer_context: Dict[str, Any] = Field(default_factory=dict, description="Basic customer profile data")
    business_payload: Dict[str, Any] = Field(..., description="The core transaction or request data")
    risk_metadata: Dict[str, Any] = Field(default_factory=dict, description="Pre-calculated risk signals from legacy systems")
    source: str = Field(default="api", description="Where the request originated (e.g., web_dashboard, mobile_app, batch_job)")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "json_schema_extra": {
            "example": {
                "use_case_type": "credit_limit_increase",
                "customer_context": {"id": "CUST-123", "tier": "gold"},
                "business_payload": {"requested_amount": 5000, "currency": "USD"},
                "risk_metadata": {"last_fraud_score": 12},
                "source": "mobile_app"
            }
        }
    }
