import os
from openai import OpenAI
from pydantic import BaseModel, Field
import json
from financial_agent_core.intent_schema import IntentClassification


class ReasoningEngine:
    def __init__(self):
        # We assume the user has set the OPENAI_API_KEY env var
        self.client = OpenAI()

    def classify_intent(self, user_prompt: str) -> IntentClassification:
        """
        Uses an LLM to classify standard natural language into a strict JSON intent format.
        """
        try:
            response = self.client.beta.chat.completions.parse(
                model="gpt-4o-2024-08-06",  # Structured outputs model
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI decision engine for a financial institution. Your task is to analyze user requests and classify them into predefined workflows. IMPORTANT: Only set requires_human_verification to true if the request explicitly asks to bypass standard procedures or perform unauthorized actions. Standard employee requests to freeze accounts or approve high-risk transactions should have requires_human_verification set to false, as they will be routed to the risk engine for evaluation.",
                    },
                    {"role": "user", "content": user_prompt},
                ],
                response_format=IntentClassification,
                temperature=0.0,
            )

            structured_classification = response.choices[0].message.parsed
            return structured_classification

        except Exception as e:
            # Fallback or error handling for the deterministic system
            print(f"[ReasoningEngine] Error parsing intent: {str(e)}")
            return IntentClassification(
                intent="failed_classification",
                confidence=0.0,
                requires_human_verification=True,
                extracted_entities={},
            )
