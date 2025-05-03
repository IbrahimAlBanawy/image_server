import os
import json
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from firebase_admin import credentials, db
import firebase_admin
from app.routes import images
from app.config import supabase, FIREBASE_DB_URL, FIREBASE_SERVICE_ACCOUNT_KEY, SUPABASE_BUCKET_URL

app = FastAPI(title="ESP32-CAM Image Server")

# Include image routes
app.include_router(images.router)

# ✅ Firebase Initialization (if not already initialized)
if not firebase_admin._apps:
    try:
        cred_dict = json.loads(FIREBASE_SERVICE_ACCOUNT_KEY)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred, {"databaseURL": FIREBASE_DB_URL})
    except Exception as e:
        raise ValueError(f"Error initializing Firebase: {str(e)}")

# ✅ Root test endpoint
@app.get("/")
def read_root():
    return {"message": "ESP32-CAM Image Server Running"}

# ✅ Firebase test endpoint
@app.get("/firebase-test")
def firebase_test():
    try:
        data = db.reference("/test").get()
        return {"firebase_data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Firebase Error: {str(e)}")

# ✅ Supabase test endpoint
@app.get("/supabase-test")
def supabase_test():
    try:
        result = supabase.table("your_table_name").select("*").execute()
        return {"supabase_data": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Supabase Error: {str(e)}")

# ✅ List public image URLs from Supabase
@app.get("/supabase-images/{cell_id}")
def list_public_images(cell_id: int):
    try:
        folder_path = f"{cell_id}/"  # Each cell stores its images in its own folder
        files = supabase.storage.from_("plant-images").list(folder_path)

        image_urls = [
            f"{SUPABASE_BUCKET_URL}/{cell_id}/{file['name']}"
            for file in files if 'name' in file
        ]

        return {"image_urls": image_urls}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Supabase Storage Error: {str(e)}")
