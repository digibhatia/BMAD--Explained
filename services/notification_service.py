"""
Notification Service — legacy, static templates.

Every outage message uses the same generic template regardless of
region, impact size, or real network status. Flagged in the BMAD
analysis as a Multi-Agent opportunity (planner + network status +
CRM + notification, coordinated).
"""

GENERIC_OUTAGE_MESSAGE = "We are aware of a service issue in your area and are working to resolve it."


def send_outage_notification(customer_id):
    print(f"[NOTIFY {customer_id}] {GENERIC_OUTAGE_MESSAGE}")
    return {"customer_id": customer_id, "message": GENERIC_OUTAGE_MESSAGE}
