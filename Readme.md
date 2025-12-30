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

update pipeline
```bash 
ROI
 ↓
Binary lumen mask
 ↓
Skeleton + diameter
 ↓
YOLO stenosis window
 ↓
D_min  ← inside YOLO box
D_ref  ← outside YOLO box
 ↓
% stenosis
```
```bash
Original Image
   ↓
YOLOv8 (stenosis localization)
   ↓
ROI crop + save YOLO box metadata
   ↓
Lumen segmentation (automatic mask)
   ↓
Skeleton + diameter computation
   ↓
D_min ONLY inside YOLO box
D_ref ONLY outside YOLO box
   ↓
% stenosis
```
So for each ROI, store:
```bash
{
  "image": "roi_001.png",
  "roi_offset": [roi_x1, roi_y1],
  "yolo_box": [sx1, sy1, sx2, sy2]
}
```

```bash
Doctor Uploads Images
        ↓
YOLO Stenosis Detection (fast)
        ↓
┌───────────────┐
│ If stenosis   │── YES ──▶ Full pipeline
│ detected?     │           (ROI → Mask → Diameter)
└───────────────┘
        │
        NO
        │
  Skip image (store as normal)
```

```mermaid
flowchart LR
    A[DICOM Upload] --> B[DICOM Ingest & Frame Extraction]
    B --> C[YOLO Stenosis Detection Model]
    C --> D[Detections + Confidence Scores<br/>+ Timestamps]
    D --> E[Frame Ranking Engine]
    E --> F[Findings Editor]
    F --> G[Study Data Store]
    G --> H[Study Viewer UI]
    H --> I[Optimization]
    I --> J[Doctor Actions<br/>Accept / Review / Edit]
```
Doctor's flow
```mermaid
flowchart TD
    A[Upload DICOM Folder] --> B[AI Processing Starts]
    B --> C[Findings Editor]
    C --> D[Doctor Clicks Study]
    D --> E[Study Page Opens]
    E --> F[Automated Highlighted Confidence Frames]
    F --> G[Visual Evidence Panel<br/>Show Artery Label + Confidence + EF]
    G --> H[Frame-Level Comparison View]
    H --> I{Doctor Decision}

    I -->|Accept| J[Finalize Findings]
    I -->|Needs Review| K[Inspector Mode]

    K --> L[Edit Frames / Add Notes]
    L --> M[Save Edits]

    M --> N[Natural Language Report Flow]
    J --> O[Generate One-Page Summary]
    O --> P[Download PDF / Export / Send to EHR]
```
Natural Language Report Flow
```mermaid
flowchart TD
    A[Doctor Dictates Text / Voice] --> B[Speech-to-Text]
    B --> C[Structured Findings JSON]
    C --> D[LLM Report Formatter]
    D --> E[Draft Impression & Recommendations]
    E --> F[Report Preview UI]
    F --> G[Doctor Edits Text]
    G --> H[Doctor Signs]
    H --> I[Final Report Saved]
    I --> J[Export PDF / DICOM-SR]
```
Application Flow:
```mermaid
flowchart LR
    A[Dashboard] --> B[Findings Editor]
    B --> C[Study Page]

    C --> D[Interactive Overlays]
    D --> E[Inspector Drawer]

    E --> F[AI Report Model]
    F --> G[Download / Export]
```

```bash
flowchart LR
    subgraph DATA_FLOW[DATA FLOW]
        A[DICOM Upload]
        B[DICOM Ingest & Frame Extraction]
        C[YOLO Stenosis Detection Model]
        D[Detections + Confidence Scores<br/>+ Timestamps]
        E[Frame Ranking Engine]
        F[Findings Editor]
        G[Study Data Store]
        H[Study Viewer UI]
        I[Optimization]
        J[Doctor Actions<br/>Accept / Review / Edit]

        A --> B --> C --> D --> E --> F
        F --> G --> H --> I --> J
    end
```
```bash
flowchart TD
    subgraph DOCTOR_FLOW[Doctor’s Flow]
        A[Upload DICOM Folder]
        B[AI Processing Starts]
        C[Findings Editor]
        D[Doctor Clicks Study]
        E[Study Page Opens]
        F[Automated Highlighted Confidence Frames]
        G[Visual Evidence Panel<br/>Artery Label + Confidence + EF]
        H[Frame-Level Comparison View]
        I{Doctor Decision}

        J[Finalize Findings]
        K[Inspector Mode]
        L[Edit Frames / Add Notes]
        M[Save Edits]
        N[Natural Language Report Flow]
        O[Generate One-Page Summary]
        P[Download PDF / Export / Send to EHR]

        A --> B --> C --> D --> E --> F --> G --> H --> I
        I -->|Accept| J --> O --> P
        I -->|Needs Review| K --> L --> M --> N
    end

```
```bash
flowchart TD
    subgraph NLP_FLOW[Natural Language Report Flow]
        A[Doctor Dictates Text / Voice]
        B[Speech-to-Text]
        C[Structured Findings JSON]
        D[LLM Report Formatter]
        E[Draft Impression & Recommendations]
        F[Report Preview UI]
        G[Doctor Edits Text]
        H[Doctor Signs]
        I[Final Report Saved]
        J[Export PDF / DICOM-SR]

        A --> B --> C --> D --> E --> F --> G --> H --> I --> J
    end
```

```bash

flowchart LR
    subgraph APP_FLOW[Application Flow]
        A[Dashboard]
        B[Findings Editor]
        C[Study Page]
        D[Interactive Overlays]
        E[Inspector Drawer]
        F[AI Report Model]
        G[Download / Export]

        A --> B --> C
        C --> D --> E --> F --> G
    end

```