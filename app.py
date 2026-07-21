from flask import Flask, jsonify

from api.billing import billing_bp
from api.complaints import complaints_bp
from api.plans import plans_bp
from api.outage import outage_bp

app = Flask(__name__)
app.register_blueprint(billing_bp)
app.register_blueprint(complaints_bp)
app.register_blueprint(plans_bp)
app.register_blueprint(outage_bp)


@app.route("/", methods=["GET"])
def index():
    """Not a real endpoint — just a discoverability page so hitting the
    root URL doesn't look like a broken app during the workshop."""
    return jsonify({
        "service": "customer-care-system",
        "status": "running",
        "endpoints": {
            "GET /bill/<customer_id>": "Deterministic bill calculation (try customer_id=1042 or 2087)",
            "POST /billing-query": 'JSON body: {"question": "...", "customer_id": "1042"} — RAG-grounded billing FAQ answer',
            "POST /complaint": 'JSON body: {"customer_id": "1042", "description": "..."} — agentic complaint routing',
            "GET /recommend-plan/<customer_id>": "Static plan recommendation (try customer_id=1042 or 2087)",
            "POST /notify-outage/<customer_id>": "Generic outage notification",
        },
        "note": "GET routes work directly in the browser. POST routes need curl or Postman with a JSON body.",
    })


if __name__ == "__main__":
    app.run(port=5000, debug=True)
