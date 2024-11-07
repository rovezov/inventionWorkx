# backend/api/hardware_api.py

from flask import Blueprint, request, jsonify
from services.database import database_check_in, database_check_out, database_get_hardwareSets

# Define the blueprint for hardware-related routes
hardware_blueprint = Blueprint('hardware', __name__)

@hardware_blueprint.route('/list', methods=['GET'])
def list_hardware():
    hardware = database_get_hardwareSets()
    return jsonify(hardware), 200

@hardware_blueprint.route('/checkout', methods=['POST'])
def checkout_hardware():
    data = request.json
    projectId = data.get("projectId")
    hardwareName = data.get("hardwareName")
    userID = data.get("userID")
    qty = data.get("qty")

    # Now pass projectId to database_check_out
    database_check_out(hardwareName, userID, qty, projectId)
    return jsonify({"message": "Hardware checked out to project."}), 200

@hardware_blueprint.route('/checkin', methods=['POST'])
def checkin_hardware():
    data = request.json
    projectId = data.get("projectId")
    hardwareName = data.get("hardwareName")
    userID = data.get("userID")
    qty = data.get("qty")

    # Now pass projectId to database_check_in
    database_check_in(hardwareName, userID, qty, projectId)
    return jsonify({"message": "Hardware checked in to project."}), 200
