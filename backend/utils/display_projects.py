# backend/utils/display_projects.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pymongo import MongoClient
from config.settings import load_config

# Load MongoDB URI from settings
config = load_config()
client = MongoClient("mongodb+srv://resulovezov:zTXelEryJEzsz6N8@cluster0.ieiqobl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

def display_projects():
    """Displays all projects in the Projects collection with detailed information."""
    project_collection = client["Projects"]["Universe"]

    # Fetch all projects
    projects = list(project_collection.find())

    if projects:
        print("Projects in the database:")
        for project in projects:
            print(f"ID: {project.get('id')}")
            print(f"Name: {project.get('name')}")
            print(f"Description: {project.get('description')}")
            print(f"Users: {project.get('users')}")
            print("-" * 30)
    else:
        print("No projects found in the database.")

if __name__ == "__main__":
    display_projects()
