from ultralytics import YOLO
import cv2
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "models" / "best.pt"

# ✅ Correct YOLOv8 loading
yolo_model = YOLO(str(MODEL_PATH))

def detect_stenosis(image_bytes):
    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

    # Run inference
    results = yolo_model(img, conf=0.7, device=0)

    if len(results[0].boxes) == 0:
        return {"detected": False}

    box = results[0].boxes.xyxy[0].cpu().numpy()
    conf = float(results[0].boxes.conf[0])

    return {
        "detected": True,
        "box": box,
        "confidence": conf,
        "shape": img.shape
    }
