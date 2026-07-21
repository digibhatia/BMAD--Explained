"""
Billing Service — legacy, deterministic business logic.

This module contains two very different kinds of functions, on purpose.
The BMAD exercise starts here: read calculate_bill and answer_customer_query
and ask, for each one, "should AI touch this?"
"""

from database.invoices import get_invoice

LATE_FEE_FLAT = 50
TAX_RATE = 0.18


def calculate_tax(invoice):
    return round(invoice["base_charge"] * TAX_RATE, 2)


def calculate_late_fee(invoice):
    return LATE_FEE_FLAT if invoice["days_since_bill"] > 15 else 0


def calculate_bill(customer_id):
    """Deterministic, auditable, financial. Do not put AI here."""
    invoice = get_invoice(customer_id)
    if not invoice:
        return None
    tax = calculate_tax(invoice)
    late_fee = calculate_late_fee(invoice)
    total = invoice["base_charge"] + tax + late_fee + invoice["roaming_charges"]
    return {
        "customer_id": customer_id,
        "base_charge": invoice["base_charge"],
        "tax": tax,
        "late_fee": late_fee,
        "roaming_charges": invoice["roaming_charges"],
        "total": total,
    }


def answer_customer_query(question):
    """
    Not implemented. Every billing question today either goes unanswered
    or is manually handled by a support agent reading the policy PDF.
    This is the function BMAD will target first.
    """
    pass
