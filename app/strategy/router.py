from enum import Enum
from typing import Optional
from pydantic import BaseModel

class StrategyPath(str, Enum):
    AUTOMATE = "AUTOMATE"       # Low risk, fully automated approval/action
    INVESTIGATE = "INVESTIGATE" # Medium risk, requires AI agent deep dive
    SUMMARIZE = "SUMMARIZE"     # High volume, requires quick AI summary
    ESCALATE = "ESCALATE"       # High risk, human review requested immediately
    BLOCK = "BLOCK"             # Extreme risk or policy failure

from app.control_plane.decision import ControlPlaneDecision

class StrategyRouter:
    """
    Deterministic logic to decide which agentic or procedural path to follow.
    Signals a "Decision" based on Intake and Control Plane inputs.
    """
    @staticmethod
    def select_path(decision: ControlPlaneDecision) -> StrategyPath:
        if decision.validation_status == "FAILED":
            return StrategyPath.BLOCK
        
        if decision.requires_review:
            return StrategyPath.ESCALATE

        if decision.risk_score < 20:
            return StrategyPath.AUTOMATE
        elif decision.risk_score < 70:
            return StrategyPath.INVESTIGATE
        else:
            return StrategyPath.ESCALATE
