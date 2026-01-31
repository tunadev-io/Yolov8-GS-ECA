# GE-YOLOv8: Custom YOLOv8 with Gradient Search and ECA Attention

This repository provides custom architectural modifications to Ultralytics YOLOv8, specifically:
- **CSP (Cross Stage Partial)** - Gradient Search module for improved feature extraction
- **ECAAttention (Efficient Channel Attention)** - Enhanced attention mechanism for better feature representation

## Features

- Custom CSP blocks in the backbone for gradient search
- ECAAttention module for efficient channel attention
- Pre-configured model: `yolov8-ECA-CSP.yaml`
- Compatible with Ultralytics YOLOv8 training pipeline
- Designed for use on Kaggle and other cloud platforms

## Installation

### Option 1: Quick Start (Recommended for Kaggle)

Use the provided Jupyter notebook `train_ge_yolov8_kaggle.ipynb` which handles all setup automatically.

### Option 2: Manual Installation

```bash
# Install dependencies
pip install torch torchvision
pip install ultralytics einops

# Clone this repository
git clone https://github.com/tunadev-io/Yolov8-GS-ECA.git
cd Yolov8-GS-ECA

# Copy custom modules to ultralytics installation
python -c "
import shutil, os, ultralytics, re

ul_path = os.path.dirname(ultralytics.__file__)
src = 'nn/modules'
dst = os.path.join(ul_path, 'nn', 'modules')

# Copy custom attention modules
for f in ['Attention.py', 'CoordAttention.py']:
    shutil.copy2(os.path.join(src, f), os.path.join(dst, f))
    print(f'Copied {f}')

# Add CSP to block.py
with open(os.path.join(src, 'block.py')) as f:
    src_code = f.read()

csp_match = re.search(r'(class CSP\\(.*?\\n(?:.*?\\n)*?^        return .*?\\n)', src_code, re.M)
if csp_match:
    csp = csp_match.group(1)
    with open(os.path.join(dst, 'block.py'), 'a') as f:
        f.write('\\n\\n' + csp)
    print('Added CSP class')
else:
    print('Warning: Could not find CSP class definition')
"
```

## Usage

### Training with Custom GE-YOLOv8

```python
from ultralytics import YOLO

# Load the custom model configuration
model = YOLO('models/v8/yolov8-ECA-CSP.yaml')

# Train the model
results = model.train(
    data='your_data.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
)
```

### Dataset Configuration

Create a `data.yaml` file:

```yaml
path: /path/to/dataset
train: images/train
val: images/val

nc: 10  # number of classes
names: ['class1', 'class2', ...]  # class names
```

## Model Architecture

The `yolov8-ECA-CSP.yaml` configuration includes:

- **Backbone**: CSP blocks for gradient search (replaces standard C2f blocks)
- **Head**: ECAAttention applied to P5 output for enhanced feature representation
- **Default**: 10 classes (configurable via `nc` parameter)

### Custom Modules

1. **CSP** (`nn/modules/block.py`)
   - Cross Stage Partial network with gradient search
   - Improves feature extraction and gradient flow
   
2. **ECAAttention** (`nn/modules/Attention.py`)
   - Efficient Channel Attention mechanism
   - Adaptive kernel size for channel attention
   - Minimal parameter overhead

## Kaggle Notebook

See `train_ge_yolov8_kaggle.ipynb` for a complete training example including:
- Environment setup
- Custom module installation
- Dataset configuration generation
- Model training and validation
- Model export options

## Requirements

- Python >= 3.8
- PyTorch >= 1.8.0
- Ultralytics >= 8.0.0
- einops >= 0.3.0

## Project Structure

```
Yolov8-GS-ECA/
├── nn/
│   └── modules/
│       ├── Attention.py          # ECAAttention and other attention modules
│       ├── CoordAttention.py     # Coordinate attention
│       ├── block.py              # CSP and other block modules
│       └── ...
├── models/
│   └── v8/
│       ├── yolov8-ECA-CSP.yaml  # Main custom model config
│       ├── yolov8-ECA.yaml      # ECA-only variant
│       ├── yolov8-CSP.yaml      # CSP-only variant
│       └── ...
├── train_ge_yolov8_kaggle.ipynb # Kaggle training notebook
├── setup.py                      # Package installation script
└── README.md                     # This file
```

## License

This project extends Ultralytics YOLOv8 and follows the same AGPL-3.0 license.

## Acknowledgments

- Built on [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- CSP module based on gradient search optimization
- ECA attention from "ECA-Net: Efficient Channel Attention for Deep Convolutional Neural Networks"

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Citation

If you use this work, please cite:

```bibtex
@software{ge_yolov8,
  title={GE-YOLOv8: YOLOv8 with Gradient Search and ECA Attention},
  author={tunadev-io},
  year={2024},
  url={https://github.com/tunadev-io/Yolov8-GS-ECA}
}
```
