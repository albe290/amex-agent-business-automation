# agents/risk_agent.py
from crewai import Agent
from tools.credit_limit_tool import credit_check_tool, approve_credit_limit_tool
from tools.account_lookup_tool import account_lookup_tool


class RiskAgent:
    def get_agent(self):
        return Agent(
            role="Risk Assessment Analyst",
            goal="Evaluate the financial risk of transactions and credit requests.",
            backstory="""You are a senior risk analyst. You use credit data and transaction history 
            to determine whether a request should be approved or denied based on the customer's risk profile.
            You prioritize historical account health and "VIP/Centurion" status over the novelty of a single transaction. 
            You actively prevent unnecessary friction for high-net-worth individuals making standard purchases.""",
            tools=[credit_check_tool, approve_credit_limit_tool, account_lookup_tool],
            verbose=True,
            allow_delegation=False,
        )
