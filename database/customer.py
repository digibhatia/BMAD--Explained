"""In-memory customer data store — stands in for a real customer database table."""

CUSTOMERS = {
    "1042": {"customer_id": "1042", "name": "R. Sharma", "plan": "Unlimited Plus", "region": "North-East-4"},
    "2087": {"customer_id": "2087", "name": "A. Mehta", "plan": "Basic 20GB", "region": "West-2"},
}


def get_customer(customer_id):
    return CUSTOMERS.get(customer_id)
