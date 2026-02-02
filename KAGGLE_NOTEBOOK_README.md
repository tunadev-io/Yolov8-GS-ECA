# Kaggle Notebook: GE-YOLOv8 Training on RSNA 2024 Dataset

## Overview

This repository contains a comprehensive Kaggle notebook for training the **Custom GE-YOLOv8** model on the **RSNA 2024 Lumbar Spine Degenerative Classification** dataset. The model is from the paper *"Deep learning-based automatic detection and grading of disk herniation"* and includes custom CSP (Gradient Search) and ECAAttention modules.

## Notebook: `kaggle_ge_yolov8_rsna2024_training.ipynb`

### Purpose

To benchmark the custom GE-YOLOv8 model against standard YOLOv11 using an **identical data processing pipeline** but different model architectures.

### Key Features

1. **Custom Architecture**
   - CSP (Gradient Search) modules for improved feature extraction
   - ECAAttention mechanism for channel attention
   - Based on YOLOv8 backbone with modifications

2. **Identical Benchmark Setup**
   - Same data pipeline as YOLOv11 experiment
   - Same image preprocessing (384x384 resize)
   - Same class mapping (3 classes)
   - Same training hyperparameters

3. **RSNA 2024 Dataset Processing**
   - Filters Axial T2 MRI sequences
   - Converts DICOM to 8-bit normalized images
   - Creates bounding box labels from point annotations
   - Propagates labels to adjacent slices (n-1, n+1)

## Usage Instructions

### 1. Prerequisites

- Kaggle account with GPU acceleration enabled
- RSNA 2024 Lumbar Spine dataset added to notebook
  - Dataset: `rsna-2024-lumbar-spine-degenerative-classification`

### 2. Upload to Kaggle

