from Components.vehicle_information_controller import vehicle_information_bp
from Components.account_component import login_bp

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.register_blueprint(vehicle_information_bp, url_prefix='/vehicle_information')
app.register_blueprint(login_bp, url_prefix='/login')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)