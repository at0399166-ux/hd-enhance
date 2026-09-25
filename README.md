# HD Enhance Mobile

A mobile-friendly photo + video enhancement web app.

## What it does
- Photo upload and enhancement
- Video upload and enhancement
- 1x, 2x, 3x, 4x scaling
- Denoise and sharpen controls
- Preview and download
- FastAPI backend
- FFmpeg video pipeline
- Pillow/OpenCV image pipeline
- Optional Real-ESRGAN integration

## Important
This project does not include AI model weights because they are large. The app works with a high-quality fallback pipeline immediately. Real-ESRGAN can be added later on a machine/server with enough RAM/CPU/GPU.

## Run on a computer/server
1. Install Python 3.11+ and FFmpeg.
2. `pip install -r backend/requirements.txt`
3. `uvicorn backend.app:app --host 0.0.0.0 --port 8000`
4. Open `http://127.0.0.1:8000`

## Phone-only
A phone browser cannot reliably run a heavy Python/FFmpeg server by itself. To make the same project accessible from Chrome on your phone, deploy the backend to a server/hosting service. The frontend is already mobile-ready.
