# YOLOv11 RSNA 2024 Training Notebook - Quick Overview

## Notebook Structure

```
┌─────────────────────────────────────────────────────────────────┐
│  YOLOv11 RSNA 2024 Lumbar Spine Training Pipeline              │
└─────────────────────────────────────────────────────────────────┘

1. SETUP
   ├─ Install: ultralytics, pydicom, albumentations
   └─ Import: pandas, numpy, cv2, matplotlib, etc.

2. DATA FILTERING
   ├─ Load: train_series_descriptions.csv
   ├─ Filter: series_description == 'Sagittal T2/STIR'
   └─ Load: train_label_coordinates.csv

3. DATA PREPROCESSING
   ├─ DICOM Loading & Normalization (0-255)
   ├─ Resize: 384x384 pixels
   ├─ Bounding Box Creation (32x32 fixed size)
   ├─ YOLO Format Conversion
   └─ Label Propagation (n-1, n, n+1 slices)

4. DATASET SPLIT
   ├─ Training: 80%
   └─ Validation: 20%

5. DATA AUGMENTATION
   ├─ Rotation: ±10°
   ├─ Scaling: ±10%
   └─ Horizontal Flip: 50%

6. VISUALIZATION
   └─ Display sample images with annotations

7. MODEL CONFIG
   ├─ Create: data.yaml
   │   ├─ nc: 5 classes
   │   └─ names: [L1/L2, L2/L3, L3/L4, L4/L5, L5/S1]
   └─ Load: YOLOv11x (yolo11x.pt)

8. TRAINING (Table III Hyperparameters)
   ├─ Image Size: 384
   ├─ Batch: 16
   ├─ Epochs: 50
   ├─ Optimizer: AdamW
   ├─ Learning Rate: 0.001
   ├─ Weight Decay: 0.0005
   ├─ Dropout: 0.2
   ├─ Patience: 15
   ├─ Cosine LR: True
   ├─ Warmup: 10 epochs
   └─ Momentum: 0.8

9. RESULTS VISUALIZATION
   ├─ Loss curves
   ├─ Confusion matrix
   └─ PR curves

10. EVALUATION
    ├─ Load best.pt model
    ├─ Run validation
    └─ Display metrics (mAP, Precision, Recall)

11. INFERENCE & VISUALIZATION
    └─ Predict on validation samples (Figure 9 style)

12. MODEL EXPORT
    └─ Export to ONNX format

13. SUMMARY
    └─ Display final metrics and conclusions
```

## Key Features

### 5 Classes (Intervertebral Disc Levels)
```
Class 0: L1/L2  (Red)
Class 1: L2/L3  (Green)
Class 2: L3/L4  (Blue)
Class 3: L4/L5  (Yellow)
Class 4: L5/S1  (Magenta)
```

### Processing Pipeline
```
DICOM Images → Normalize (0-255) → Resize (384x384) → 
Create BBoxes → YOLO Format → Train/Val Split → 
Augmentation → Training → Evaluation → Export
```

### Expected Output
```
/kaggle/working/
├── datasets/sagittal_t2/
│   ├── train/
│   │   ├── images/
│   │   └── labels/
│   ├── val/
│   │   ├── images/
│   │   └── labels/
│   └── data.yaml
└── yolov11_sagittal_t2/train/
    ├── weights/
    │   ├── best.pt
    │   └── last.pt
    ├── results.png
    ├── confusion_matrix.png
    └── PR_curve.png
```

## Quick Start

1. Upload notebook to Kaggle
2. Add RSNA 2024 dataset
3. Enable GPU
4. Run all cells
5. Monitor training progress
6. View results and predictions

## Performance Metrics

The notebook will output:
- **mAP@50**: Mean Average Precision at 50% IoU
- **mAP@50-95**: Mean Average Precision across IoU thresholds
- **Precision**: Detection precision
- **Recall**: Detection recall
- **F1 Score**: Harmonic mean of precision and recall

## Methodology Reference

Based on:
**Patel et al. (2025)**: "YOLOv11 Based Classification of Lumbar Spine Degenerative Changes Across Multi-Modal Imaging"

## File Information

- **Notebook**: `yolov11_rsna_sagittal_t2_training.ipynb`
- **Documentation**: `README_YOLOV11_NOTEBOOK.md`
- **Overview**: `NOTEBOOK_OVERVIEW.md` (this file)
