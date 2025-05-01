from fastapi import APIRouter, UploadFile, File, HTTPException
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
    return await save_image_and_update_firebase(cell_id, file)

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
