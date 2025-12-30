import numpy as np
from skimage.morphology import skeletonize
from scipy.ndimage import distance_transform_edt

def compute_stenosis(roi, mask, meta):
    binary = mask > 0
    skeleton = skeletonize(binary)
    dist = distance_transform_edt(binary)

    coords = np.column_stack(np.where(skeleton))
    diameters = dist[skeleton] * 2

    sx1, sy1, sx2, sy2 = meta["yolo_box"]

    inside = (
        (coords[:,1]>=sx1)&(coords[:,1]<=sx2)&
        (coords[:,0]>=sy1)&(coords[:,0]<=sy2)
    )
    outside = ~inside

    if inside.sum() < 3 or outside.sum() < 7:
        return {"percent": None, "severity": "Unreliable"}

    D_min = diameters[inside].min()
    D_ref = np.sort(diameters[outside])[-10:].mean()
    percent = (1 - D_min/D_ref) * 100

    if percent < 30:
        severity = "Normal"
    elif percent < 50:
        severity = "Mild"
    elif percent < 70:
        severity = "Moderate"
    else:
        severity = "Severe"

    return {
        "percent": round(float(percent), 2),
        "severity": severity
    }
