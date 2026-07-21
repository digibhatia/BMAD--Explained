"""In-memory ticket data store — stands in for a real ticketing system table."""

TICKETS = {}
_next_id = 1000


def create_ticket(customer_id, priority, description):
    global _next_id
    _next_id += 1
    ticket_id = f"TCK-{_next_id}"
    TICKETS[ticket_id] = {
        "ticket_id": ticket_id,
        "customer_id": customer_id,
        "priority": priority,
        "description": description,
        "status": "open",
    }
    return TICKETS[ticket_id]


def close_ticket(ticket_id):
    if ticket_id in TICKETS:
        TICKETS[ticket_id]["status"] = "closed"
    return TICKETS.get(ticket_id)
