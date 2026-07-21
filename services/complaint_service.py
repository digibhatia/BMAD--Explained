"""
Complaint Service — LEGACY, superseded by agents/complaint_agent.py per the
BMAD decision in BMAD_ANALYSIS.md ("Complaint Routing -> Agent").

Kept in the repository, unused, so learners can diff the old if/else
routing against the new agentic graph and see exactly what changed and why.
"""

from database.tickets import create_ticket, close_ticket


def notify_manager(ticket):
    print(f"[MANAGER NOTIFIED] {ticket['ticket_id']} — {ticket['description']}")


def route_complaint(customer_id, priority, description):
    """Superseded — see agents/complaint_agent.py: route_complaint_agentic()."""
    ticket = create_ticket(customer_id, priority, description)

    if priority == "HIGH":
        notify_manager(ticket)
    if priority == "LOW":
        close_ticket(ticket["ticket_id"])

    return ticket
