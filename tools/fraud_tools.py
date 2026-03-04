# tools/fraud_tools.py
from tools.mock_db import get_account, update_account_status


def freeze_account(account_id: str) -> dict:
    """
    Concrete tool execution function.
    Interacts with the simulated Core Banking System to update the account status.
    """
    account = get_account(account_id)
    if not account:
        return {
            "success": False,
            "error_msg": f"Account {account_id} not found in system.",
        }

    if account["status"] == "FROZEN":
        return {"success": True, "message": f"Account {account_id} is already frozen."}

    success = update_account_status(account_id, "FROZEN")
    if success:
        return {
            "success": True,
            "message": f"Account {account_id} successfully frozen.",
        }
    return {"success": False, "error_msg": f"Failed to update status for {account_id}."}
