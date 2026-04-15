from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from pathlib import Path

from detectors.audio_detector import detect_audio_risk
from detectors.image_detector import detect_image_risk
from detectors.fusion import fuse_risk

app = FastAPI(title="SecureAI Agent Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    temp_path = UPLOAD_DIR / file.filename

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    audio = ocr = clip = 0

    ext = file.filename.lower()

    try:

        if ext.endswith((".wav", ".mp3")):
            audio = detect_audio_risk(temp_path)

        elif ext.endswith((".png", ".jpg", ".jpeg")):
            ocr, clip = detect_image_risk(temp_path)

        else:
            ocr, clip = detect_image_risk(temp_path)

        result = fuse_risk(audio, ocr, clip)

    finally:
        if temp_path.exists():
            os.remove(temp_path)

    return {
        "audio": audio,
        "ocr": ocr,
        "clip": clip,
        **result
    }
