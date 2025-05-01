from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import images

app = FastAPI(title="ESP32-CAM Image Server")

# ✅ Mount the static directory (so images can be served via URL)
app.mount("/data", StaticFiles(directory="data"), name="data")

# ✅ Include your upload/list/delete routes
app.include_router(images.router)
