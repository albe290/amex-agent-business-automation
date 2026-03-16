def check_compliance_constraints(action: str, context: dict) -> tuple[bool, str]:
    """
    Validates the action against overarching banking compliance regulations.
    These are non-negotiable checks that override LLM intent.
    """

    actor = context.get("actor", "unknown")

    # Rule 1: Only internal employees can trigger account freezes.
    # Customers cannot autonomously freeze another account.
    if action == "freeze_account" and actor != "employee":
        return (
            False,
            "Compliance Violation: Account freezes must be initiated by an authorized employee.",
        )

    # Rule 2: Escalations require a valid reason string
    if action == "create_escalation_ticket":
        reason = context.get("reason", "")
        if len(reason) < 10:
            return (
                False,
                "Compliance Violation: Escalations must include a descriptive reason (min 10 chars).",
            )

    return True, "Passed compliance checks"
