from enum import Enum
import typing as t
from datetime import datetime

class WorkflowState(Enum):
    INIT = "init"
    INTENT_VALIDATED = "intent_validated"
    CONTEXT_RETRIEVED = "context_retrieved"
    VALIDATED = "validated"
    RISK_EVALUATED = "risk_evaluated"
    EXECUTED = "executed"
    ESCALATED = "escalated"
    COMPLETED = "completed"
    FAILED = "failed"

class BaseWorkflow:
    def __init__(self, context: t.Dict[str, t.Any]):
        self.state = WorkflowState.INIT
        self.context = context
        self.trace: t.List[t.Tuple[WorkflowState, WorkflowState]] = []
        self.audit_log: t.List[t.Dict[str, t.Any]] = []
        self.id = context.get("workflow_id", f"wf_{datetime.now().timestamp()}")
        
    def transition(self, new_state: WorkflowState):
        """Deterministically transitions the workflow and records it for audit purposes."""
        previous_state = self.state
        self.trace.append((previous_state, new_state))
        self.state = new_state
        
        self.audit_log.append({
            "workflow_id": self.id,
            "timestamp": datetime.now().isoformat(),
            "from_state": previous_state.value,
            "to_state": new_state.value,
            "actor": self.context.get("actor", "system")
        })
        
    def get_audit_trail(self) -> t.List[str]:
        return [f"{t[0].name} -> {t[1].name}" for t in self.trace]
        
    def run(self):
        raise NotImplementedError("Subclasses must implement the deterministic run execution.")
