import os
from dotenv import load_dotenv

load_dotenv()

FIREBASE_CRED_PATH = os.getenv("FIREBASE_CRED_PATH")
FIREBASE_DB_URL = os.getenv("FIREBASE_DB_URL")
IMAGE_STORAGE_PATH = os.getenv("IMAGE_STORAGE_PATH", "./data/plant_images")
IMAGE_BASE_URL = os.getenv("IMAGE_BASE_URL")
