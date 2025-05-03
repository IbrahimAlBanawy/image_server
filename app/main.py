from fastapi import FastAPI, HTTPException
from app.routes import images
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Firebase Admin SDK
import firebase_admin
from firebase_admin import credentials, db

# Supabase Client
from supabase import create_client, Client

app = FastAPI(title="ESP32-CAM Image Server")

# Include your routes
app.include_router(images.router)

# Firebase Initialization
firebase_service_account_key = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")
firebase_db_url = os.getenv("FIREBASE_DB_URL")

if not firebase_service_account_key:
    raise ValueError("FIREBASE_SERVICE_ACCOUNT_KEY environment variable not set.")
if not firebase_db_url:
    raise ValueError("FIREBASE_DB_URL environment variable not set.")

if not firebase_admin._apps:
    try:
        cred_dict = json.loads(firebase_service_account_key)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred, {"databaseURL": firebase_db_url})
    except Exception as e:
        raise ValueError(f"Error initializing Firebase: {str(e)}")

# Supabase Initialization
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL or Key environment variables not set.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ Root test
@app.get("/")
def read_root():
    return {"message": "ESP32-CAM Image Server Running"}

# ✅ Firebase test
@app.get("/firebase-test")
def firebase_test():
    try:
        data = db.reference("/test").get()
        return {"firebase_data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Firebase Error: {str(e)}")

# ✅ Supabase test
@app.get("/supabase-test")
def supabase_test():
    try:
        result = supabase.table("your_table_name").select("*").execute()
        return {"supabase_data": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Supabase Error: {str(e)}")

# ✅ List Public Image URLs from Supabase
@app.get("/supabase-images")
def list_public_images():
    try:
        bucket_name = "esp32-images"  # Replace with your Supabase bucket name
        folder_path = "images/"       # Optional: folder inside the bucket

        result = supabase.storage.from_(bucket_name).list(folder_path)
        files = result

        # Construct the base public URL
        base_url = f"{SUPABASE_URL}/storage/v1/object/public/{bucket_name}/{folder_path}"
        image_urls = [base_url + file['name'] for file in files if 'name' in file]

        return {"image_urls": image_urls}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Supabase Storage Error: {str(e)}")
