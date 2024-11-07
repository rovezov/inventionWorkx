# backend/utils/reset_database.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pymongo import MongoClient
from config.settings import load_config

# Load MongoDB URI from the settings
config = load_config()
client = MongoClient(config["MONGODB_URI"])

def reset_collection(db, collection_name, initialize_data=None):
    """
    Drops the specified collection and optionally initializes it with default data.

    :param db: The MongoDB database object.
    :param collection_name: Name of the collection to drop and reset.
    :param initialize_data: Optional list of documents to insert as initial data.
    """
    collection = db[collection_name]
    collection.drop()
    print(f"Collection '{collection_name}' has been reset.")

    # Initialize with default data if provided
    if initialize_data:
        collection.insert_many(initialize_data)
        print(f"Initialized '{collection_name}' with default data.")

def reset_database():
    # Connect to specific databases
    users_db = client["Users"]
    projects_db = client["Projects"]
    hardware_db = client["HardwareSet"]

    # Reset collections with optional initialization
    reset_collection(users_db, "Universe")  # Clears all users

    reset_collection(projects_db, "Universe")  # Clears all projects

    # Reset hardware collection and initialize with default hardware data
    hardware_initial_data = [
        {"hardware_name": "Laser Cutter", "capacity": 1000, "availability": 1000, "checked_out": {}},
        {"hardware_name": "3D Printer", "capacity": 1000, "availability": 1000, "checked_out": {}},
        {"hardware_name": "GPU", "capacity": 1000, "availability": 1000, "checked_out": {}}
    ]
    reset_collection(hardware_db, "Universe", initialize_data=hardware_initial_data)

    print("Database reset complete.")

if __name__ == "__main__":
    # Confirm before resetting the database
    confirm = input("Are you sure you want to reset the database? This action cannot be undone (yes/no): ")
    if confirm.lower() == "yes":
        reset_database()
        print("Database has been reset for testing.")
    else:
        print("Operation canceled.")
