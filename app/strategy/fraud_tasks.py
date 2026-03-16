# tasks/fraud_tasks.py
from crewai import Task


class FraudTasks:
    def detect_fraud(self, agent, transaction_data):
        return Task(
            description=f"""Analyze the transaction for account {transaction_data.get('account_id')} 
            involving merchant {transaction_data.get('merchant_id')}. 
            Identify if the merchant or transaction pattern is suspicious. 
            CRITICAL INSTRUCTION: First, look up the account status and tier. If the account is an Elite tier (e.g., Centurion) and the merchant is SAFE, you must ALLOW the transaction and DO NOT freeze the account. 
            ONLY use the account freezing tool if the account is already DELINQUENT, the merchant is HIGH_RISK, or there is undeniable evidence of fraud.""",
            expected_output="A report on transaction safety and any actions taken (e.g., account frozen).",
            agent=agent,
        )
