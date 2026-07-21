from flask import Blueprint, jsonify, request
from services.complaint_service import route_complaint

complaints_bp = Blueprint("complaints", __name__)


@complaints_bp.route("/complaint", methods=["POST"])
def file_complaint():
    data = request.json
    ticket = route_complaint(data["customer_id"], data["priority"], data["description"])
    return jsonify(ticket)
