"""
Billing Service.

calculate_bill stays exactly as it was — the BMAD analysis said no AI here,
and that decision doesn't change just because a RAG pipeline exists elsewhere
in this file.

answer_customer_query is now implemented per the BMAD decision: RAG.
"""

import os
from database.invoices import get_invoice
from database.customer import get_customer

LATE_FEE_FLAT = 50
TAX_RATE = 0.18

_collection = None


def calculate_tax(invoice):
    return round(invoice["base_charge"] * TAX_RATE, 2)


def calculate_late_fee(invoice):
    return LATE_FEE_FLAT if invoice["days_since_bill"] > 15 else 0


def calculate_bill(customer_id):
    """Deterministic, auditable, financial. Unchanged since Commit 1 — BMAD said no AI here."""
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


def _get_collection():
    """Lazily connect to the ChromaDB collection built by knowledge/build_index.py."""
    global _collection
    if _collection is None:
        import chromadb
        store_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vector_store", "chroma")
        client = chromadb.PersistentClient(path=store_path)
        _collection = client.get_or_create_collection("billing_policy")
    return _collection


def retrieve_policy_context(question, k=3):
    collection = _get_collection()
    results = collection.query(query_texts=[question], n_results=k)
    return "\n".join(results["documents"][0]) if results["documents"] else ""


def answer_customer_query(question, customer_id=None):
    """
    RAG per the BMAD decision in BMAD_ANALYSIS.md — now combined with a
    structured CRM lookup when a customer_id is available, following the
    same structured-vs-unstructured split taught in the Integration
    Engineering module: exact figures come from get_customer/get_invoice,
    policy explanations come from the retrieved context. Never let the
    retrieved text stand in for a real account figure.
    """
    from openai import OpenAI
    client = OpenAI()

    context = retrieve_policy_context(question)
    if not context:
        return "I don't have policy information to answer that — this will be routed to a human agent."

    account_context = ""
    if customer_id:
        customer = get_customer(customer_id)
        invoice = get_invoice(customer_id)
        if customer and invoice:
            account_context = (
                f"\n\nCustomer account (structured, from CRM — use for any exact figures):\n"
                f"plan={customer['plan']}, base_charge={invoice['base_charge']}, "
                f"roaming_charges={invoice['roaming_charges']}, days_since_bill={invoice['days_since_bill']}"
            )

    system_prompt = (
        "You are a telecom billing assistant. Use the policy context for explanations "
        "and the customer account data for any exact figures. Never invent a number "
        "that isn't in the account data below. If neither source answers the question, "
        "say the information is not available — do not guess."
        + "\n\nPolicy context:\n" + context + account_context
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content

