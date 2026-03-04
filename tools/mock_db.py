# tools/mock_db.py
import datetime

# A simple in-memory dictionary acting as our simulated Core Banking System / CRM
DB = {
    "accounts": {
        "acc_123": {
            "status": "ACTIVE",
            "balance": 5000.00,
            "owner": "John Doe",
            "type": "Personal",
        },
        "acc_999": {
            "status": "FROZEN",
            "balance": 150.00,
            "owner": "Jane Smith",
            "type": "Personal",
        },
        "acc_456": {
            "status": "ACTIVE",
            "balance": 125000.00,
            "owner": "Acme Corp",
            "type": "Corporate",
        },
        "acc_789": {
            "status": "REVIEW",
            "balance": -450.00,
            "owner": "Bob Wilson",
            "type": "Personal",
        },
        "acc_VIP": {
            "status": "ACTIVE",
            "balance": 950000.00,
            "owner": "Alice Rich",
            "type": "Centurion",
        },
        "acc_246": {
            "status": "FRAUD_HOLD",
            "balance": 0.00,
            "owner": "Tech Startup LLC",
            "type": "Business Gold",
        },
        "acc_135": {
            "status": "ACTIVE",
            "balance": 1250.00,
            "owner": "Charlie Brown",
            "type": "Everyday Preferred",
        },
        "acc_864": {
            "status": "DELINQUENT",
            "balance": 8450.00,
            "owner": "Diana Prince",
            "type": "Personal Platinum",
        },
        "acc_007": {
            "status": "ACTIVE",
            "balance": 4500000.00,
            "owner": "James Bond",
            "type": "Centurion",
        },
        "acc_555": {
            "status": "REVIEW",
            "balance": 45000.00,
            "owner": "Global Imports Inc",
            "type": "Corporate Green",
        },
        "acc_BCE": {
            "status": "ACTIVE",
            "balance": 2100.50,
            "owner": "Peter Parker",
            "type": "Blue Cash Everyday",
        },
        "acc_DELTA": {
            "status": "ACTIVE",
            "balance": 15600.00,
            "owner": "Tony Stark",
            "type": "Delta SkyMiles Reserve",
        },
        "acc_HILTON": {
            "status": "ACTIVE",
            "balance": 3200.75,
            "owner": "Logan Howlett",
            "type": "Hilton Honors Aspire",
        },
        "acc_MARRIOTT": {
            "status": "ACTIVE",
            "balance": 8900.00,
            "owner": "Bruce Wayne",
            "type": "Marriott Bonvoy Brilliant",
        },
        "acc_BIZ_PLAT": {
            "status": "ACTIVE",
            "balance": 250000.00,
            "owner": "Wayne Enterprises",
            "type": "Business Platinum",
        },
    },
    "escalation_tickets": [],
}


def get_account(account_id: str) -> dict:
    return DB["accounts"].get(account_id)


def update_account_status(account_id: str, new_status: str) -> bool:
    if account_id in DB["accounts"]:
        DB["accounts"][account_id]["status"] = new_status
        return True
    return False


def add_escalation_ticket(ticket: dict) -> str:
    ticket_id = f"TKT-{len(DB['escalation_tickets']) + 1}-{int(datetime.datetime.now().timestamp())}"
    ticket["ticket_id"] = ticket_id
    ticket["created_at"] = datetime.datetime.now().isoformat()
    DB["escalation_tickets"].append(ticket)
    return ticket_id


def reset_db():
    """Resets the in-memory database to its initial state."""
    global DB
    # Deep copy the initial state (hardcoded here for simplicity)
    DB["accounts"] = {
        "acc_123": {
            "status": "ACTIVE",
            "balance": 5000.00,
            "owner": "John Doe",
            "type": "Personal",
        },
        "acc_999": {
            "status": "FROZEN",
            "balance": 150.00,
            "owner": "Jane Smith",
            "type": "Personal",
        },
        "acc_456": {
            "status": "ACTIVE",
            "balance": 125000.00,
            "owner": "Acme Corp",
            "type": "Corporate",
        },
        "acc_789": {
            "status": "REVIEW",
            "balance": -450.00,
            "owner": "Bob Wilson",
            "type": "Personal",
        },
        "acc_VIP": {
            "status": "ACTIVE",
            "balance": 950000.00,
            "owner": "Alice Rich",
            "type": "Centurion",
        },
        "acc_246": {
            "status": "FRAUD_HOLD",
            "balance": 0.00,
            "owner": "Tech Startup LLC",
            "type": "Business Gold",
        },
        "acc_135": {
            "status": "ACTIVE",
            "balance": 1250.00,
            "owner": "Charlie Brown",
            "type": "Everyday Preferred",
        },
        "acc_864": {
            "status": "DELINQUENT",
            "balance": 8450.00,
            "owner": "Diana Prince",
            "type": "Personal Platinum",
        },
        "acc_007": {
            "status": "ACTIVE",
            "balance": 4500000.00,
            "owner": "James Bond",
            "type": "Centurion",
        },
        "acc_555": {
            "status": "REVIEW",
            "balance": 45000.00,
            "owner": "Global Imports Inc",
            "type": "Corporate Green",
        },
        "acc_BCE": {
            "status": "ACTIVE",
            "balance": 2100.50,
            "owner": "Peter Parker",
            "type": "Blue Cash Everyday",
        },
        "acc_DELTA": {
            "status": "ACTIVE",
            "balance": 15600.00,
            "owner": "Tony Stark",
            "type": "Delta SkyMiles Reserve",
        },
        "acc_HILTON": {
            "status": "ACTIVE",
            "balance": 3200.75,
            "owner": "Logan Howlett",
            "type": "Hilton Honors Aspire",
        },
        "acc_MARRIOTT": {
            "status": "ACTIVE",
            "balance": 8900.00,
            "owner": "Bruce Wayne",
            "type": "Marriott Bonvoy Brilliant",
        },
        "acc_BIZ_PLAT": {
            "status": "ACTIVE",
            "balance": 250000.00,
            "owner": "Wayne Enterprises",
            "type": "Business Platinum",
        },
    }
    DB["escalation_tickets"] = []
