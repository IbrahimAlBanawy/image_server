from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from app.routes import images
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ✅ Firebase Admin SDK
import firebase_admin
from firebase_admin import credentials, db

# ✅ Supabase Client
from supabase import create_client, Client

app = FastAPI(title="ESP32-CAM Image Server")

# ✅ Serve images from /data
app.mount("/data", StaticFiles(directory="data"), name="data")

# ✅ Include your upload/list/delete routes
app.include_router(images.router)

# ✅ Firebase Initialization
firebase_cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
firebase_db_url = os.getenv("FIREBASE_DB_URL")

# Ensure Firebase credentials are available
if not firebase_cred_path:
    raise ValueError("FIREBASE_CREDENTIALS_PATH environment variable not set.")
if not firebase_db_url:
    raise ValueError("FIREBASE_DB_URL environment variable not set.")

if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(firebase_cred_path)
        firebase_admin.initialize_app(cred, {"databaseURL": firebase_db_url})
    except Exception as e:
        raise ValueError(f"Error initializing Firebase: {str(e)}")

# ✅ Supabase Initialization
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Ensure Supabase credentials are available
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL or Key environment variables not set.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ Test route
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
