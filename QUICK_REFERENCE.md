# YOLOv11 Axial T2 MRI Training - Quick Reference

## 📋 Quick Start

```bash
# On Kaggle
1. Upload yolov11_axial_t2_mri_training.ipynb
2. Add dataset: RSNA 2024 Lumbar Spine Degenerative Classification
3. Enable GPU (T4 x2 recommended)
4. Run All Cells
```

## 🎯 Key Information

### Model
- **Architecture:** YOLOv11x (Extra Large)
- **Task:** Object Detection
- **Input:** 384x384 RGB images

### Dataset
- **Source:** RSNA 2024 Lumbar Spine Degenerative Classification
- **Modality:** Axial T2 MRI only
- **Split:** 80% train / 20% validation

### Classes (3)
| Class ID | Name | Description |
|----------|------|-------------|
| 0 | Center | Spinal Canal Stenosis |
| 1 | Left | Left Neural Foraminal Narrowing & Left Subarticular Stenosis |
| 2 | Right | Right Neural Foraminal Narrowing & Right Subarticular Stenosis |

### Hyperparameters (from Paper - Table III)
```python
imgsz = 384           # Image size
batch = 16            # Batch size
epochs = 50           # Training epochs (50 for Kaggle, paper: 100-120)
optimizer = 'AdamW'   # Optimizer
lr0 = 0.001          # Initial learning rate
weight_decay = 0.0005 # Weight decay
dropout = 0.2         # Dropout rate
patience = 15         # Early stopping patience
cos_lr = True         # Cosine LR scheduler
warmup_epochs = 10    # Warmup epochs
momentum = 0.8        # Momentum
```

## 📊 Pipeline Overview

```
Input: DICOM Files (.dcm)
    ↓
Filter: Axial T2 Series Only
    ↓
Load: Read DICOM with pydicom
    ↓
Normalize: Convert to 8-bit (0-255)
    ↓
Resize: 384x384 pixels
    ↓
Create Labels: Point → YOLO Bounding Box
    ↓
Propagate: Share labels to adjacent slices (n±1)
    ↓
Split: 80% train / 20% val
    ↓
Augment: Rotation, Scaling, Flipping
    ↓
Train: YOLOv11x with paper hyperparameters
    ↓
Evaluate: mAP, Precision, Recall
    ↓
Visualize: Predictions on validation images
    ↓
Export: ONNX, TorchScript
```

## 🔧 Notebook Sections

1. **Environment Setup** - Install packages
2. **Data Filtering** - Extract Axial T2 series
3. **Class Mapping** - Define 3 classes
4. **DICOM Processing** - Load & normalize functions
5. **Dataset Preparation** - Process all images
6. **Train/Val Split** - 80/20 split
7. **Data Augmentation** - Configure augmentation
8. **data.yaml Creation** - YOLO config file
9. **Visualize Samples** - Check training data
10. **Initialize Model** - Load YOLOv11x
11. **Training** - Train with paper hyperparameters
12. **Display Results** - Show training curves
13. **Evaluation** - Validate on test set
14. **Inference & Viz** - Predict and visualize (Figure 9 style)
15. **Export Model** - Export to ONNX/TorchScript
16. **Summary** - Final results and statistics

## 💾 Output Files

```
/kaggle/working/
├── datasets/axial_t2/
│   ├── train/images/     # Training images
│   ├── train/labels/     # Training labels (YOLO format)
│   ├── val/images/       # Validation images
│   ├── val/labels/       # Validation labels
│   └── data.yaml         # YOLO dataset config
└── yolo11_axial_t2/train/
    ├── weights/
    │   ├── best.pt       # ⭐ Best model (use this!)
    │   └── last.pt       # Last checkpoint
    ├── results.png       # Training curves
    ├── confusion_matrix.png
    └── ... (other metrics)
```

## 📈 Expected Performance

