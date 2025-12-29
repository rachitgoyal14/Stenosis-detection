Original image:
```bash
+----------------------------+
|     heart + vessels        |
|        [stenosis]          |
|                            |
+----------------------------+
```
After ROI cropping:
```bash
+------------+
|  artery    |
|  stenosis  |
+------------+
```
How ROI Cropping fits in pipeline:

```bash
Angiography Image
        ↓
YOLOv8 (detect stenosis)
        ↓
ROI Cropping  ← YOU ARE HERE
        ↓
Lumen Segmentation (U-Net)
        ↓
Centerline + Diameter
        ↓
% Stenosis
```

```bash
Binary mask (yours)
   ↓
Mask cleanup  ← REQUIRED
   ↓
Single-vessel extraction
   ↓
Skeleton (centerline)
   ↓
Distance transform
   ↓
Diameter profile
   ↓
% stenosis
```

