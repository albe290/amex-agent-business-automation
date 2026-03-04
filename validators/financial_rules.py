from tools.mock_db import get_account


def check_financial_rules(action: str, context: dict) -> tuple[bool, str]:
    """
    Applies deterministic business rules before sentinel evaluation.
    This acts as a fast-fail mechanism.
    """
    account_id = context.get("account_id")
    amount = context.get("transaction_amount", 0.0)

    account_info = get_account(account_id)
    if not account_info:
        return False, f"Account {account_id} not found."

    account_type = account_info.get("type", "")

    # Rule 1: Transactions over $100k always require review, regardless of action
    if amount >= 100000:
        return False, "Transaction amounts >= $100,000 always require human review."

    # Rule 2: Cannot freeze Centurion context without manual approval
    if action == "freeze_account" and account_type == "Centurion":
        return False, "Cannot automatically freeze Centurion accounts."

    # Rule 3: Cannot perform actions on already frozen accounts (except unlock)
    if account_info.get("status") == "FROZEN" and action != "unlock_account":
        return (
            False,
            f"Account {account_id} is already FROZEN. Action {action} invalid.",
        )

    return True, "Passed financial rules"
