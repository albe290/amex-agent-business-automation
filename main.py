# main.py
import time
import sys
import os
from security.validator import SecurityValidator
from crew.financial_crew import FinancialCrew
from monitoring.metrics import log_execution_metrics


def main():
    print("\n" + "=" * 50)
    print("      BLUESHIELD SECURE FINANCIAL AGENT (CrewAI)")
    print("=" * 50 + "\n")

    # 1. Initialize Security Validator
    validator = SecurityValidator()

    # 2. Define Sample Transaction Case
    # In a real app, this would come from an API or User Input
    transaction_case = {
        "account_id": "acc_vip",
        "merchant_id": "M_999",  # Risky merchant
        "amount": 1500.0,
        "actor": "employee",
    }

    user_prompt = f"Investigate transaction for account {transaction_case['account_id']} at merchant {transaction_case['merchant_id']} for ${transaction_case['amount']}."

    # 3. Step 1: Sentinel Prompt Validation
    is_safe, msg = validator.validate_prompt(user_prompt)
    if not is_safe:
        print(f"\n[CRITICAL] System Blocked Execution: {msg}")
        sys.exit(1)

    # 4. Step 2: CrewAI Orchestration
    start_time = time.time()
    print("\n[Orchestration] Kicking off Financial Crew...")

    try:
        crew_engine = FinancialCrew(transaction_case)
        result = crew_engine.run()

        latency = time.time() - start_time
        print("\n" + "-" * 30)
        print("CREW EVALUATION COMPLETED")
        print(f"Latency: {latency:.2f}s")
        print("-" * 30)
        print(f"RESULT:\n{result}")

        # 5. Step 3: Sentinel Output Validation
        is_output_safe, output_msg = validator.validate_output(str(result))
        if not is_output_safe:
            print(f"\n[CRITICAL] Output Blocked: {output_msg}")

        # 6. Monitoring
        log_execution_metrics(latency=latency, success=is_output_safe)

    except Exception as e:
        print(f"\n[ERROR] Execution failed: {str(e)}")
        log_execution_metrics(
            latency=time.time() - start_time, success=False, error=str(e)
        )


if __name__ == "__main__":
    main()
