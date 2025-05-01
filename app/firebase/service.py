import os
import json
import firebase_admin
from firebase_admin import credentials, db

# ✅ Initialize Firebase using environment variable-based credential
if not firebase_admin._apps:
    firebase_cred_json = os.getenv("FIREBASE_CRED_JSON")
    firebase_db_url = os.getenv("FIREBASE_DB_URL")

    if not firebase_cred_json:
        raise ValueError("Missing FIREBASE_CRED_JSON environment variable")
    if not firebase_db_url:
        raise ValueError("Missing FIREBASE_DB_URL environment variable")

    try:
        cred_dict = json.loads(firebase_cred_json)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred, {"databaseURL": firebase_db_url})
        print("✅ Firebase Admin SDK initialized")
    except Exception as e:
        print("❌ Firebase initialization failed:", str(e))
        raise e

# ✅ Firebase image operations

def update_last_image_url(cell_id: int, image_url: str):
    ref = db.reference(f"esp32cam/images/cell{cell_id}")
    ref.child("last").set({"url": image_url})
    ref.child("history").push().set({"url": image_url})

def get_last_image_url_from_db(cell_id: int):
    ref = db.reference(f"esp32cam/images/cell{cell_id}/last")
    return ref.get()

def list_all_image_urls(cell_id: int):
    ref = db.reference(f"esp32cam/images/cell{cell_id}/history")
    return ref.get() or {}

def delete_last_image(cell_id: int):
    ref = db.reference(f"esp32cam/images/cell{cell_id}/last")
    ref.delete()
    return {"message": "✅ Last image entry deleted from Firebase."}

def clear_all_images(cell_id: int):
    ref = db.reference(f"esp32cam/images/cell{cell_id}")
    ref.delete()
    return {"message": f"✅ All image data for cell {cell_id} cleared from Firebase."}
