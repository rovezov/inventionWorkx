# backend/config/settings.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_config():
    return {
        "MONGODB_URI": os.getenv("MONGODB_URI"),
        "SECRET_KEY": os.getenv("SECRET_KEY"),
        "CIPHER_N": int(os.getenv("CIPHER_N", 5)),
        "CIPHER_D": int(os.getenv("CIPHER_D", 1)),
        "PRODUCTION_URL": os.getenv("PRODUCTION_URL")
    }
