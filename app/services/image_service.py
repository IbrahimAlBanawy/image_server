import os
from datetime import datetime
from fastapi import UploadFile
from app.firebase.service import (
    update_last_image_url,
    get_last_image_url_from_db,
    list_all_image_urls,
    delete_last_image,
    clear_all_images
)
from app.config import IMAGE_STORAGE_PATH, IMAGE_BASE_URL

async def save_image_and_update_firebase(cell_id: int, file: UploadFile):
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"cell{cell_id}_{timestamp}.jpg"
    folder_path = os.path.join(IMAGE_STORAGE_PATH, f"cell{cell_id}")
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    image_url = f"{IMAGE_BASE_URL}/data/plant_images/cell{cell_id}/{filename}"
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
