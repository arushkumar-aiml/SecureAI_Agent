import os
from PIL import Image
import pytesseract

SUSPICIOUS_KEYWORDS = [
    "ignore previous", "ignore all instructions", "system prompt", "you are now",
    "disregard", "override", "jailbreak", "act as", "new instructions",
    "reveal your prompt", "bypass", "do anything now"
]

def detect_image_risk(path):
    """
    Returns (ocr_risk, dimension_risk) as a tuple, both 0-100.
    ocr_risk: based on real OCR text extraction, scanning for prompt-injection style phrases.
    dimension_risk: heuristic sanity check on file size / pixel count (NOT a deepfake detector).
    """
    try:
        img = Image.open(path)
        width, height = img.size
        pixels = width * height
        size_mb = os.path.getsize(path) / (1024 * 1024)

        # Real OCR pass — actually extracts text from the image
        try:
            extracted_text = pytesseract.image_to_string(img).lower()
        except Exception:
            extracted_text = ""

        ocr_risk = 10
        if extracted_text.strip():
            hits = [kw for kw in SUSPICIOUS_KEYWORDS if kw in extracted_text]
            if hits:
                ocr_risk = min(95, 60 + len(hits) * 10)
            elif len(extracted_text.strip()) > 40:
                # sizeable hidden text block found, even if not matching known phrases
                ocr_risk = 40

        # Basic sanity-check heuristic (explicitly NOT a deepfake detector)
        if size_mb > 5 or pixels > 4000 * 4000:
            dimension_risk = 60
        elif size_mb > 2 or pixels > 2000 * 2000:
            dimension_risk = 30
        else:
            dimension_risk = 10

        return ocr_risk, dimension_risk

    except Exception:
        return 70, 70