import os
import sys

# Ensure the parent directory is available in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from financial_agent_core.planner import DeterministicPlanner
from tools.mock_db import DB


def interactive_shell():
    print("\n" + "=" * 50)
    print("SECURE FINANCIAL AI AGENT RUNTIME (DEV)")
    print("Policy-Driven Intelligence interface initialized.")
    print("=" * 50 + "\n")

    # Check for OpenAI API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("[ERROR] OPENAI_API_KEY environment variable is not set.")
        print("Please exit, set your terminal variable, and try again:")
        print("  Windows: $env:OPENAI_API_KEY='your-key-here'")
        print("  Mac/Linux: export OPENAI_API_KEY='your-key-here'")
        return

    planner = DeterministicPlanner()

    # Base context
    context = {"actor": "employee"}
    print(f"Current Context Actor: {context['actor']}\n")

    while True:
        try:
            import json

            print("\n" + "-" * 70)
            print("CURRENT MOCK DATABASE STATE:")
            print(json.dumps(DB, indent=2))
            print("-" * 70 + "\n")

            print("---")
            user_prompt = input("Enter test scenario (or 'quit' to exit): ")

            if user_prompt.lower() in ["quit", "exit", "q"]:
                break

            if not user_prompt.strip():
                continue

            print("\n--- Executing Planner Routing ---")

            # Reset context per run
            run_context = context.copy()
            # We enforce testing against acc_123 for now
            run_context["account_id"] = "acc_123"

            result = planner.handle_request(
                user_prompt=user_prompt, context=run_context
            )

            print("\n--- Execution Result ---")

            print(json.dumps(result, indent=2))

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n[X] Error during execution: {str(e)}")


if __name__ == "__main__":
    interactive_shell()
