# backend/services/database.py

import logging
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from config.settings import load_config
from services.cipher import encrypt


# Load MongoDB URI
config = load_config()
client = MongoClient("mongodb+srv://resulovezov:zTXelEryJEzsz6N8@cluster0.ieiqobl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Configure logging
logging.basicConfig(level=logging.WARNING) # Set up logging with WARNING level
logger = logging.getLogger(__name__)

# Constants for status codes
SIGN_UP_SUCCESSFUL = 1
SIGN_UP_USER_EXISTS = 0
LOGIN_SUCCESS = 1
LOGIN_FAILED = 0
PROJECT_ADD_SUCCESS = 1
PROJECT_ADD_FAILURE = 0
DB_ERROR = -1

### User Management Functions ###

def database_sign_up(userid, password):
    """Registers a new user with an encrypted password."""
    try:
        db = client["Users"]
        collection = db["Universe"]
        
        # Check if the user already exists
        if collection.find_one({"userid": userid}):
            return SIGN_UP_USER_EXISTS  # User already exists
        
        # Encrypt password and add new user
        encrypted_password = encrypt(password)
        collection.insert_one({
            "userid": userid,
            "password": encrypted_password,
            "projects": []
        })
        logging.debug(f"User '{userid}' created successfully.")
        return SIGN_UP_SUCCESSFUL
    except Exception as e:
        logging.error(f"Sign-up error: {e}")
        return DB_ERROR

def database_login(userid, password):
    """Authenticates a user by checking their password."""
    try:
        db = client["Users"]
        collection = db["Universe"]
        
        # Find the user and verify password
        user = collection.find_one({"userid": userid})
        if user and user["password"] == encrypt(password):
            logging.debug(f"User '{userid}' logged in successfully.")
            return LOGIN_SUCCESS
        logging.debug(f"Login failed for user '{userid}'.")
        return LOGIN_FAILED
    except Exception as e:
        logging.error(f"Login error: {e}")
        return DB_ERROR

### Project Management Functions ###

def database_add_project(userid, name, id, description):
    """Adds a new project for the user, ensuring that project IDs are unique globally."""
    try:
        db = client["Projects"]
        collection = db["Universe"]
        user_collection = client["Users"]["Universe"]

        # Check if a project with the same ID already exists globally
        existing_project = collection.find_one({"id": id})
        if existing_project:
            logger.warning(f"[Duplication Warning] Project with ID '{id}' already exists globally.")
            return {"message": "Project ID already exists globally. Choose a different ID."}, 409

        # Look up the user
        user = user_collection.find_one({"userid": userid})
        if user:
            project = {
                "name": name,
                "id": id,
                "description": description,
                "users": [userid]
            }
            try:
                # Insert the project, enforcing unique ID
                collection.insert_one(project)
            except DuplicateKeyError:
                logger.warning(f"[Duplication Warning] Project with ID '{id}' already exists globally.")
                return {"message": "Project ID already exists globally. Choose a different ID."}, 409

            # Add the project ID to the user's project list, avoiding duplicates
            user_collection.update_one(
                {"userid": userid},
                {"$addToSet": {"projects": id}}
            )
            return {"message": "Project created successfully."}, 201
        else:
            logger.error(f"[User Not Found] User ID '{userid}' does not exist.")
            return {"message": "User not found."}, 404
    except Exception as e:
        logger.error(f"Add project error: {e}")
        return {"message": "Internal server error."}, 500

def database_leave_project(userid, id):
    """Adds a new project for the user, ensuring that project IDs are unique globally."""
    try:
        db = client["Projects"]
        collection = db["Universe"]
        user_collection = client["Users"]["Universe"]

        # Check if a project with the same ID already exists globally
        existing_project = collection.find_one({"id": id})
        if existing_project:
            logger.warning(f"[Duplication Warning] Project with ID '{id}' already exists globally.")
            return {"message": "Project ID already exists globally. Choose a different ID."}, 409

        # Look up the user
        user = user_collection.find_one({"userid": userid})
        if user:
            # Check if the user is part of the project
            if id not in user.get("projects", []):
                logger.warning(f"[Not Part of Project] User ID '{userid}' is not part of project '{id}'.")
                return {"message": "User is not part of this project."}, 400
            # Remove the project ID from the user's project list
            user_collection.update_one(
                {"userid": userid},
                {"$pull": {"projects": id}}
            )

            # Remove the user from the project's user list
            collection.update_one(
                {"id": id},
                {"$pull": {"users": userid}}
            )

            return {"message": "User successfully left the project."}, 200
        else:
            logger.error(f"[User Not Found] User ID '{userid}' does not exist.")
            return {"message": "User not found."}, 404
    except Exception as e:
        logger.error(f"Leave project error: {e}")
        return {"message": "Internal server error."}, 500

def database_get_user_projects(userid):
    """Retrieves a list of projects associated with the user, including checked-out hardware."""
    try:
        user_collection = client["Users"]["Universe"]
        project_collection = client["Projects"]["Universe"]
        hardware_collection = client["HardwareSet"]["Universe"]

        # Find user and retrieve associated projects
        user = user_collection.find_one({"userid": userid})
        if user:
            project_ids = user["projects"]
            projects = list(project_collection.find({"id": {"$in": project_ids}}, {"_id": 0}))

            # Add checked-out hardware information for each project
            for project in projects:
                project_hardware = hardware_collection.find(
                    {f"checked_out.{project['id']}": {"$gt": 0}},
                    {"hardware_name": 1, f"checked_out.{project['id']}": 1, "_id": 0}
                )
                project["hardware"] = [
                    {
                        "name": hardware["hardware_name"],
                        "quantity": hardware["checked_out"][project["id"]]
                    }
                    for hardware in project_hardware
                ]
            return projects
        return None
    except Exception as e:
        logging.error(f"Get user projects error: {e}")
        return None


### Hardware Management Functions ###

def database_create_hardware():
    """Initializes hardware items in the database (run only once)."""
    try:
        db = client["HardwareSet"]
        collection = db["Universe"]
        
        # Define hardware items
        hardware_items = [
            {"hardware_name": "Laser Cutter", "capacity": 1000, "availability": 1000, "checked_out": {}},
            {"hardware_name": "3D Printer", "capacity": 1000, "availability": 1000, "checked_out": {}},
            {"hardware_name": "GPU", "capacity": 1000, "availability": 1000, "checked_out": {}}
        ]
        
        # Insert each hardware item if it doesn't already exist
        for hardware in hardware_items:
            if not collection.find_one({"hardware_name": hardware["hardware_name"]}):
                collection.insert_one(hardware)
                logging.debug(f"Hardware '{hardware['hardware_name']}' added to database.")
    except Exception as e:
        logging.error(f"Create hardware error: {e}")

def database_get_hardwareSets():
    """Retrieves the list of available hardware sets."""
    try:
        db = client["HardwareSet"]
        collection = db["Universe"]
        hardware_list = list(collection.find({}, {"_id": 0}))
        logging.debug(f"Hardware sets retrieved: {hardware_list}")
        return hardware_list
    except Exception as e:
        logging.error(f"Get hardware sets error: {e}")
        return []


def database_check_out(hardware_name, user_id, qty, project_id):
    """Checks out a specified quantity of hardware for a user's project."""
    try:
        db = client["HardwareSet"]
        collection = db["Universe"]
        document = collection.find_one({"hardware_name": hardware_name})

        if document:
            # Check if enough availability exists
            if document["availability"] >= qty:
                # Update availability and assign to the project's checked_out field
                collection.update_one(
                    {"hardware_name": hardware_name},
                    {
                        "$inc": {"availability": -qty},
                        "$set": {f"checked_out.{project_id}": document["checked_out"].get(project_id, 0) + qty}
                    }
                )
                logging.debug(f"Checked out {qty} of '{hardware_name}' to project '{project_id}'.")
            else:
                logging.warning(f"Insufficient availability for '{hardware_name}' to check out {qty} units.")
    except Exception as e:
        logging.error(f"Check out error: {e}")
        
def database_check_in(hardware_name, user_id, qty, project_id):
    """Checks in a specified quantity of hardware for a user's project."""
    try:
        db = client["HardwareSet"]
        collection = db["Universe"]
        document = collection.find_one({"hardware_name": hardware_name})

        if document:
            # Find the quantity currently checked out by this project
            project_qty = document["checked_out"].get(project_id, 0)
            if project_qty >= qty:
                # Update availability and reduce checked-out quantity for the project
                collection.update_one(
                    {"hardware_name": hardware_name},
                    {
                        "$inc": {"availability": qty},
                        "$set": {f"checked_out.{project_id}": project_qty - qty}
                    }
                )
                logging.debug(f"Checked in {qty} of '{hardware_name}' from project '{project_id}'.")
                return True
            else:
                logging.warning(f"Project '{project_id}' attempted to check in more than it had checked out.")
                return False
    except Exception as e:
        logging.error(f"Check-in error: {e}")
        return False