1. Go to [Kaggle Notebooks](https://www.kaggle.com/code)
2. Click "New Notebook" → "Upload Notebook"
3. Select `kaggle_ge_yolov8_rsna2024_training.ipynb`
4. Add the RSNA 2024 dataset to the notebook

### 3. Configure Settings

In the Kaggle notebook settings:
- **Accelerator**: GPU (P100 or T4 recommended)
- **Internet**: ON (required to clone repository)
- **Persistence**: /kaggle/working (to save outputs)

### 4. Run the Notebook

Execute all cells sequentially. The notebook will:

1. **Environment Setup** (~5 minutes)
   - Install standard ultralytics package
   - Clone GE-YOLOv8 repository for custom modules
   - Add custom repo to Python path
   - Verify custom modules are accessible

2. **Data Processing** (~20-40 minutes depending on dataset size)
   - Filter Axial T2 sequences
   - Process DICOM files
   - Generate YOLO format labels
   - Create train/val splits (80/20)

3. **Training** (~2-4 hours for 50 epochs)
   - Initialize custom model
   - Train with benchmark settings
   - Save checkpoints every 5 epochs

4. **Evaluation** (~5 minutes)
   - Validate on test set
   - Generate metrics (mAP50, mAP50-95)
   - Create comparison summary

## Dataset Structure

The notebook expects the RSNA 2024 dataset with this structure:

```
/kaggle/input/rsna-2024-lumbar-spine-degenerative-classification/
├── train.csv
├── train_label_coordinates.csv
├── train_series_descriptions.csv
└── train_images/
    └── [study_id]/
        └── [series_id]/
            └── [instance_number].dcm
```

## Output Files

After running, the notebook generates:

```
/kaggle/working/
├── datasets/axial_t2/              # Processed dataset
│   ├── images/
│   │   ├── train/                  # Training images (JPG)
│   │   └── val/                    # Validation images (JPG)
│   ├── labels/
│   │   ├── train/                  # Training labels (TXT)
│   │   └── val/                    # Validation labels (TXT)
│   └── data.yaml                   # YOLO dataset config
├── ge_yolov8_benchmark/            # Training outputs
│   └── axial_t2_run/
│       ├── weights/
│       │   ├── best.pt             # Best model weights
│       │   └── last.pt             # Last epoch weights
│       ├── results.csv             # Training history
│       └── results.png             # Training curves
└── ge_yolov8_benchmark_summary.txt # Metrics summary
```

## Model Configuration

The notebook uses: `/kaggle/working/Yolov8-GS-ECA/models/v8/yolov8-ECA-CSP.yaml`

### Architecture Details

- **Backbone**: YOLOv8 with CSP modules
- **Neck**: FPN with CSP blocks
- **Head**: Detection head with ECAAttention
- **Scale**: YOLOv8n (can be changed to s/m/l/x)

### Class Mapping

| Class ID | Description | Conditions Included |
|----------|-------------|---------------------|
| 0 | Spinal Canal Stenosis | Center region |
| 1 | Left Neural/Subarticular | Left side conditions |
| 2 | Right Neural/Subarticular | Right side conditions |

## Training Configuration

| Parameter | Value | Justification |
|-----------|-------|---------------|
| Image Size | 384×384 | Match YOLOv11 benchmark |
| Epochs | 50 | Standard for medical imaging |
| Batch Size | 16 | Balance between speed and memory |
| Optimizer | AdamW | Better than SGD for transformers |
| Learning Rate | 0.001 | Conservative for medical data |
| Early Stopping | 10 epochs | Prevent overfitting |

## Expected Metrics

The notebook outputs the following metrics for comparison:

- **mAP50**: Mean Average Precision at IoU=0.50
- **mAP50-95**: Mean Average Precision at IoU=0.50:0.95
- **Precision**: Detection precision
- **Recall**: Detection recall
- **Per-class AP**: Individual class performance

## Comparison with YOLOv11

To compare with YOLOv11 results:

1. Note the final mAP50 and mAP50-95 values
2. Compare with your YOLOv11 experiment metrics
3. Analyze per-class performance differences
4. Consider inference speed vs. accuracy trade-offs

## Troubleshooting

### Issue: Custom modules not found OR "does not appear to be a Python project" error

**Solution**: The GE-YOLOv8 repository doesn't have `setup.py`, so it cannot be installed with `pip install -e .`. The notebook now:
1. Installs standard `ultralytics` package first
2. Clones the custom repo and adds it to Python path
3. Imports will use custom modules from the cloned directory

If you see import errors, verify:
- The custom repo was cloned to `/kaggle/working/Yolov8-GS-ECA`
- The repo path is in `sys.path` (check verification cell output)
- Files `nn/modules/block.py` and `nn/modules/Attention.py` exist in the cloned repo

### Issue: Out of memory

**Solution**: 
- Reduce batch size to 8 or 4
- Use a smaller model scale (n instead of s/m)
- Disable image caching

### Issue: DICOM loading errors

**Solution**: 
- Check dataset is properly added to notebook
- Verify file paths in error messages
- Some DICOM files may be corrupted - the script handles these gracefully

### Issue: Training too slow

**Solution**:
- Ensure GPU is enabled in notebook settings
- Reduce image size to 320 or 256 (but note this affects comparison)
- Use fewer epochs (e.g., 25) for initial testing

## Citation

If you use this notebook or the GE-YOLOv8 model, please cite:

**Paper**: *"Deep learning-based automatic detection and grading of disk herniation"*

*Note: Complete citation details (authors, journal, DOI) should be added once available.*

**Original GE-YOLOv8 Repository**: https://github.com/hxxbb/Yolov8-GS-ECA

## License

This notebook follows the same license as the original repository (GPL-3.0).

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review cell outputs for error messages
3. Open an issue in the repository

## Updates and Improvements

Potential enhancements:
- [ ] Add data augmentation options
- [ ] Support for multi-scale training
- [ ] Integration with wandb for experiment tracking
- [ ] Ensemble with YOLOv11 predictions
- [ ] Export to ONNX for deployment
