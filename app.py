from flask import Flask

from api.billing import billing_bp
from api.complaints import complaints_bp
from api.plans import plans_bp
from api.outage import outage_bp

app = Flask(__name__)
app.register_blueprint(billing_bp)
app.register_blueprint(complaints_bp)
app.register_blueprint(plans_bp)
app.register_blueprint(outage_bp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
