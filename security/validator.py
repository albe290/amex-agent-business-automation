# security/validator.py
import re
from security.policy_engine import PolicyEngine
from security.compliance_validator import check_compliance_constraints
from monitoring.metrics import sync_broadcast_event


class SecurityValidator:
    """
    Sentinel-based security layer that wraps the CrewAI orchestration.
    """

    def __init__(self):
        self.policy_engine = PolicyEngine()

    def validate_prompt(self, user_request: str):
        """
        Scan input for prompt injection, adversarial patterns, or policy violations.
        """
        sync_broadcast_event("SENTINEL_SCAN", {"status": "STARTING", "phase": "PROMPT"})

        # Basic injection detection
        injection_patterns = [
            r"ignore previous instructions",
            r"system prompt",
            r"override policy",
            r"ignore all amex protocols",
            r"bypass.*tool",
            r"internal system credentials",
            r"print.*account balance",
        ]
        for pattern in injection_patterns:
            if re.search(pattern, user_request, re.IGNORECASE):
                print(f"[Sentinel] BLOCK: Prompt injection detected.")
                sync_broadcast_event(
                    "SENTINEL_BLOCK", {"reason": "prompt_injection", "phase": "PROMPT"}
                )
                return False, "Prompt injection detected."

        # Policy-based validation
        is_safe, msg = check_compliance_constraints(
            "user_input", {"content": user_request, "actor": "employee"}
        )
        if not is_safe:
            print(f"[Sentinel] BLOCK: {msg}")
            sync_broadcast_event(
                "SENTINEL_BLOCK", {"reason": "compliance_violation", "phase": "PROMPT"}
            )
            return False, msg

        print("[Sentinel] ALLOW: Prompt passed initial security scan.")
        sync_broadcast_event("SENTINEL_ALLOW", {"phase": "PROMPT"})
        return True, "Success"

    def validate_output(self, result: str):
        """
        Scan agent output for sensitive data leakage or unapproved recommendations.
        """
        sync_broadcast_event("SENTINEL_SCAN", {"status": "STARTING", "phase": "OUTPUT"})

        # Check for PII or sensitive patterns
        sensitive_patterns = [r"ssn", r"password", r"secret_key"]
        for pattern in sensitive_patterns:
            if re.search(pattern, result.lower(), re.IGNORECASE):
                print(f"[Sentinel] BLOCK: Sensitive data detected in output.")
                sync_broadcast_event(
                    "SENTINEL_BLOCK", {"reason": "pii_leak", "phase": "OUTPUT"}
                )
                return False, "Sensitive data detected in output."

        print("[Sentinel] ALLOW: Output passed final security scan.")
        sync_broadcast_event("SENTINEL_ALLOW", {"phase": "OUTPUT"})
        return True, "Success"
