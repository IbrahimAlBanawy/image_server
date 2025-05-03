import os
from dotenv import load_dotenv

load_dotenv()

# ✅ Firebase Config
FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH")
FIREBASE_DB_URL = os.getenv("FIREBASE_DB_URL")

# ✅ Image Storage Config
IMAGE_STORAGE_PATH = os.getenv("IMAGE_STORAGE_PATH", "./data/plant_images")
IMAGE_BASE_URL = os.getenv("IMAGE_BASE_URL")
