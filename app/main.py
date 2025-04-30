from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path
import shutil
from datetime import datetime
from uuid import uuid4
from PIL import Image

app = FastAPI(
    title="Image Server API",
    description="Production-ready image hosting service",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
IMAGE_STORAGE = os.getenv("IMAGE_STORAGE", "/data/images")
THUMBNAIL_STORAGE = os.getenv("THUMBNAIL_STORAGE", "/data/thumbnails")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
THUMBNAIL_SIZE = (300, 300)

# Create directories if they don't exist
Path(IMAGE_STORAGE).mkdir(parents=True, exist_ok=True)
Path(THUMBNAIL_STORAGE).mkdir(parents=True, exist_ok=True)

def get_file_extension(filename: str) -> str:
    return filename.split(".")[-1].lower()

def is_allowed_file(filename: str) -> bool:
    return "." in filename and get_file_extension(filename) in ALLOWED_EXTENSIONS

def generate_unique_filename(original_filename: str) -> str:
    ext = get_file_extension(original_filename)
    unique_id = uuid4().hex
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{timestamp}_{unique_id}.{ext}"

def save_uploaded_file(file: UploadFile, destination: str) -> str:
    filename = generate_unique_filename(file.filename)
    file_path = os.path.join(destination, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return filename

def create_thumbnail(original_path: str, thumbnail_path: str):
    with Image.open(original_path) as img:
        img.thumbnail(THUMBNAIL_SIZE)
        img.save(thumbnail_path)

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    if not is_allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")
    
    try:
        # Save original image
        filename = save_uploaded_file(file, IMAGE_STORAGE)
        original_path = os.path.join(IMAGE_STORAGE, filename)
        
        # Create and save thumbnail
        thumbnail_filename = f"thumb_{filename}"
        thumbnail_path = os.path.join(THUMBNAIL_STORAGE, thumbnail_filename)
        create_thumbnail(original_path, thumbnail_path)
        
        return {
            "filename": filename,
            "thumbnail": thumbnail_filename,
            "message": "File uploaded successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/image/{filename}")
async def get_image(filename: str):
    file_path = os.path.join(IMAGE_STORAGE, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)

@app.get("/thumbnail/{filename}")
async def get_thumbnail(filename: str):
    file_path = os.path.join(THUMBNAIL_STORAGE, filename)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Thumbnail not found")
    return FileResponse(file_path)

@app.delete("/image/{filename}")
async def delete_image(filename: str):
    image_path = os.path.join(IMAGE_STORAGE, filename)
    thumb_path = os.path.join(THUMBNAIL_STORAGE, f"thumb_{filename}")
    
    if os.path.exists(image_path):
        os.remove(image_path)
    if os.path.exists(thumb_path):
        os.remove(thumb_path)
    
    return {"message": "Image deleted successfully"}

@app.get("/list/")
async def list_images():
    images = []
    for filename in os.listdir(IMAGE_STORAGE):
        if not filename.startswith('.'):
            file_path = os.path.join(IMAGE_STORAGE, filename)
            stat = os.stat(file_path)
            images.append({
                "filename": filename,
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "thumbnail": f"thumb_{filename}"
            })
    return {"images": images}

@app.get("/")
async def health_check():
    return {"status": "healthy", "service": "image-server"}