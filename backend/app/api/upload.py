from fastapi import APIRouter, UploadFile, File
from typing import List
import uuid
import cv2
import os

from services.yolo_service import detect_stenosis
from services.roi_service import extract_roi
from services.mask_service import segment_lumen
from services.stenosis_service import compute_stenosis
from utils.file_utils import save_file

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/angiography/")
async def upload_angiography(files: List[UploadFile] = File(...)):
    processed = []
    skipped = []

    os.makedirs("storage/results/visuals", exist_ok=True)

    for file in files:
        image_bytes = await file.read()
        filename = f"{uuid.uuid4()}_{file.filename}"

        save_file(image_bytes, filename, folder="uploads")

        # 1️⃣ YOLO
        yolo_out = detect_stenosis(image_bytes)

        if not yolo_out["detected"]:
            skipped.append(file.filename)
            continue

        # 2️⃣ ROI
        roi, meta = extract_roi(image_bytes, yolo_out, filename)

        # 3️⃣ Mask
        mask = segment_lumen(roi, filename)

        # 4️⃣ Stenosis + artery
        result = compute_stenosis(roi, mask, meta)

        # 5️⃣ Save visual
        visual_filename = f"{filename}_visual.png"
        visual_path = f"storage/results/visuals/{visual_filename}"
        cv2.imwrite(visual_path, result["visual"])

        processed.append({
            "image": file.filename,
            "artery": result["artery"],
            "confidence": yolo_out["confidence"],
            "stenosis_percent": result["percent"],
            "severity": result["severity"],
            "visual_url": f"/results/visuals/{visual_filename}"
        })

    return {
        "total_images": len(files),
        "stenosis_detected": len(processed),
        "processed_images": processed,
        "skipped_images": skipped
    }
