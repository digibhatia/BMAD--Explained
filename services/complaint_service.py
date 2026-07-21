"""
Complaint Service — legacy, rigid priority routing.

Business has asked for sentiment detection, fraud detection and SLA
validation on top of this. None of that fits an if/else ladder — this
is the module BMAD will redesign as an agent.
"""

from database.tickets import create_ticket, close_ticket


def notify_manager(ticket):
    print(f"[MANAGER NOTIFIED] {ticket['ticket_id']} — {ticket['description']}")


def route_complaint(customer_id, priority, description):
    ticket = create_ticket(customer_id, priority, description)

    if priority == "HIGH":
        notify_manager(ticket)
    if priority == "LOW":
        close_ticket(ticket["ticket_id"])

    return ticket
