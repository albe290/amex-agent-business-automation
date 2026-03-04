import json
import os
import datetime

AUDIT_LOG_FILE = "audit_log.json"


def log_action(workflow_id: str, actor: str, action: str, decision: str, context: dict):
    """
    Securely log every action, sentinel verdict, and context used by the agent.
    """
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "workflow_id": workflow_id,
        "actor": actor,
        "action_attempted": action,
        "sentinel_decision": decision,
        "agent_context": context,
    }

    # In a real system, this would write to a secure SIEM or append-only database.
    # For this project, we append to a local JSONL file.

    mode = "a" if os.path.exists(AUDIT_LOG_FILE) else "w"
    with open(AUDIT_LOG_FILE, mode) as f:
        f.write(json.dumps(log_entry) + "\n")

    return True
