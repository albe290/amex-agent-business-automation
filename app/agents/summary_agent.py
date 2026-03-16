# agents/summary_agent.py
from crewai import Agent


class SummaryAgent:
    def get_agent(self):
        return Agent(
            role="Financial Case Summarizer",
            goal="Synthesize the findings from fraud, risk, and compliance into a clear final recommendation.",
            backstory="""You are an expert communicator at BlueShield Financial who can take complex technical findings 
            and distill them into actionable business intelligence. You consolidate the work of 
            the specialists into a final executive summary.""",
            tools=[],
            verbose=True,
            allow_delegation=False,
        )
