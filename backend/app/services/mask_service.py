import cv2
import numpy as np
from skimage.filters import frangi
from skimage.morphology import remove_small_objects

def segment_lumen(roi, filename):
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    vessel = frangi(gray)
    vessel = (vessel / vessel.max() * 255).astype(np.uint8)

    binary = cv2.adaptiveThreshold(
        vessel, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 21, -2
    )

    binary = remove_small_objects(binary > 0, min_size=150)
    mask = (binary * 255).astype(np.uint8)

    cv2.imwrite(f"storage/masks/{filename}", mask)
    return mask
