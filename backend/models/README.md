# AI Models Directory

## 📁 Required Model Files

⚠️ **IMPORTANT**: Model files are NOT included in the Git repository due to their large size (exceeding GitHub's 100MB limit).

This directory should contain the following trained YOLO models:

### Active Models (Currently Used):
- **`best.pt`** (39 MB) - Fall detection with YOLOv11
  - Class 0: "fall" - Person is falling
  - Class 1: "no-fall" - Person is NOT falling
- **`ppe_detection.pt`** (136 MB) - Personal Protective Equipment detection
- **`fire_detection.pt`** (15 MB) - Fire detection
- **`smoke_detection.pt`** (5.4 MB) - Smoke detection

### Optional Models (For GRU-based fall detection - currently commented out):
- **`yolo11s-pose.pt`** (19 MB) - Pose estimation
- **`gru_model_binary_old.pth`** (190 KB) - GRU model for temporal analysis

## 🚀 Quick Start

**After cloning this repository**, you need to add the model files to this directory.

## 📥 How to Add Models

### Option 1: Contact VivyaSense Team
Contact **partheeban@vivyacorp.com** to get access to the pre-trained models used in production.

### Option 2: Train Your Own Models

1. Use Ultralytics YOLOv8/YOLOv11 to train custom models
2. Save the trained `.pt` files
3. Place them in this directory (`backend/models/`)

Example:
```bash
# Copy your trained models to this directory
cp /path/to/your/best.pt ./backend/models/
cp /path/to/your/ppe_detection.pt ./backend/models/
cp /path/to/your/fire_detection.pt ./backend/models/
cp /path/to/your/smoke_detection.pt ./backend/models/
```

### Option 3: Use Default YOLOv8 Models (For Testing)

For testing purposes, you can download default YOLO models:
```bash
cd backend/models/

# Download YOLOv8n (general object detection)
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt

# Download YOLOv11s-pose (pose estimation)
wget https://github.com/ultralytics/assets/releases/download/v8.2.0/yolo11s-pose.pt
```

⚠️ **Note**: Default models are for general object detection and won't provide specialized detection (fall, PPE, fire, smoke).

## � Expected Directory Structure

After adding all models, your directory should look like this:

```
backend/models/
├── README.md (this file)
├── best.pt (39 MB - Fall detection)
├── ppe_detection.pt (136 MB - PPE detection)
├── fire_detection.pt (15 MB - Fire detection)
├── smoke_detection.pt (5.4 MB - Smoke detection)
├── yolo11s-pose.pt (19 MB - Optional)
└── gru_model_binary_old.pth (190 KB - Optional)
```

**Total size**: ~215 MB (without optional models)

## 📊 Model Details

### Fall Detection (`best.pt`)
- **Framework**: YOLOv11
- **Size**: 39 MB
- **Classes**:
  - Class 0: "fall" - Person is falling
  - Class 1: "no-fall" - Person is NOT falling
- **Detection Logic**: Only triggers alert when class_id == 0
- **Service**: `FallDetectionService` in `backend/services/fall_detection_service.py`

### PPE Detection (`ppe_detection.pt`)
- **Framework**: YOLOv8
- **Size**: 136 MB
- **Detects**: Helmet, Vest, Gloves, Safety Boots, etc.
- **Use Case**: Workplace safety compliance monitoring

### Fire Detection (`fire_detection.pt`)
- **Framework**: YOLOv8
- **Size**: 15 MB
- **Use Case**: Early fire detection in monitored areas

### Smoke Detection (`smoke_detection.pt`)
- **Framework**: YOLOv8
- **Size**: 5.4 MB
- **Use Case**: Early smoke detection in monitored areas

## 🚀 Training Custom Models

To train custom models using Ultralytics:

```python
from ultralytics import YOLO

# Load a pretrained model
model = YOLO('yolov8n.pt')

# Train the model
results = model.train(
    data='your_dataset.yaml',
    epochs=100,
    imgsz=640,
    batch=16
)

# Save the trained model
model.save('ppe_detection.pt')
```

## 📚 Resources

- [Ultralytics YOLOv8 Documentation](https://docs.ultralytics.com/)
- [Training Custom Models](https://docs.ultralytics.com/modes/train/)
- [Model Export](https://docs.ultralytics.com/modes/export/)

## ⚠️ Troubleshooting

### "Model file not found" Error
If you see errors like "Model file not found":
1. Ensure model files are in the correct directory (`backend/models/`)
2. Check file names match exactly (case-sensitive)
3. Verify files have the correct `.pt` or `.pth` extension

### Model Loading Error
If models fail to load:
1. Ensure you have the correct version of `ultralytics` installed
2. Check that model files are not corrupted
3. Verify you have enough RAM to load the models (minimum 4GB recommended)

## 📞 Contact

For access to pre-trained models or training assistance:
- **Email**: partheeban@vivyacorp.com
- **Repository**: https://github.com/Partheeban123/VivyaSense

## ✅ Summary

- ⚠️ **Model files are NOT in Git** - You must add them manually after cloning
- 📧 **Contact VivyaSense team** to get pre-trained models
- 🎓 **Train your own models** using YOLOv8/YOLOv11
- 🧪 **Use default YOLO models** for testing purposes only