| Metric | Expected Range |
|--------|----------------|
| mAP50 | 0.70 - 0.85 |
| mAP50-95 | 0.50 - 0.65 |
| Precision | 0.75 - 0.90 |
| Recall | 0.65 - 0.80 |

## 🚀 Usage After Training

### Load Best Model
```python
from ultralytics import YOLO
model = YOLO('/kaggle/working/yolo11_axial_t2/train/weights/best.pt')
```

### Run Inference
```python
# Single image
results = model('path/to/mri_image.jpg', conf=0.25)

# Batch inference
results = model(['image1.jpg', 'image2.jpg'], conf=0.25)
```

### Visualize Results
```python
for result in results:
    result.show()  # Display image with boxes
    result.save(filename='result.jpg')  # Save result
```

### Get Predictions Programmatically
```python
for result in results:
    boxes = result.boxes
    for box in boxes:
        # Get coordinates
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        
        # Get confidence and class
        conf = box.conf[0].cpu().numpy()
        cls = int(box.cls[0].cpu().numpy())
        
        print(f"Class: {cls}, Confidence: {conf:.2f}, Box: ({x1},{y1},{x2},{y2})")
```

## 🐛 Common Issues & Solutions

### Issue: Out of Memory
**Solution:** Reduce batch size
```python
# In training cell, change:
batch=16  →  batch=8  or  batch=4
```

### Issue: Training too slow
**Solution:** 
- Verify GPU is enabled: `torch.cuda.is_available()`
- Use smaller model: `YOLO('yolo11m.pt')` instead of `yolo11x.pt`

### Issue: Dataset not found
**Solution:** Check paths in notebook
```python
INPUT_PATH = '/kaggle/input/rsna-2024-lumbar-spine-degenerative-classification'
# Verify this path exists in Kaggle
```

### Issue: No labels created
**Solution:** Check CSV files have correct columns:
- `train_series_descriptions.csv`: needs `series_description` column
- `train_label_coordinates.csv`: needs `x`, `y`, `condition`, `instance_number` columns

## 📚 Key Functions

### Load DICOM
```python
def load_dicom_image(dcm_path):
    """Load and normalize DICOM to 8-bit RGB"""
    dcm = pydicom.dcmread(dcm_path)
    img = dcm.pixel_array
    # Normalize to 0-255
    img = (img - img.min()) / (img.max() - img.min() + 1e-8)
    img = (img * 255).astype(np.uint8)
    return img
```

### Create YOLO BBox
```python
def create_yolo_bbox(x, y, orig_height, orig_width, box_size=32):
    """Convert point to YOLO format bounding box"""
    # Creates fixed-size box centered on point
    # Returns: (x_center, y_center, width, height) normalized to 0-1
```

## 🎓 Learning Resources

- **Paper:** "YOLOv11 Based Classification of Lumbar Spine Degenerative Changes Across Multi-Modal Imaging" (Patel et al., 2025)
- **YOLO Docs:** https://docs.ultralytics.com
- **RSNA Competition:** https://www.kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification
- **PyDICOM Docs:** https://pydicom.github.io/
- **Albumentations:** https://albumentations.ai/

## ⏱️ Estimated Times

| Task | Time (GPU T4 x2) |
|------|------------------|
| Data Processing | 15-30 min |
| Training (50 epochs) | 2-3 hours |
| Evaluation | 5-10 min |
| **Total** | **~3-4 hours** |

## 📝 Notes

- The notebook is self-contained and runs from start to finish
- All paths are relative to Kaggle directory structure
- Intermediate results are saved automatically
- Label propagation (n±1 slices) increases training data
- Model checkpoints saved every 10 epochs
- Early stopping enabled with patience=15

## 🎉 Success Criteria

✅ All cells execute without errors  
✅ Training completes with decreasing loss  
✅ mAP50 > 0.70 on validation set  
✅ Visualizations show correct bounding boxes  
✅ Model exports successfully to ONNX  

---

**Ready to train?** Upload the notebook to Kaggle and hit "Run All"! 🚀
