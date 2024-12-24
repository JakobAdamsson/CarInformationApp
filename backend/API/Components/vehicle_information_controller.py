from flask import Blueprint, jsonify, Response, send_from_directory, request
from Service.vehicle_data_service import VehicleDataService
import os
from httpstatus import HttpStatus

vehicle_information_bp = Blueprint('/vehicle_information', __name__)

VI_functions = VehicleDataService()
status = HttpStatus()

BILTEMA = "https://www.biltema.se/"
OLJEMAGASINET = "https://www.oljemagasinet.se/magasinet/valj-ratt-motorolja"


@vehicle_information_bp.route('/', methods=['GET'])
def hello():
    return "Hello, World!"

@vehicle_information_bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(vehicle_information_bp.root_path, 'static'), 'favicon.ico')

@vehicle_information_bp.route('/get_data/<registration_number>', methods=['GET'])
def get_data(registration_number):
    
    try: 
        if VI_functions.validate_reg_number(registration_number):
            # Get engine type provided as params from frontend(fetchcardata)
            engine_type = request.args.get("Engine")
            car_model = request.args.get("Model")
            # Get vehicle data
            vehicle_data = VI_functions.get_vehicle_data(registration_number, BILTEMA)
            oil_capacity = VI_functions.get_oil_capacity(registration_number, OLJEMAGASINET, engine_type)
            vehicle_data['Oljevolym'] = oil_capacity
            print("här?")
            vehicle_data['Registreringsnummer'] = registration_number
            print("här?2")
            vehicle_data["Motortyp"] = engine_type
            print("här?3")
            vehicle_data["Bilmodell"] = car_model
            print("här?4")
            return jsonify({"data": vehicle_data, "status": status.OK}), status.OK
        return jsonify({"message": "Not a valid reg number", "status": status.NOT_FOUND}), status.NOT_FOUND
    except Exception as e:
        return jsonify({"error": str(e), "status": status.INTERNAL_SERVER_ERROR}), status.INTERNAL_SERVER_ERROR

