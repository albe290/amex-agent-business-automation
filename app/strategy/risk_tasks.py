# tasks/risk_tasks.py
from crewai import Task


class RiskTasks:
    def assess_risk(self, agent, transaction_data):
        return Task(
            description=f"""Evaluate the credit risk for account {transaction_data.get('account_id')} 
            considering the requested transaction amount of ${transaction_data.get('amount')}. 
            Check the account's credit score and determine if the limit increase or transaction should be allowed.""",
            expected_output="A detailed risk assessment and recommendation (ALLOW/DENY) based on credit data.",
            agent=agent,
        )
