from tools.mock_db import DB, get_account


def process_refund(account_id: str, amount: float, transaction_id: str) -> dict:
    """Simulates refunding a transaction amount to an account's balance."""
    account = get_account(account_id)
    if not account:
        return {"success": False, "message": f"Account {account_id} not found."}

    if account["status"] == "FROZEN":
        return {
            "success": False,
            "message": f"Cannot process refund for frozen account {account_id}.",
        }

    account["balance"] -= amount  # Decrease outstanding balance
    return {
        "success": True,
        "new_balance": account["balance"],
        "message": f"Refund of {amount} processed for tx {transaction_id}.",
    }


def validate_merchant(merchant_id: str) -> dict:
    """Checks if a merchant is on a known fraud list."""
    # Hardcoded mock simulation
    risky_merchants = ["M_999", "M_666", "CRYPTO_EXCHANGE"]
    is_safe = merchant_id not in risky_merchants
    status = "SAFE" if is_safe else "HIGH_RISK"

    return {"success": True, "merchant_status": status, "is_safe": is_safe}


def reverse_transaction(account_id: str, transaction_id: str) -> dict:
    """Completely reverses an unauthorized transaction."""
    # Very similar to process_refund in the mock DB, but semantically different intent.
    return {
        "success": True,
        "message": f"Reversed unauthorized transaction {transaction_id} for {account_id}.",
    }
