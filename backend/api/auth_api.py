# backend/api/auth_api.py

import jwt
from flask import Blueprint, request, jsonify
from services.database import database_sign_up, database_login
from config.settings import load_config
import datetime

auth_blueprint = Blueprint('auth', __name__)
config = load_config()
SECRET_KEY = config["SECRET_KEY"]

def generate_token(userid):
    payload = {
        "userid": userid,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    data = request.json
    result = database_sign_up(data['userid'], data['password'])
    if result == 1:
        return jsonify({"message": "User created successfully."}), 201
    elif result == 0:
        return jsonify({"message": "User already exists."}), 409
    else:
        return jsonify({"message": "Sign-up failed."}), 500

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    result = database_login(data['userid'], data['password'])
    if result == 1:
        token = generate_token(data['userid'])
        return jsonify({"message": "Login successful.", "token": token}), 200
    else:
        return jsonify({"message": "Login failed."}), 401
