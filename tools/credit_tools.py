from tools.mock_db import DB, get_account


def run_credit_check(account_id: str) -> dict:
    """Simulates running a credit check for an account."""
    account = get_account(account_id)
    if not account:
        return {"success": False, "message": f"Account {account_id} not found."}

    score = (
        750
        if account["type"] in ["Centurion", "Corporate", "Business Platinum"]
        else 680
    )
    return {
        "success": True,
        "credit_score": score,
        "message": f"Credit check completed for {account_id}",
    }


def approve_credit_limit(account_id: str, requested_amount: float) -> dict:
    """Approves a credit limit increase."""
    account = get_account(account_id)
    if not account:
        return {"success": False, "message": f"Account {account_id} not found."}

    # In a real system, this would mutate a credit_limit field in the DB.
    # For now, we simulate success if the account is ACTIVE.
    if account["status"] != "ACTIVE":
        return {
            "success": False,
            "message": f"Cannot approve limit increase for {account['status']} account.",
        }

    return {
        "success": True,
        "message": f"Approved credit limit increase of ${requested_amount} for {account_id}.",
    }


def deny_credit(account_id: str, reason: str) -> dict:
    """Officially logs a credit denial."""
    # In a real system, this might send an email or log an adverse action notice.
    return {"success": True, "message": f"Credit denied for {account_id}: {reason}"}
