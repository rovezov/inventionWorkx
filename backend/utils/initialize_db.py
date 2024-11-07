# backend/utils/initialize_database.py

import sys
import os

# Ensure the parent directory is in the path for importing config and services
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pymongo import MongoClient
from config.settings import load_config
from services.cipher import encrypt  # Assuming encrypt function is in services

# Load MongoDB configuration
config = load_config()
client = MongoClient(config["MONGODB_URI"])

def initialize_users():
    """
    Initializes the Users collection with a default admin user for testing.
    Passwords are encrypted before storage.
    """
    user_collection = client["Users"]["Universe"]

    # Example user with encrypted password
    default_users = [
        {"userid": "admin", "password": encrypt("admin123"), "projects": []},
        {"userid": "testuser", "password": encrypt("password123"), "projects": []}
    ]
    
    # Insert users only if they don't already exist
    for user in default_users:
        if not user_collection.find_one({"userid": user["userid"]}):
            user_collection.insert_one(user)
            print(f"Inserted default user: {user['userid']}")

def initialize_projects():
    """
    Initializes the Projects collection with a default project for testing.
    """
    project_collection = client["Projects"]["Universe"]

    # Example project
    default_projects = [
        {"name": "Sample Project", "id": "proj1", "description": "A sample project for testing", "users": ["admin"]}
    ]

    # Insert projects only if they don't already exist
    for project in default_projects:
        if not project_collection.find_one({"id": project["id"]}):
            project_collection.insert_one(project)
            print(f"Inserted default project: {project['name']}")

def initialize_hardware():
    """
    Initializes the HardwareSet collection with default hardware items.
    """
    hardware_collection = client["HardwareSet"]["Universe"]

    # Default hardware items
    default_hardware = [
        {"hardware_name": "Laser Cutter", "capacity": 1000, "availability": 1000, "checked_out": {}},
        {"hardware_name": "3D Printer", "capacity": 1000, "availability": 1000, "checked_out": {}},
        {"hardware_name": "GPU", "capacity": 1000, "availability": 1000, "checked_out": {}}
    ]

    # Insert hardware only if it doesn't already exist
    for hardware in default_hardware:
        if not hardware_collection.find_one({"hardware_name": hardware["hardware_name"]}):
            hardware_collection.insert_one(hardware)
            print(f"Inserted default hardware: {hardware['hardware_name']}")

def initialize_database():
    """
    Calls all initialization functions to set up the database.
    """
    initialize_users()
    initialize_projects()
    initialize_hardware()
    print("Database initialization complete.")

if __name__ == "__main__":
    # Confirm before initializing the database
    confirm = input("Are you sure you want to initialize the database? (yes/no): ")
    if confirm.lower() == "yes":
        initialize_database()
    else:
        print("Operation canceled.")
