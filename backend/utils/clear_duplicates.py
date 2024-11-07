# backend/utils/clear_duplicates.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pymongo import MongoClient
from config.settings import load_config

# Load MongoDB URI from settings
config = load_config()
client = MongoClient(config["MONGODB_URI"])


def remove_duplicate_projects():
    """Remove duplicate projects based only on project 'id', keeping the first instance."""
    project_collection = client["Projects"]["Universe"]

    # Find duplicates based on project ID
    pipeline = [
        {"$group": {"_id": "$id", "ids": {"$push": "$_id"}, "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 1}}}
    ]
    duplicates = list(project_collection.aggregate(pipeline))

    # Remove all duplicates, keeping only the first instance for each project ID
    delete_count = 0
    for duplicate in duplicates:
        ids_to_delete = duplicate["ids"][1:]  # Skip the first instance
        result = project_collection.delete_many({"_id": {"$in": ids_to_delete}})
        delete_count += result.deleted_count
        print(f"Removed {len(ids_to_delete)} duplicates of project ID '{duplicate['_id']}'")

    print(f"Total project duplicates removed: {delete_count}")

def remove_duplicate_hardware():
    """Remove duplicate hardware entries based on 'hardware_name', keeping the first instance."""
    hardware_collection = client["HardwareSet"]["Universe"]

    # Find duplicates based on hardware name
    pipeline = [
        {"$group": {"_id": "$hardware_name", "ids": {"$push": "$_id"}, "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 1}}}
    ]
    duplicates = list(hardware_collection.aggregate(pipeline))

    # Remove all duplicates, keeping only the first instance for each hardware_name
    delete_count = 0
    for duplicate in duplicates:
        ids_to_delete = duplicate["ids"][1:]  # Skip the first instance
        result = hardware_collection.delete_many({"_id": {"$in": ids_to_delete}})
        delete_count += result.deleted_count
        print(f"Removed {len(ids_to_delete)} duplicates of hardware '{duplicate['_id']}'")

    print(f"Total hardware duplicates removed: {delete_count}")

if __name__ == "__main__":
    print("Removing duplicate projects...")
    remove_duplicate_projects()
    print("\nRemoving duplicate hardware...")
    remove_duplicate_hardware()
    print("\nDuplicate cleanup complete.")
