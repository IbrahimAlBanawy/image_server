import os
import json
from dotenv import load_dotenv

load_dotenv()

# ✅ Firebase Config
FIREBASE_SERVICE_ACCOUNT_KEY = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")
FIREBASE_DB_URL = os.getenv("FIREBASE_DB_URL")

# Ensure Firebase credentials are available
if not FIREBASE_SERVICE_ACCOUNT_KEY:
    raise ValueError("FIREBASE_SERVICE_ACCOUNT_KEY environment variable not set.")
if not FIREBASE_DB_URL:
    raise ValueError("FIREBASE_DB_URL environment variable not set.")

# ✅ Parse Firebase credentials from the environment variable
try:
    # Parse the JSON string into a dictionary
    firebase_credentials = json.loads(FIREBASE_SERVICE_ACCOUNT_KEY)
except Exception as e:
    raise ValueError(f"Error parsing Firebase service account key: {str(e)}")

# ✅ Image Storage Config
IMAGE_STORAGE_PATH = os.getenv("IMAGE_STORAGE_PATH", "./data/plant_images")
IMAGE_BASE_URL = os.getenv("IMAGE_BASE_URL")

# Ensure image storage path is set properly
if not IMAGE_BASE_URL:
    raise ValueError("IMAGE_BASE_URL environment variable not set.")

# Log the configuration for debugging purposes (ensure sensitive info is not logged)
print(f"Firebase DB URL: {FIREBASE_DB_URL}")
print(f"Image Storage Path: {IMAGE_STORAGE_PATH}")
