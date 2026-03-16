# tasks/compliance_tasks.py
from crewai import Task


class ComplianceTasks:
    def check_compliance(self, agent, original_request, context_findings):
        return Task(
            description=f"""Review the findings from the Fraud and Risk assessments for the request: {original_request}.
            Ensure that all recommended actions follow BlueShield and 'Sentinel' security policies.
            Context Findings: {context_findings}""",
            expected_output="A final compliance verdict (COMPLIANT/NON-COMPLIANT) with reasoning.",
            agent=agent,
        )
