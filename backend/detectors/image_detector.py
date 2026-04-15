import os
from PIL import Image

def detect_image_risk(path):
    try:
        size_mb = os.path.getsize(path) / (1024 * 1024)

        img = Image.open(path)
        width, height = img.size
        pixels = width * height

        # simple + stable heuristic
        if size_mb > 5 or pixels > 4000 * 4000:
            return 80   # suspicious
        elif size_mb > 2 or pixels > 2000 * 2000:
            return 50   # flagged
        else:
            return 10   # safe

    except Exception:
        return 70