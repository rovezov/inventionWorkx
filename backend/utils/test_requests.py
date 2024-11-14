# backend/utils/test_requests.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import requests
from config.settings import load_config

config = load_config()
PRODUCTION_URL = config["PRODUCTION_URL"]
BASE_URL = "http://" + PRODUCTION_URL +":5000/api"
AUTH_HEADERS = {}

# Define various test functions
def login_and_get_token():
    """Logs in the user and retrieves the JWT token for authenticated requests."""
    login_data = {"userid": "testuser", "password": "password123"}  # Replace with valid credentials
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    try:
        if response.status_code == 200:
            token = response.json().get("token")
            AUTH_HEADERS["Authorization"] = f"Bearer {token}"
            print("Login successful, token acquired.")
        else:
            print("Login failed:", response.status_code, response.text)
    except requests.exceptions.JSONDecodeError:
        print("Login response was not JSON:", response.status_code, response.text)


def test_create_duplicate_project():
    """Attempts to create the same project twice to test duplicate handling."""
    project_data = {"userid": "testuser", "name": "Project1", "id": "proj1", "description": "Sample project"}
    response1 = requests.post(f"{BASE_URL}/project/create", json=project_data, headers=AUTH_HEADERS)
    
    try:
        print("Create Project (1st Attempt):", response1.json())
    except requests.exceptions.JSONDecodeError:
        print("Create Project (1st Attempt) returned non-JSON response:", response1.status_code, response1.text)
    
    response2 = requests.post(f"{BASE_URL}/project/create", json=project_data, headers=AUTH_HEADERS)
    
    try:
        print("Create Project (2nd Attempt):", response2.json())
    except requests.exceptions.JSONDecodeError:
        print("Create Project (2nd Attempt) returned non-JSON response:", response2.status_code, response2.text)

def test_list_projects():
    """Lists all projects associated with the user."""
    response = requests.get(f"{BASE_URL}/project/list", params={"userid": "testuser"}, headers=AUTH_HEADERS)
    print("List Projects:", response.json())

def test_checkout_hardware():
    """Checks out a specified quantity of hardware."""
    hardware_data = {"hardwareName": "Laser Cutter", "userID": "testuser", "qty": 2}
    response = requests.post(f"{BASE_URL}/hardware/checkout", json=hardware_data, headers=AUTH_HEADERS)
    try:
        print("Checkout Hardware:", response.json())
    except requests.exceptions.JSONDecodeError:
        print("Checkout Hardware failed:", response.text)

def test_checkin_hardware():
    """Checks in a specified quantity of hardware."""
    hardware_data = {"hardwareName": "Laser Cutter", "userID": "testuser", "qty": 2}
    response = requests.post(f"{BASE_URL}/hardware/checkin", json=hardware_data, headers=AUTH_HEADERS)
    try:
        print("Checkin Hardware:", response.json())
    except requests.exceptions.JSONDecodeError:
        print("Checkin Hardware failed:", response.text)

def test_join_project():
    """Test joining a project by ID."""
    join_data = {"userid": "testuser", "project_id": "proj1"}
    response = requests.post(f"{BASE_URL}/project/join", json=join_data, headers=AUTH_HEADERS)
    
    try:
        print("Join Project:", response.json())
    except requests.exceptions.JSONDecodeError:
        print("Join Project returned non-JSON response:", response.status_code, response.text)


if __name__ == "__main__":
    # First, log in to acquire the token
    login_and_get_token()
    
    # Run tests only if the token was successfully acquired
    if "Authorization" in AUTH_HEADERS:
        test_create_duplicate_project()
        test_list_projects()
        test_checkout_hardware()
        test_checkin_hardware()
        test_join_project()
    else:
        print("Failed to acquire token; aborting tests.")

