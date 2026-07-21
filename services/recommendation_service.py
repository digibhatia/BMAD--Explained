"""
Recommendation Service — legacy, static rule.

Today this always recommends the same "top" plan regardless of usage.
No personalization exists. Flagged in the BMAD analysis as a
RAG + Agent opportunity (retrieve the catalog, reason over real usage).
"""

def recommend_plan(customer_id):
    return {"customer_id": customer_id, "recommended_plan": "Unlimited Plus", "reason": "default top-tier plan"}
