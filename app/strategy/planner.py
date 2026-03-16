from typing import List, Dict, Any
from app.strategy.router import StrategyPath

class TaskPlan(str):
    """
    Represents a concrete plan of action for the platform.
    """
    pass

class StrategyPlanner:
    """
    Translates a StrategyPath into a discrete set of agentic or procedural tasks.
    Acts as the bridge between governance and work.
    """
    
    @staticmethod
    def build_plan(path: StrategyPath, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Maps the selected path to a specific sequence of operations.
        """
        if path == StrategyPath.BLOCK:
            return [{"step": "terminate", "action": "send_block_notification"}]
        
        if path == StrategyPath.AUTOMATE:
            return [
                {"step": "analysis", "agent": "analyst_agent", "mode": "light"},
                {"step": "output", "action": "generate_auto_response"}
            ]
            
        if path == StrategyPath.INVESTIGATE:
            return [
                {"step": "evidence_gathering", "agent": "analyst_agent", "mode": "deep"},
                {"step": "recommendation", "agent": "writer_agent"},
                {"step": "final_check", "action": "generate_audit_report"}
            ]
            
        if path == StrategyPath.ESCALATE:
            return [
                {"step": "evidence_gathering", "agent": "analyst_agent", "mode": "deep"},
                {"step": "escalation_packet", "action": "prepare_review_logic"},
                {"step": "notify", "action": "alert_human_ovveride"}
            ]
            
        return [{"step": "unknown", "action": "log_error"}]
