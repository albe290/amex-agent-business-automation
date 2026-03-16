# risk/policy_loader.py
import sys
import yaml
import os


def load_policy():
    policy_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "config", "policy.yaml")
    )

    if not os.path.exists(policy_path):
        print(f"[!] Warning: policy.yaml not found at {policy_path}")
        return {}

    with open(policy_path, "r") as f:
        try:
            return yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            print(f"[!] Error parsing policy.yaml: {e}")
            return {}


POLICY = load_policy()
