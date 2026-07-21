from flask import Blueprint, jsonify
from services.notification_service import send_outage_notification

outage_bp = Blueprint("outage", __name__)


@outage_bp.route("/notify-outage/<customer_id>", methods=["POST"])
def notify_outage(customer_id):
    return jsonify(send_outage_notification(customer_id))
