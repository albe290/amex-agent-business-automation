from pydantic import BaseModel, Field


class ExtractedEntities(BaseModel):
    account_id: str | None = Field(None, description="The account ID if found")
    transaction_amount: str | None = Field(
        None, description="The transaction amount if found"
    )
    merchant_name: str | None = Field(None, description="The merchant name if found")


class IntentClassification(BaseModel):
    intent: str = Field(
        ...,
        description="The classified intent, e.g., 'fraud_triage', 'anomaly_detection', 'credit_underwriting'",
    )
    confidence: float = Field(..., description="Confidence score between 0.0 and 1.0")
    requires_human_verification: bool = Field(
        ...,
        description="Whether this request looks highly sensitive and needs human review before routing",
    )
    extracted_entities: ExtractedEntities = Field(
        ..., description="Specific data extracted from the prompt"
    )
