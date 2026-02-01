# YOLOv11 Axial T2 MRI Training Notebook

## Overview

This Jupyter notebook provides a **complete, end-to-end pipeline** for training a YOLOv11 object detection model specifically for **Axial T2 MRI images** from the RSNA 2024 Lumbar Spine Degenerative Classification dataset.

The implementation strictly follows the methodology described in the research paper:  
**"YOLOv11 Based Classification of Lumbar Spine Degenerative Changes Across Multi-Modal Imaging"** (Patel et al., 2025)

## Notebook File

- **File:** `yolov11_axial_t2_mri_training.ipynb`
- **Environment:** Kaggle (optimized for Kaggle kernels)
- **Expected Runtime:** 2-4 hours (depending on dataset size and GPU availability)

## Features

### 1. Environment Setup
- Automatic installation of required packages (`ultralytics`, `pydicom`, `albumentations`)
- Import of all necessary libraries for data processing, model training, and visualization

### 2. Data Filtering
- Loads `train_series_descriptions.csv` and filters for **Axial T2** series only
- Loads `train_label_coordinates.csv` for bounding box annotations
- Expected input path: `/kaggle/input/rsna-2024-lumbar-spine-degenerative-classification`

### 3. Data Preprocessing
- **DICOM Handling:** Reads `.dcm` files using `pydicom`
- **Normalization:** Converts pixel values to 8-bit integers (0-255)
- **Resizing:** Resizes all images to **384x384 pixels** (as per paper)
- **Label Creation:** Converts point coordinates (x, y) to YOLO bounding boxes with fixed size

### 4. Class Mapping (3 Classes)
The notebook maps RSNA conditions to 3 anatomical classes for Axial view:

- **Class 0 (Center):** Spinal Canal Stenosis
- **Class 1 (Left):** Left Neural Foraminal Narrowing & Left Subarticular Stenosis
- **Class 2 (Right):** Right Neural Foraminal Narrowing & Right Subarticular Stenosis

### 5. Label Propagation
Implements the **shared coordinates strategy** mentioned in the paper:
- Labels are propagated to adjacent slices (n-1, n, n+1)
- This augments the training data and improves model generalization

### 6. Dataset Split
- **Training Set:** 80% of images
- **Validation Set:** 20% of images
- Saves to `/kaggle/working/datasets/axial_t2/train` and `/val`

### 7. Data Augmentation
Implements augmentation pipeline using **Albumentations**:
- Rotation (±15 degrees)
- Random scaling (±20%)
- Horizontal flipping
- Vertical flipping

YOLO's built-in augmentation is also applied during training.

### 8. Model Configuration
- **Model:** YOLOv11x (Extra Large version, as used in the paper)
- **data.yaml:** Auto-generated with 3 classes and proper paths
- **Pre-trained weights:** Uses `yolo11x.pt` (automatically downloaded)

### 9. Training Hyperparameters (Table III from Paper)
The notebook uses **exact hyperparameters** from the research paper:

| Parameter | Value | Description |
|-----------|-------|-------------|
| `imgsz` | 384 | Image size (384x384) |
| `batch` | 16 | Batch size |
| `epochs` | 50 | Number of epochs (reduced from 100-120 for Kaggle) |
| `optimizer` | AdamW | Optimizer |
| `lr0` | 0.001 | Initial learning rate |
| `weight_decay` | 0.0005 | Weight decay |
| `dropout` | 0.2 | Dropout rate |
| `patience` | 15 | Early stopping patience |
| `cos_lr` | True | Cosine learning rate annealing |
| `warmup_epochs` | 10 | Warmup epochs |
| `momentum` | 0.8 | Momentum |

### 10. Evaluation & Visualization
- Validates on the validation set
- Displays training metrics (mAP50, mAP50-95, Precision, Recall)
- Shows confusion matrix and training curves
- **Inference visualization:** Displays MRI images with predicted bounding boxes and class labels (similar to Figure 9 in the paper)

