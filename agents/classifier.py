"""
Pure classification logic, deliberately separated from agents/complaint_agent.py.

Why: complaint_agent.py imports langgraph at module level, which means any
test importing classify_complaint from there also pulls in the full graph
runtime. Splitting the pure, dependency-free logic out here means it can be
unit-tested in CI without needing LangGraph, ChromaDB or an API key —
exactly the kind of small refactor a production-readiness pass should catch.
"""


def classify_complaint(description: str) -> dict:
    text = description.lower()
    if "fraud" in text or "unauthorized" in text:
        severity = "critical"
    elif "down" in text or "not working" in text or "outage" in text:
        severity = "high"
    else:
        severity = "medium"
    return {
        "type": "network" if "down" in text else "billing_or_service",
        "severity": severity,
        "confidence_score": 0.86,
    }


def decide_escalation(classification: dict, prior_ticket_count: int, valid: bool = True) -> str:
    """The hard escalation rule, isolated so it can be unit-tested directly."""
    if not valid:
        return "escalate"
    if classification["severity"] in ("high", "critical") or prior_ticket_count > 0:
        return "escalate"
    return "resolve"
