# agents/dispute_agent.py
from crewai import Agent


class DisputeAgent:
    def get_agent(self):
        return Agent(
            role="Transaction Dispute Specialist",
            goal="Investigate and resolve customer-initiated transaction disputes and chargebacks.",
            backstory="""You are an expert in consumer protection and dispute resolution. 
            You review merchant evidence and customer claims to determine if a chargeback is valid.
            You work closely with the Fraud agent to ensure disputes aren't actually undetected fraud.""",
            tools=[],  # In a real system: get_dispute_history_tool
            verbose=True,
            allow_delegation=True,
        )
