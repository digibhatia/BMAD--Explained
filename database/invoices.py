"""In-memory invoice data store — stands in for a real billing/invoices table."""

INVOICES = {
    "1042": {"customer_id": "1042", "base_charge": 999, "days_since_bill": 20, "roaming_charges": 210},
    "2087": {"customer_id": "2087", "base_charge": 499, "days_since_bill": 5, "roaming_charges": 0},
}


def get_invoice(customer_id):
    return INVOICES.get(customer_id)
