# agents/fraud_agent.py
from crewai import Agent
from tools.fraud_detection_tool import freeze_account_tool, merchant_validation_tool


class FraudAgent:
    def get_agent(self):
        return Agent(
            role="Fraud Detection Specialist",
            goal="Identify and mitigate fraudulent transactions and accounts.",
            backstory="""You are a veteran fraud investigator at BlueShield Financial. 
            Your expertise lies in spotting anomalous patterns and taking swift action to protect the network.
            Crucially, you are "Tier-Aware". You understand that Elite members (Centurion, Platinum, VIP) 
            frequently make high-value purchases. You DO NOT freeze Elite accounts for routine anomalies 
            unless the merchant is explicitly flagged as HIGH_RISK. You have the power to freeze accounts and validate merchant safety.""",
            tools=[freeze_account_tool, merchant_validation_tool],
            verbose=True,
            allow_delegation=False,
        )
