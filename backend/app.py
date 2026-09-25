from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uuid, shutil, subprocess, os, time

from .services.image_enhancer import enhance_image
from .services.video_enhancer import enhance_video

BASE = Path(__file__).resolve().parent
UPLOADS = BASE / "uploads"
OUTPUTS = BASE / "outputs"
UPLOADS.mkdir(exist_ok=True)
OUTPUTS.mkdir(exist_ok=True)

app = FastAPI(title="HD Enhance Mobile")

ALLOWED_IMAGE = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_VIDEO = {".mp4", ".mov", ".mkv", ".webm"}
MAX_MB = int(os.getenv("MAX_UPLOAD_MB", "500"))

def save_upload(upload: UploadFile, allowed):
    ext = Path(upload.filename or "").suffix.lower()
    if ext not in allowed:
        raise HTTPException(400, "Unsupported file type")
    job = uuid.uuid4().hex
    src = UPLOADS / f"{job}{ext}"
    size = 0
    with src.open("wb") as f:
        while True:
            chunk = upload.file.read(1024 * 1024)
            if not chunk:
                break
            size += len(chunk)
            if size > MAX_MB * 1024 * 1024:
                src.unlink(missing_ok=True)
                raise HTTPException(413, f"File is larger than {MAX_MB} MB")
            f.write(chunk)
    return job, src

@app.get("/api/health")
def health():
    return {"ok": True, "service": "HD Enhance"}

@app.post("/api/enhance/image")
async def image(file: UploadFile = File(...), scale: int = Form(2), sharpen: float = Form(1.0), denoise: int = Form(1)):
    scale = max(1, min(4, int(scale)))
    job, src = save_upload(file, ALLOWED_IMAGE)
    out = OUTPUTS / f"{job}.jpg"
    try:
        enhance_image(src, out, scale, float(sharpen), int(denoise))
        return {"ok": True, "job": job, "download": f"/api/download/{job}.jpg"}
    except Exception as e:
        src.unlink(missing_ok=True)
        raise HTTPException(500, str(e))

@app.post("/api/enhance/video")
async def video(file: UploadFile = File(...), scale: int = Form(2), sharpen: float = Form(1.0), denoise: int = Form(1)):
    scale = max(1, min(4, int(scale)))
    job, src = save_upload(file, ALLOWED_VIDEO)
    out = OUTPUTS / f"{job}.mp4"
    try:
        enhance_video(src, out, scale, float(sharpen), int(denoise))
        return {"ok": True, "job": job, "download": f"/api/download/{job}.mp4"}
    except Exception as e:
        src.unlink(missing_ok=True)
        raise HTTPException(500, "Video processing failed. Make sure FFmpeg is installed on the server.")

@app.get("/api/download/{name}")
def download(name: str):
    safe = Path(name).name
    path = OUTPUTS / safe
    if not path.exists():
        raise HTTPException(404, "File not found")
    return FileResponse(path, filename=safe)

app.mount("/", StaticFiles(directory=str(BASE.parent / "frontend"), html=True), name="frontend")
