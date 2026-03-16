import re
from typing import Tuple

class ControlPlaneValidator:
    """
    Sanity and Security layer for the Control Plane.
    Checks for prompt injection, sensitive data leakage, and MITRE ATLAS patterns.
    """
    
    @staticmethod
    def validate_input(content: str) -> Tuple[bool, str]:
        """
        Scan input for malicious patterns or policy violations.
        """
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
            if re.search(pattern, content, re.IGNORECASE):
                return False, f"Rule Violation: Potential malicious pattern detected ('{pattern}')"

        # Check for PII or sensitive patterns in intake
        sensitive_patterns = [r"ssn", r"password", r"secret_key"]
        for pattern in sensitive_patterns:
            if re.search(pattern, content.lower(), re.IGNORECASE):
                return False, "Privacy Violation: Sensitive PII detected in input"

        return True, "Success"

    @staticmethod
    def validate_output(result: str) -> Tuple[bool, str]:
        """
        Scan agent output for sensitive data leakage.
        """
        sensitive_patterns = [r"ssn", r"password", r"secret_key"]
        for pattern in sensitive_patterns:
            if re.search(pattern, result.lower(), re.IGNORECASE):
                return False, "Data Leakage: Sensitive patterns detected in output"
        
        return True, "Success"
