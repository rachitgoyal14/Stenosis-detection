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

