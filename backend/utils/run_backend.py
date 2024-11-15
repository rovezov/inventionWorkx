import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask
from flask_cors import CORS
from api.auth_api import auth_blueprint
from api.project_api import project_blueprint
from api.hardware_api import hardware_blueprint


app = Flask(__name__)
CORS(app, origins=["http://3.144.236.59", "http://localhost", "http://127.0.0.1"])

# Register blueprints for each API
app.register_blueprint(auth_blueprint, url_prefix="/api/auth")
app.register_blueprint(project_blueprint, url_prefix="/api/project")
app.register_blueprint(hardware_blueprint, url_prefix="/api/hardware")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Update host and port

