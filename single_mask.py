import cv2
import numpy as np
from skimage.filters import frangi
from skimage.morphology import (
    remove_small_objects,
    binary_closing,
    binary_opening,
    disk
)

def generate_better_mask(roi_gray):
    # ---- 1. Contrast enhancement ----
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img = clahe.apply(roi_gray)

    # ---- 2. Denoise ----
    img = cv2.GaussianBlur(img, (5,5), 0)

    # ---- 3. Vessel enhancement (tuned) ----
    # Fixed parameter names for newer scikit-image versions
    vessel = frangi(
        img,
        sigmas=range(1, 4, 1),  # scale_range -> sigmas
        alpha=0.5,              # beta1 -> alpha  
        beta=15                 # beta2 -> beta
    )
    vessel = (vessel / vessel.max() * 255).astype(np.uint8)

    # ---- 4. Adaptive threshold ----
    binary = cv2.adaptiveThreshold(
        vessel,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        21,
        -2
    )

    # ---- 5. Morphological cleanup ----
    binary = binary_closing(binary > 0, disk(2))
    binary = binary_opening(binary, disk(1))

    # ---- 6. Remove tiny junk ----
    binary = remove_small_objects(binary, min_size=150)

    return (binary * 255).astype(np.uint8)

def extract_main_vessel(mask):
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mask)

    if num_labels <= 1:
        return mask

    largest = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
    cleaned = np.zeros_like(mask)
    cleaned[labels == largest] = 255
    return cleaned

def thicken_mask(mask):
    kernel = np.ones((3,3), np.uint8)
    return cv2.dilate(mask, kernel, iterations=1)

# Main processing
roi_gray = cv2.imread("roi_stenosis.png", cv2.IMREAD_GRAYSCALE)

if roi_gray is None:
    print("Error: Could not load roi_stenosis.png")
    print("Please check if the file exists in the current directory.")
    exit()

print("Processing roi_stenosis.png...")
print(f"Image shape: {roi_gray.shape}")

mask = generate_better_mask(roi_gray)
mask = extract_main_vessel(mask)
mask = thicken_mask(mask)

cv2.imwrite("mmask.png", mask)
print("Enhanced mask saved as: mmask.png")