from flask import Blueprint, jsonify
from services.recommendation_service import recommend_plan

plans_bp = Blueprint("plans", __name__)


@plans_bp.route("/recommend-plan/<customer_id>", methods=["GET"])
def get_recommendation(customer_id):
    return jsonify(recommend_plan(customer_id))