### 11. Model Export
Exports the trained model to multiple formats:
- ONNX
- TorchScript

## How to Use

### On Kaggle:

1. **Upload the notebook** to Kaggle
2. **Add the dataset**: RSNA 2024 Lumbar Spine Degenerative Classification
3. **Enable GPU**: Settings → Accelerator → GPU T4 x2 (recommended)
4. **Run all cells**: Cell → Run All
5. **Wait for training**: Approximately 2-4 hours
6. **Download results**: From `/kaggle/working/yolo11_axial_t2/train/`

### Locally (if you have the dataset):

1. **Modify paths** in the notebook:
   - Change `INPUT_PATH` to your dataset location
   - Change `WORKING_PATH` to your desired output location
2. **Ensure GPU is available** (CUDA-compatible)
3. **Run the notebook** using Jupyter or JupyterLab
4. **Install dependencies** (first cell handles this)

## Output Structure

After training, the following structure is created:

```
/kaggle/working/
├── datasets/
│   └── axial_t2/
│       ├── train/
│       │   ├── images/
│       │   └── labels/
│       ├── val/
│       │   ├── images/
│       │   └── labels/
│       └── data.yaml
└── yolo11_axial_t2/
    └── train/
        ├── weights/
        │   ├── best.pt          # Best model checkpoint
        │   └── last.pt          # Last model checkpoint
        ├── results.png          # Training curves
        ├── confusion_matrix.png # Confusion matrix
        └── ... (other metrics)
```

## Expected Results

Based on the paper and similar implementations:

- **mAP50:** 0.70 - 0.85 (depending on dataset quality and training time)
- **mAP50-95:** 0.50 - 0.65
- **Precision:** 0.75 - 0.90
- **Recall:** 0.65 - 0.80

*Note: Results may vary based on dataset quality, GPU configuration, and random seed.*

## Requirements

### Python Packages:
- `ultralytics` (latest version)
- `pydicom`
- `albumentations`
- `pandas`
- `numpy`
- `opencv-python` (`cv2`)
- `matplotlib`
- `scikit-learn`
- `tqdm`
- `pyyaml`

### Hardware:
- **GPU:** NVIDIA GPU with at least 16GB VRAM (e.g., T4, V100, A100)
- **RAM:** 16GB+ recommended
- **Storage:** 50GB+ free space for dataset and outputs

### Dataset:
- RSNA 2024 Lumbar Spine Degenerative Classification
- Available on Kaggle: https://www.kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification

## Troubleshooting

### Out of Memory Errors:
- Reduce `batch` size (try 8 or 4)
- Reduce `imgsz` to 320 or 256

### Slow Training:
- Ensure GPU is enabled (check with `torch.cuda.is_available()`)
- Reduce `epochs` for testing
- Use a smaller model (e.g., `yolo11m.pt` instead of `yolo11x.pt`)

### Missing Dataset Files:
- Verify the dataset is correctly linked in Kaggle
- Check that `INPUT_PATH` points to the correct directory
- Ensure CSV files exist: `train_series_descriptions.csv` and `train_label_coordinates.csv`

## Citation

If you use this notebook in your research, please cite the original paper:

```
Patel et al. (2025). "YOLOv11 Based Classification of Lumbar Spine Degenerative Changes 
Across Multi-Modal Imaging"
```

And the RSNA 2024 dataset:

```
RSNA 2024 Lumbar Spine Degenerative Classification
https://www.kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification
```

## License

This notebook is provided for educational and research purposes. Please refer to the RSNA dataset license and Ultralytics YOLO license for usage restrictions.

## Support

For issues or questions:
1. Check the Kaggle discussion forum for the RSNA 2024 competition
2. Refer to Ultralytics YOLO documentation: https://docs.ultralytics.com
3. Open an issue in the repository

## Acknowledgments

- RSNA 2024 Competition organizers
- Ultralytics team for YOLOv11
- Patel et al. for the research methodology
- Kaggle for providing computational resources
