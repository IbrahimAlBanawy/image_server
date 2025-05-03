from fastapi import APIRouter, UploadFile, File, HTTPException
from app.config import supabase, SUPABASE_BUCKET_URL
import shutil
import os
from uuid import uuid4
from app.services.image_service import (
    save_image_and_update_firebase,
    get_last_image_url,
    get_all_image_urls,
    delete_last_image_url,
    clear_all_image_urls
)

router = APIRouter()

@router.post("/upload/{cell_id}")
async def upload_image(cell_id: int, file: UploadFile = File(...)):
    if cell_id not in [1, 2, 3]:
        raise HTTPException(status_code=400, detail="Invalid cell ID.")

    temp_file_path = f"/tmp/{uuid4()}_{file.filename}"
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        with open(temp_file_path, "rb") as image_data:
            supabase.storage.from_("plant-images").upload(
                path=f"cell{cell_id}/{file.filename}",
                file=image_data,
                file_options={"content-type": file.content_type},
                upsert=True
            )

        # Construct the public URL using SUPABASE_BUCKET_URL
        file_url = f"{SUPABASE_BUCKET_URL}/cell{cell_id}/{file.filename}"

        await save_image_and_update_firebase(cell_id, file_url)

        return {"message": "✅ Image uploaded successfully", "url": file_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@router.get("/last/{cell_id}")
def get_last(cell_id: int):
    return get_last_image_url(cell_id)

@router.get("/list/{cell_id}")
def get_list(cell_id: int):
    return get_all_image_urls(cell_id)

@router.delete("/delete/{cell_id}")
def delete_last(cell_id: int):
    return delete_last_image_url(cell_id)

@router.delete("/clear/{cell_id}")
def clear_all(cell_id: int):
    return clear_all_image_urls(cell_id)
