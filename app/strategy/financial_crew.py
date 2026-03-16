# crew/financial_crew.py
from crewai import Crew, Process, Task
from agents.fraud_agent import FraudAgent
from agents.risk_agent import RiskAgent
from agents.compliance_agent import ComplianceAgent
from agents.summary_agent import SummaryAgent
from agents.dispute_agent import DisputeAgent
from agents.rewards_agent import RewardsAgent
from tasks.fraud_tasks import FraudTasks
from tasks.risk_tasks import RiskTasks
from tasks.compliance_tasks import ComplianceTasks
from monitoring.metrics import sync_broadcast_event
import time


class FinancialCrew:
    def __init__(self, transaction_data):
        self.transaction_data = transaction_data

    def run(self):
        # Initialize 6-Agent Assembly
        fraud_agent = FraudAgent().get_agent()
        risk_agent = RiskAgent().get_agent()
        dispute_agent = DisputeAgent().get_agent()
        rewards_agent = RewardsAgent().get_agent()
        compliance_agent = ComplianceAgent().get_agent()
        summary_agent = SummaryAgent().get_agent()

        # Initialize Task Engines
        fraud_task_engine = FraudTasks()
        risk_task_engine = RiskTasks()
        compliance_task_engine = ComplianceTasks()

        # Define Tasks
        fraud_task = fraud_task_engine.detect_fraud(fraud_agent, self.transaction_data)
        risk_task = risk_task_engine.assess_risk(risk_agent, self.transaction_data)

        # Compliance task depends on the findings of others
        compliance_task = compliance_task_engine.check_compliance(
            compliance_agent,
            str(self.transaction_data),
            "Findings from the Fraud and Risk assessments.",
        )
        compliance_task.context = [fraud_task, risk_task]

        # Summary task to consolidate everything and output strictly formatted JSON
        summary_task = Task(
            description="""
Provide a final executive summary of the transaction investigation, rewards opportunities, and compliance status.

You must analyze the findings and return the result STRICTLY as valid JSON. Do not include any markdown wrappers (like ```json), explanations, or conversational text. Output ONLY the JSON object.

Required format:
{
  "fraud_detected": true | false,
  "risk_level": "low" | "medium" | "high",
  "recommended_action": "approve" | "review" | "freeze" | "deny",
  "reason": "Short, professional explanation of the decision."
}
""",
            expected_output="Valid JSON string containing fraud_detected, risk_level, recommended_action, and reason.",
            agent=summary_agent,
            context=[compliance_task],
        )

        # Define the Orchestration Callback
        def crew_step_callback(step_output):
            try:
                # 1. Normalize step_output to a list
                steps = step_output if isinstance(step_output, list) else [step_output]

                for step in steps:
                    # 2. Extract Agent Name
                    agent_name = "BlueShield Agent"
                    if hasattr(step, "agent"):
                        raw_agent = step.agent
                        if isinstance(raw_agent, str):
                            agent_name = raw_agent
                        else:
                            agent_name = getattr(
                                raw_agent,
                                "role",
                                getattr(raw_agent, "name", "BlueShield Agent"),
                            )

                    # 3. Extract Thought / Action
                    thought = getattr(step, "thought", "")

                    # 4. Filter out internal noise
                    if not thought or "Failed to parse LLM response" in thought:
                        continue

                    # 5. Robust Tool Extraction
                    tool = "N/A"
                    # Check direct attributes
                    for attr in ["tool", "tool_name", "tool_used"]:
                        val = getattr(step, attr, None)
                        if val and isinstance(val, str):
                            tool = val
                            break

                    # Check nested action object (common in AgentStep)
                    if tool == "N/A" and hasattr(step, "action"):
                        action = step.action
                        tool = getattr(action, "tool", "N/A")

                    # 6. Build Display Thought
                    display_thought = thought
                    if tool and tool != "N/A":
                        # If the AI is using a tool, make it explicit in the dash
                        sync_broadcast_event(
                            "TOOL_EXECUTION",
                            {"tool_name": tool, "agent": str(agent_name)},
                        )

                        if not thought or len(thought) < 5:
                            display_thought = f"Executing tool: {tool}"
                        else:
                            display_thought = f"{thought} (Tool: {tool})"
                    elif not thought or len(thought) < 5:
                        display_thought = "Processing investigative step..."

                    sync_broadcast_event(
                        "ORCHESTRATION_STEP",
                        {
                            "agent": str(agent_name),
                            "thought": display_thought,
                            "tool": tool,
                            "status": "IN_PROGRESS",
                        },
                    )
            except Exception as e:
                # print(f"DEBUG: Callback error: {e}") # Uncomment if debugging locally
                pass

        # Create Crew with full 6-agent hierarchy
        crew = Crew(
            agents=[
                fraud_agent,
                risk_agent,
                dispute_agent,
                rewards_agent,
                compliance_agent,
                summary_agent,
            ],
            tasks=[
                fraud_task,
                risk_task,
                compliance_task,
                summary_task,
            ],
            process=Process.sequential,
            verbose=True,
            step_callback=crew_step_callback,
            cache=False,
        )

        # Start Crew Execution
        result = crew.kickoff()
        return result
