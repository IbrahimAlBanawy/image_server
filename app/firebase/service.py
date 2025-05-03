import firebase_admin
from firebase_admin import credentials, db
from app.config import FIREBASE_SERVICE_ACCOUNT_KEY, FIREBASE_DB_URL
import json

# Initialize Firebase if not already done
if not firebase_admin._apps:
    # Parse the Firebase service account key JSON from the environment variable
    try:
        cred_dict = json.loads(FIREBASE_SERVICE_ACCOUNT_KEY)  # Parse JSON string to dictionary
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred, {"databaseURL": FIREBASE_DB_URL})
    except Exception as e:
        raise ValueError(f"Error initializing Firebase: {str(e)}")

# Function to update the last image URL in the Firebase Realtime Database
def update_last_image_url(cell_id: int, image_url: str):
    ref = db.reference(f"esp32cam/images/cell{cell_id}")
    ref.child("last").set({"url": image_url})
    ref.child("history").push().set({"url": image_url})

# Function to get the last image URL from the Firebase Realtime Database
def get_last_image_url_from_db(cell_id: int):
    ref = db.reference(f"esp32cam/images/cell{cell_id}/last")
    return ref.get()

# Function to list all image URLs from the Firebase Realtime Database
def list_all_image_urls(cell_id: int):
    ref = db.reference(f"esp32cam/images/cell{cell_id}/history")
    return ref.get() or {}

# Function to delete the last image entry from the Firebase Realtime Database
def delete_last_image(cell_id: int):
    ref = db.reference(f"esp32cam/images/cell{cell_id}/last")
    ref.delete()
    return {"message": "✅ Last image entry deleted from Firebase."}

# Function to clear all image data for a specific cell from Firebase
def clear_all_images(cell_id: int):
    ref = db.reference(f"esp32cam/images/cell{cell_id}")
    ref.delete()
    return {"message": f"✅ All image data for cell {cell_id} cleared from Firebase."}
