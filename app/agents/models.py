from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class AnalystOutput(BaseModel):
    """
    Structured output schema for the Analyst Agent.
    """
    agent_name: str = "analyst_agent"
    findings: List[str] = Field(..., description="Key anomalies or patterns detected")
    confidence: float = Field(..., ge=0, le=1)
    supporting_evidence: List[Dict[str, Any]] = Field(default_factory=list)
    recommended_path: str = Field(..., description="The agent's suggested next step")

class WriterOutput(BaseModel):
    """
    Structured output schema for the Writer Agent.
    """
    agent_name: str = "writer_agent"
    final_recommendation: str
    rationale: str
    risk_summary: str
