import os
import cv2
import numpy as np
import json

def extract_roi(image_bytes, yolo_out, filename, scale=2):
    os.makedirs("storage/roi", exist_ok=True)

    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    H, W = img.shape[:2]

    x1, y1, x2, y2 = map(int, yolo_out["box"])
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

    bw, bh = int((x2 - x1) * scale), int((y2 - y1) * scale)

    x1p = max(0, cx - bw)
    y1p = max(0, cy - bh)
    x2p = min(W, cx + bw)
    y2p = min(H, cy + bh)

    roi = img[y1p:y2p, x1p:x2p]

    # YOLO box relative to ROI
    yolo_box_roi = [
        x1 - x1p,
        y1 - y1p,
        x2 - x1p,
        y2 - y1p
    ]

    roi_path = os.path.join("storage", "roi", filename)
    cv2.imwrite(roi_path, roi)

    meta = {"yolo_box": yolo_box_roi}

    meta_path = os.path.join("storage", "roi", filename + ".json")
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)

    return roi, meta
