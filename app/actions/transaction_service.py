# services/transaction_service.py
import time
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional
from crew.financial_crew import FinancialCrew
from security.validator import SecurityValidator
from monitoring.metrics import log_execution_metrics, event_bus
from risk.scoring_engine import calculate_risk_score
from tools.audit_logger import log_audit


class TransactionRequest(BaseModel):
    account_id: str
    merchant_id: str
    amount: float
    actor: str = "employee"
    custom_prompt: Optional[str] = None


class TransactionResponse(BaseModel):
    status: str
    message: str
    latency: str


class TransactionService:
    def __init__(self):
        self.validator = SecurityValidator()

    def externalize_decision(self, decision: str) -> dict:
        """
        Decision Gateway: Protects internal fraud routing logic
        by translating internal risk decisions into safe external responses.
        """
        if decision == "APPROVE":
            return {"status": "approved", "message": "Transaction Approved"}

        if decision == "REVIEW":
            return {
                "status": "verification_required",
                "message": "Additional Verification Required",
            }

        return {"status": "declined", "message": "Transaction Unable to Process"}

    async def process(self, req: TransactionRequest) -> TransactionResponse:
        user_prompt = (
            req.custom_prompt
            if req.custom_prompt
            else f"Analyze transaction for {req.account_id} at {req.merchant_id} for ${req.amount}"
        )

        await event_bus.emit(
            "CASE_INITIALIZED",
            {
                "account_id": req.account_id,
                "merchant_id": req.merchant_id,
                "amount": req.amount,
            },
        )
        await event_bus.emit("SENTINEL_SCAN", {})

        # 1. Security Check
        is_safe, msg = self.validator.validate_prompt(user_prompt)
        if not is_safe:
            await event_bus.emit(
                "SENTINEL_BLOCK", {"reason": msg or "prompt_injection_detected"}
            )
            raise HTTPException(status_code=403, detail=f"Security Block: {msg}")

        await event_bus.emit("SENTINEL_ALLOW", {})
        await event_bus.emit("ORCHESTRATION_START", {})

        start_time = time.time()
        try:
            # 2. CrewAI Run
            transaction_data = req.dict()
            crew_engine = FinancialCrew(transaction_data)
            result = crew_engine.run()

            latency = time.time() - start_time

            # 3. Output Check
            is_output_safe, output_msg = self.validator.validate_output(str(result))

            log_execution_metrics(latency=latency, success=is_output_safe)

            # === DETERMINISTIC RISK SCORING ALGORITHM ===
            final_score = calculate_risk_score(transaction_data, str(result))

            if final_score >= 80:
                policy_decision = "APPROVE"
            elif final_score >= 50:
                policy_decision = "REVIEW"
            else:
                policy_decision = "BLOCK"

            await event_bus.emit(
                "ORCHESTRATION_COMPLETE",
                {
                    "result": str(result),
                    "final_score": final_score,
                    "policy_decision": policy_decision,
                },
            )

            # --- INTERNAL AUDIT & EXPLAINABILITY LAYER ---
            log_audit(transaction_data, final_score, policy_decision, str(result))

            # --- DECISION GATEWAY (EXTERNALIZATION) ---
            external_response = self.externalize_decision(policy_decision)

            return {
                "status": external_response["status"],
                "message": external_response["message"],
                "latency": f"{latency:.2f}s",
            }
        except Exception as e:
            log_execution_metrics(
                latency=time.time() - start_time, success=False, error=str(e)
            )
            raise HTTPException(status_code=500, detail=str(e))


transaction_service = TransactionService()
