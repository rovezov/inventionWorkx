import jwt
from flask import Blueprint, request, jsonify
from functools import wraps
from pymongo import MongoClient
from services.database import database_add_project, database_get_user_projects
from config.settings import load_config

# Initialize project blueprint and configuration
project_blueprint = Blueprint('project', __name__)
config = load_config()
SECRET_KEY = config["SECRET_KEY"]

# Initialize MongoDB client
client = MongoClient("mongodb+srv://resulovezov:zTXelEryJEzsz6N8@cluster0.ieiqobl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return jsonify({"message": "Token is missing or invalid!"}), 403

        try:
            token = token.split()[1]  # Remove "Bearer " prefix
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token!"}), 403

        return f(*args, **kwargs)
    return decorated

# Route to create a new project
@project_blueprint.route('/create', methods=['POST'])
@token_required
def create_project():
    data = request.json
    result, status_code = database_add_project(data['userid'], data['name'], data['id'], data['description'])
    
    # Return the JSON message and status code from database_add_project
    return jsonify(result), status_code

# Route to list projects associated with a user
@project_blueprint.route('/list', methods=['GET'])
@token_required
def list_projects():
    userid = request.args.get('userid')
    projects = database_get_user_projects(userid)
    if projects is not None:
        return jsonify(projects), 200
    else:
        return jsonify({"message": "Failed to retrieve projects."}), 500

# Route to join an existing project by ID
@project_blueprint.route('/join', methods=['POST'])
@token_required
def join_project():
    data = request.json
    userid = data.get("userid")
    project_id = data.get("project_id")

    # Retrieve database collections
    project_collection = client["Projects"]["Universe"]
    user_collection = client["Users"]["Universe"]

    # Check if the project exists
    project = project_collection.find_one({"id": project_id})
    if not project:
        return jsonify({"message": "Project not found. Please check the Project ID and try again."}), 404

    # Check if user is already part of the project
    if userid in project.get("users", []):
        return jsonify({"message": "You are already a member of this project."}), 409

    # Add the user to the project's user list and the project to the user's project list
    project_collection.update_one(
        {"id": project_id},
        {"$addToSet": {"users": userid}}
    )
    user_collection.update_one(
        {"userid": userid},
        {"$addToSet": {"projects": project_id}}
    )
    return jsonify({"message": "Successfully joined the project."}), 200

# Route to leave an existing project by ID
@project_blueprint.route('/leave', methods=['POST'])
@token_required
def leave_project():
    data = request.json
    userid = data.get("userid")
    project_id = data.get("project_id")

    # Retrieve database collections
    project_collection = client["Projects"]["Universe"]
    user_collection = client["Users"]["Universe"]

    # Check if the project exists
    project = project_collection.find_one({"id": project_id})
    if not project:
        return jsonify({"message": "Project not found. Please check the Project ID and try again."}), 404

    # Check if user is not part of the project
    if userid not in project.get("users", []):
        return jsonify({"message": "You are not a member of this project."}), 409

    # Add the user to the project's user list and the project to the user's project list
    project_collection.update_one(
        {"id": project_id},
        {"$pull": {"users": userid}}
    )
    user_collection.update_one(
        {"userid": userid},
        {"$pull": {"projects": project_id}}
    )
    return jsonify({"message": "Successfully left the project."}), 200