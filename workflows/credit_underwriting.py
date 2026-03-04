from workflows.base_workflow import BaseWorkflow, WorkflowState


class CreditUnderwritingWorkflow(BaseWorkflow):
    """
    Placeholder for the Credit Underwriting workflow.
    To be fully implemented in Phase 2.
    """

    def __init__(self, context):
        super().__init__(context)

    def run(self):
        self.transition(WorkflowState.COMPLETED)
        return {
            "workflow_id": self.id,
            "status": self.state.value,
            "decision": "NOT_IMPLEMENTED",
            "audit_trail": self.get_audit_trail(),
            "execution_metadata": {},
        }
