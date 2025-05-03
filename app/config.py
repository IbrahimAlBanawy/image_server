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
    firebase_credentials = json.loads(FIREBASE_SERVICE_ACCOUNT_KEY)
except Exception as e:
    raise ValueError(f"Error parsing Firebase service account key: {str(e)}")

# ✅ Supabase Config
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL or SUPABASE_KEY environment variables not set.")

from supabase import create_client

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ Supabase Bucket Public URL
SUPABASE_BUCKET_URL = "https://kaqawvycksitnvzrldwh.supabase.co/storage/v1/object/public/plant-images"

# ✅ Optional Local Storage Config
IMAGE_STORAGE_PATH = os.getenv("IMAGE_STORAGE_PATH", "./data/plant_images")
IMAGE_BASE_URL = os.getenv("IMAGE_BASE_URL")

if not IMAGE_BASE_URL:
    raise ValueError("IMAGE_BASE_URL environment variable not set.")

# ✅ Debug Logging (avoid logging sensitive credentials)
print(f"Firebase DB URL: {FIREBASE_DB_URL}")
print(f"Supabase URL: {SUPABASE_URL}")
print(f"Image Storage Path: {IMAGE_STORAGE_PATH}")
