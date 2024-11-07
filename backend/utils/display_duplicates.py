# backend/utils/display_duplicates.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pymongo import MongoClient
from config.settings import load_config

# Load MongoDB configuration
config = load_config()
client = MongoClient(config["MONGODB_URI"])

# Connect to the appropriate database and collection
db = client["HardwareSet"]["Universe"]

# Aggregation pipeline to find duplicates based on 'hardware_name'
pipeline = [
    {"$group": {"_id": "$hardware_name", "count": {"$sum": 1}, "docs": {"$push": "$_id"}}},
    {"$match": {"count": {"$gt": 1}}}
]

duplicates = list(db.aggregate(pipeline))

if duplicates:
    print("Duplicate hardware entries found:")
    for duplicate in duplicates:
        print(f"Hardware Name: {duplicate['_id']}, Count: {duplicate['count']}, IDs: {duplicate['docs']}")
else:
    print("No duplicates found.")
