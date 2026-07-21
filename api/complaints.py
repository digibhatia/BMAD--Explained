from flask import Blueprint, jsonify, request
from agents.complaint_agent import route_complaint_agentic

complaints_bp = Blueprint("complaints", __name__)


@complaints_bp.route("/complaint", methods=["POST"])
def file_complaint():
    data = request.json
    ticket, response = route_complaint_agentic(data["customer_id"], data["description"])
    return jsonify({"ticket": ticket, "response": response})
