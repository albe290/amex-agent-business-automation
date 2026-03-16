# Fraud Mitigation & Freeze Policy

## Purpose
This document outlines the standard operating procedure for freezing accounts during suspected fraudulent activity. 

## General Rules
1. **Immediate Freeze**: Any activity originating from a known blacklisted IP or associated with a high-risk merchant ID (`M_999`, `M_666`) should result in an immediate `freeze_account` action.
2. **Suspicious Activity**: High-frequency transactions (more than 5 per minute) on basic accounts should trigger an automatic `REVIEW`.
3. **VIP Accounts**: Centurion and VIP accounts cannot be automatically frozen by the AI agent logic. Any threat detection on VIP accounts must be escalated via `create_escalation_ticket`.

## Compliance
All freezes must be logged in the `audit_logger` with a specific reason string including the Risk Score provided by the Secure Governance system.
