from flask import Blueprint, jsonify, request
from services.billing_service import calculate_bill, answer_customer_query

billing_bp = Blueprint("billing", __name__)


@billing_bp.route("/bill/<customer_id>", methods=["GET"])
def get_bill(customer_id):
    result = calculate_bill(customer_id)
    if result is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(result)


@billing_bp.route("/billing-query", methods=["POST"])
def billing_query():
    question = request.json.get("question", "")
    answer = answer_customer_query(question)
    if answer is None:
        return jsonify({"error": "not implemented — routed to a human agent today"}), 501
    return jsonify({"answer": answer})
