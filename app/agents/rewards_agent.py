# agents/rewards_agent.py
from crewai import Agent


class RewardsAgent:
    def get_agent(self):
        return Agent(
            role="Membership Rewards Concierge",
            goal="Analyze customer spending patterns to optimize rewards allocation and identify high-value customer opportunities.",
            backstory="""You focus on the 'Growth' side of BlueShield Financial. You analyze transactions 
            from a value perspective, identifying if a transaction qualifies for bonus points or if the customer 
            should be targeted for a premium card upgrade based on their high-value behavior.""",
            tools=[],  # In a real system: calculate_points_multiplier_tool
            verbose=True,
            allow_delegation=False,
        )
