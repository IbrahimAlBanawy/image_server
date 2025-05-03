from datetime import datetime
from fastapi import UploadFile
from uuid import uuid4
from app.firebase.service import (
    update_last_image_url,
    get_last_image_url_from_db,
    list_all_image_urls,
    delete_last_image,
    clear_all_images
)
from app.config import SUPABASE_BUCKET_URL, supabase

async def save_image_and_update_firebase(cell_id: int, file: UploadFile):
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    unique_filename = f"cell{cell_id}_{timestamp}_{uuid4().hex}.jpg"
    storage_path = f"cell{cell_id}/{unique_filename}"

    # Upload the image to Supabase bucket
    file_content = await file.read()
    supabase.storage.from_("plant-images").upload(
        path=storage_path,
        file=file_content,
        file_options={"content-type": file.content_type},
        upsert=True
    )

    # Construct public URL
    image_url = f"{SUPABASE_BUCKET_URL}/{storage_path}"

    # Update Firebase with the image URL
    update_last_image_url(cell_id, image_url)
    return {"message": "✅ Image saved and Firebase updated", "url": image_url}

def get_last_image_url(cell_id: int):
    return get_last_image_url_from_db(cell_id)

def get_all_image_urls(cell_id: int):
    return list_all_image_urls(cell_id)

def delete_last_image_url(cell_id: int):
    return delete_last_image(cell_id)

def clear_all_image_urls(cell_id: int):
    return clear_all_images(cell_id)
