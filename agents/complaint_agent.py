"""
Complaint Agent — replaces the legacy if/else routing in
services/complaint_service.py, per the BMAD decision in BMAD_ANALYSIS.md:
"Complaint Routing -> Agent".

Six responsibilities, six nodes, one bounded graph — Planner, Classifier,
Retriever, Validator, Escalation, Notification. The escalation threshold
is still a hard rule in code, exactly as taught in the Agent Design module:
naming a node "Escalation" does not mean the model decides the threshold.
"""

from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

from database.tickets import create_ticket


class ComplaintState(TypedDict):
    customer_id: str
    description: str
    classification: Optional[dict]
    prior_ticket_count: int
    valid: bool
    escalate: bool
    ticket: Optional[dict]
    response: Optional[str]


# ---- Planner ----
def planner_node(state: ComplaintState) -> ComplaintState:
    # In this bounded graph, "planning" is the fixed node order below — the
    # Planner's job is simply the entry point that confirms required inputs
    # are present before the rest of the pipeline runs.
    if not state.get("customer_id") or not state.get("description"):
        raise ValueError("Planner: missing customer_id or description")
    return state


# ---- Classifier ----
def classify_complaint(description: str) -> dict:
    """
    Structured-output classification — same schema and validation discipline
    as the Reliability & Structured Output Control module. Replace this stub
    with a real LLM call + JSON schema validation in your own build.
    """
    text = description.lower()
    if "fraud" in text or "unauthorized" in text:
        severity = "critical"
    elif "down" in text or "not working" in text or "outage" in text:
        severity = "high"
    else:
        severity = "medium"
    return {"type": "network" if "down" in text else "billing_or_service",
            "severity": severity, "confidence_score": 0.86}


def classifier_node(state: ComplaintState) -> ComplaintState:
    state["classification"] = classify_complaint(state["description"])
    return state


# ---- Retriever ----
def retriever_node(state: ComplaintState) -> ComplaintState:
    # Stands in for a real ticket-history lookup against database/tickets.py
    from database.tickets import TICKETS
    state["prior_ticket_count"] = sum(
        1 for t in TICKETS.values() if t["customer_id"] == state["customer_id"]
    )
    return state


# ---- Validator ----
def validator_node(state: ComplaintState) -> ComplaintState:
    c = state["classification"]
    valid = (
        c is not None
        and c.get("severity") in ("low", "medium", "high", "critical")
        and 0.0 <= c.get("confidence_score", -1) <= 1.0
    )
    state["valid"] = valid
    return state


# ---- Escalation decision (hard rule, not model judgement) ----
def decide_node(state: ComplaintState) -> str:
    if not state["valid"]:
        return "escalate"  # invalid classification is itself an escalation trigger
    severity = state["classification"]["severity"]
    if severity in ("high", "critical") or state["prior_ticket_count"] > 0:
        return "escalate"
    return "resolve"


# ---- Escalation ----
def escalate_node(state: ComplaintState) -> ComplaintState:
    ticket = create_ticket(state["customer_id"], "HIGH", state["description"])
    state["ticket"] = ticket
    state["escalate"] = True
    state["response"] = f"This has been escalated to a supervisor. Reference: {ticket['ticket_id']}"
    return state


# ---- Resolve (non-escalated path) ----
def resolve_node(state: ComplaintState) -> ComplaintState:
    ticket = create_ticket(state["customer_id"], "LOW", state["description"])
    state["ticket"] = ticket
    state["escalate"] = False
    state["response"] = f"Thanks — we've logged this as {ticket['ticket_id']} and will follow up."
    return state


# ---- Notification (always runs, regardless of path) ----
def notification_node(state: ComplaintState) -> ComplaintState:
    print(f"[NOTIFY {state['customer_id']}] {state['response']}")
    return state


def build_complaint_graph():
    graph = StateGraph(ComplaintState)
    graph.add_node("planner", planner_node)
    graph.add_node("classifier", classifier_node)
    graph.add_node("retriever", retriever_node)
    graph.add_node("validator", validator_node)
    graph.add_node("escalate", escalate_node)
    graph.add_node("resolve", resolve_node)
    graph.add_node("notify", notification_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "classifier")
    graph.add_edge("classifier", "retriever")
    graph.add_edge("retriever", "validator")
    graph.add_conditional_edges("validator", decide_node, {"escalate": "escalate", "resolve": "resolve"})
    graph.add_edge("escalate", "notify")
    graph.add_edge("resolve", "notify")
    graph.add_edge("notify", END)

    return graph.compile()


complaint_agent = build_complaint_graph()


def route_complaint_agentic(customer_id, description):
    """Drop-in replacement for the legacy route_complaint() function."""
    result = complaint_agent.invoke({
        "customer_id": customer_id, "description": description,
        "classification": None, "prior_ticket_count": 0,
        "valid": False, "escalate": False, "ticket": None, "response": None,
    })
    return result["ticket"], result["response"]
