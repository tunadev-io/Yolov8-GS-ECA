# YOLOv11 RSNA 2024 Lumbar Spine Training Notebook

## Overview

This repository contains a complete, end-to-end Kaggle Jupyter Notebook for training a **YOLOv11x** model on **Sagittal T2/STIR MRI images** from the RSNA 2024 Lumbar Spine Degenerative Classification dataset.

The implementation strictly follows the methodology described in the research paper:
> **"YOLOv11 Based Classification of Lumbar Spine Degenerative Changes Across Multi-Modal Imaging"** (Patel et al., 2025)

## Notebook File

📓 **Main Notebook**: `yolov11_rsna_sagittal_t2_training.ipynb`

## Key Features

### 1. Complete Pipeline
- ✅ Environment setup and dependency installation
- ✅ Data filtering for Sagittal T2/STIR series only
- ✅ DICOM image processing and normalization
- ✅ YOLO format label generation with bounding boxes
- ✅ Train/validation split (80/20)
- ✅ Data augmentation (Rotation, Scaling, Flipping)
- ✅ YOLOv11x model configuration
- ✅ Training with paper-specified hyperparameters
- ✅ Evaluation and visualization
- ✅ Model export (ONNX format)

### 2. Dataset Processing
- **Input**: RSNA 2024 Lumbar Spine dataset
- **Modality**: Sagittal T2/STIR MRI images only
- **Preprocessing**:
  - DICOM to 8-bit normalization (0-255)
  - Resize to 384×384 pixels
  - RGB conversion for consistency

### 3. Label Creation
- **5 Classes** representing intervertebral disc levels:
  - Class 0: L1/L2
  - Class 1: L2/L3
  - Class 2: L3/L4
  - Class 3: L4/L5
  - Class 4: L5/S1
- **Bounding Box Strategy**:
  - Fixed 32×32 pixel boxes around coordinate points
  - Converted to YOLO format (normalized)
  - Label propagation to adjacent slices (n-1, n, n+1)

### 4. Training Configuration

**Model**: YOLOv11x (Extra Large)

**Hyperparameters** (from Table III of the paper):
```python
- Image Size: 384×384
- Batch Size: 16
- Epochs: 50 (reduced from 100-120 for Kaggle)
- Optimizer: AdamW
- Learning Rate: 0.001
- Weight Decay: 0.0005
- Dropout: 0.2
- Patience: 15
- Cosine Annealing: True
- Warmup Epochs: 10
- Momentum: 0.8
```

### 5. Data Augmentation
Using **Albumentations** library:
- Rotation: ±10 degrees
- Random Scaling: ±10%
- Horizontal Flip: 50% probability

### 6. Visualization
- Sample images with ground truth annotations
- Predictions on validation set (similar to Figure 9 in paper)
- Training metrics and loss curves
- Confusion matrix
- Precision-Recall curves

## Usage

### On Kaggle
1. Create a new Kaggle notebook
2. Add the RSNA 2024 Lumbar Spine dataset
3. Upload `yolov11_rsna_sagittal_t2_training.ipynb`
4. Enable GPU accelerator
5. Run all cells

### Locally
```bash
# Install dependencies
pip install ultralytics pydicom albumentations pandas numpy opencv-python matplotlib scikit-learn tqdm

# Download RSNA 2024 dataset
# Update INPUT_PATH in the notebook

# Run with Jupyter
jupyter notebook yolov11_rsna_sagittal_t2_training.ipynb
```

## Dataset Requirements

**Required Input Structure**:
```
/kaggle/input/rsna-2024-lumbar-spine-degenerative-classification/
├── train_images/
│   ├── [study_id]/
│   │   ├── [series_id]/
│   │   │   ├── [instance_number].dcm
├── train_series_descriptions.csv
└── train_label_coordinates.csv
```

**Output Structure**:
```
/kaggle/working/datasets/sagittal_t2/
├── train/
│   ├── images/
│   └── labels/
├── val/
│   ├── images/
│   └── labels/
└── data.yaml
```

## Expected Results

The notebook will produce:
- Trained YOLOv11x model weights (`best.pt`)
- Training results and metrics
- Visualization plots
- ONNX exported model
- Model performance metrics (mAP, Precision, Recall)

## Model Performance

Expected metrics (based on paper methodology):
- **mAP@50**: High detection accuracy for disc level localization
- **mAP@50-95**: Robust across IoU thresholds
- **Precision & Recall**: Balanced detection performance

## File Structure

```
.
├── yolov11_rsna_sagittal_t2_training.ipynb  # Main notebook
├── README_YOLOV11_NOTEBOOK.md               # This file
└── [Training outputs will be generated during execution]
```

## Technical Details

### Image Processing
```python
# DICOM normalization
img = (img - img.min()) / (img.max() - img.min() + 1e-8) * 255.0

# Resize
img = cv2.resize(img, (384, 384), interpolation=cv2.INTER_LINEAR)
```

### YOLO Bounding Box Format
```
[class_id] [x_center] [y_center] [width] [height]
```
All values normalized to [0, 1]

### Shared Coordinates Strategy
Labels from slice `n` are propagated to slices `n-1` and `n+1` to augment training data and improve generalization.

## Citation

If you use this implementation, please cite:

```bibtex
@article{patel2025yolov11,
  title={YOLOv11 Based Classification of Lumbar Spine Degenerative Changes Across Multi-Modal Imaging},
  author={Patel et al.},
  year={2025}
}
```

## Requirements

### Python Packages
```txt
ultralytics>=8.0.0
pydicom>=2.3.0
albumentations>=1.3.0
pandas>=1.5.0
numpy>=1.23.0
opencv-python>=4.7.0
matplotlib>=3.6.0
scikit-learn>=1.2.0
tqdm>=4.64.0
```

### Hardware
- **GPU**: Recommended (NVIDIA with CUDA support)
- **RAM**: 16GB+ recommended
- **Storage**: 50GB+ for dataset and outputs

## Troubleshooting

### Common Issues

1. **CUDA Out of Memory**
   - Reduce batch size from 16 to 8 or 4
   - Reduce image size (not recommended)

2. **Missing DICOM Files**
   - Verify dataset download is complete
   - Check file paths match expected structure

3. **Low Performance**
   - Increase epochs (up to 100-120 as in paper)
   - Ensure data augmentation is enabled
   - Verify label propagation is working

## Future Enhancements

- [ ] Multi-modal integration (Sagittal T1, Axial T2)
- [ ] Ensemble learning with multiple models
- [ ] Test-time augmentation
- [ ] Advanced post-processing (NMS tuning)
- [ ] Real-time inference optimization

## License

This notebook follows the license terms of:
- Ultralytics YOLO (AGPL-3.0)
- RSNA 2024 Competition dataset terms

## Acknowledgments

- RSNA 2024 Lumbar Spine Degenerative Classification competition
- Patel et al. (2025) for the research methodology
- Ultralytics team for YOLOv11 implementation

## Contact

For issues, questions, or contributions, please open an issue in the repository.

---

**Last Updated**: February 2026  
**Notebook Version**: 1.0  
**Compatible with**: Kaggle, Google Colab, Local Jupyter
