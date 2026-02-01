# YOLOv11 Sagittal T1 MRI Training Notebook

## Overview

This repository contains a complete, end-to-end Kaggle Jupyter Notebook for training a YOLOv11x model specifically for **Sagittal T1 MRI images** from the RSNA 2024 Lumbar Spine Degenerative Classification dataset.

## Notebook File

**File**: `kaggle_yolov11_sagittal_t1_training.ipynb`

## Methodology

The notebook strictly follows the methodology described in the research paper:
> *"YOLOv11 Based Classification of Lumbar Spine Degenerative Changes Across Multi-Modal Imaging"* (Patel et al., 2025)

## Task

**Intervertebral Disc Level Detection** - Detection and classification of 5 disc levels in Sagittal T1 MRI images:
- L1/L2 (Class 0)
- L2/L3 (Class 1)
- L3/L4 (Class 2)
- L4/L5 (Class 3)
- L5/S1 (Class 4)

## Dataset

**RSNA 2024 Lumbar Spine Degenerative Classification**
- Input Path: `/kaggle/input/rsna-2024-lumbar-spine-degenerative-classification`
- Filtered for: Sagittal T1 series only
- Image Format: DICOM (.dcm)

## Key Features

### 1. Data Processing
- **DICOM Handling**: Read and process medical images using pydicom
- **Normalization**: Convert pixel values to 8-bit integers (0-255)
- **Resizing**: Resize all images to 384×384 pixels
- **Label Creation**: Convert point coordinates to YOLO bounding boxes (32×32 pixels)
- **Shared Coordinates Strategy**: Propagate labels to adjacent slices (n-1, n+1) for data augmentation

### 2. Model Configuration
- **Model**: YOLOv11x (Extra Large variant)
- **Architecture**: Detection model with 5 classes
- **Input Size**: 384×384 pixels

### 3. Training Hyperparameters (from Paper Table III)
```yaml
Image Size: 384×384
Batch Size: 16
Epochs: 50 (reduced from 100-120 for Kaggle time limits)
Optimizer: AdamW
Learning Rate: 0.001 (with Cosine Annealing)
Weight Decay: 0.0005
Dropout: 0.2
Momentum: 0.8
Warmup Epochs: 10
Patience: 15
```

### 4. Data Augmentation
- Rotation: ±15 degrees
- Scaling: ±20%
- Horizontal Flip: 50% probability
- Vertical Flip: 20% probability

### 5. Evaluation & Visualization
- **Metrics**: mAP50, mAP50-95, Precision, Recall
- **Visualizations**: 
  - Predicted bounding boxes on validation images
  - Training curves (losses, mAP, precision/recall)
  - Similar to Figure 9 (top row) in the paper

## Notebook Structure

1. **Environment Setup** - Install and import required libraries
2. **Data Filtering** - Filter for Sagittal T1 series
3. **Data Preprocessing & Label Creation** - Process DICOM images and create YOLO labels
4. **Data Augmentation** - Define augmentation pipeline
5. **Model Configuration** - Create data.yaml and initialize model
6. **Model Training** - Train with paper-specific hyperparameters
7. **Evaluation & Visualization** - Validate and visualize results

## Output Files

When run on Kaggle, the notebook generates:
- `/kaggle/working/datasets/sagittal_t1/` - Processed dataset
- `/kaggle/working/runs/yolov11x_sagittal_t1/weights/best.pt` - Best trained model
- `/kaggle/working/runs/yolov11x_sagittal_t1/results.csv` - Training metrics
- `/kaggle/working/validation_predictions.png` - Visualization of predictions
- `/kaggle/working/training_curves.png` - Training progress plots

## Requirements

The notebook automatically installs required packages:
- ultralytics (YOLOv11)
- pydicom (DICOM image handling)
- albumentations (data augmentation)
- opencv-python-headless (image processing)
- pandas, numpy, matplotlib, tqdm (utilities)

## Usage on Kaggle

1. Upload the notebook to Kaggle
2. Add the RSNA 2024 dataset as input:
   - Dataset: `rsna-2024-lumbar-spine-degenerative-classification`
3. Enable GPU accelerator (recommended: P100 or better)
4. Run all cells sequentially
5. Training will take approximately 3-5 hours depending on GPU

## Notes

- The notebook is designed to run entirely on Kaggle's infrastructure
- All paths are configured for Kaggle's default directory structure
- The dataset filtering ensures only Sagittal T1 images are processed
- The shared coordinates strategy increases training data by ~3x
- Early stopping (patience=15) prevents overfitting

## Reference

This implementation follows the methodology described in:
- Patel et al., "YOLOv11 Based Classification of Lumbar Spine Degenerative Changes Across Multi-Modal Imaging" (2025)

## License

Please refer to the repository's main LICENSE file.
