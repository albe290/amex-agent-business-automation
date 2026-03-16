# security/tool_guard.py
from security.compliance_validator import check_compliance_constraints


class ToolGuard:
    """
    Middleware that intercept tool calls to ensure they are safe
    and follow corporate policy BEFORE they reach the real tool logic.
    """

    def check_call(self, tool_name: str, args: dict, actor: str = "agent"):
        print(f"[Sentinel Tool Guard] Intercepting call: {tool_name} with args: {args}")

        # Cross-reference with compliance validator
        is_safe, msg = check_compliance_constraints(tool_name, {"actor": actor, **args})

        if not is_safe:
            print(f"[Sentinel Tool Guard] BLOCK: {msg}")
            return False, msg

        print(f"[Sentinel Tool Guard] ALLOW: {tool_name} is cleared for execution.")
        return True, "Cleared"


# Singleton instance
guard = ToolGuard()
