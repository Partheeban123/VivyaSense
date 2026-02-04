# 🔥 Fire and Smoke Detection Setup Guide

## Overview
This guide will help you set up fire and smoke detection using your trained YOLO models.

## 📋 Prerequisites
- `best_model1.pt` - Fire/Smoke detection model (detects both fire and smoke)

## 🚀 Setup Steps

### Step 1: Copy Model Files

Run the provided script to copy models from Downloads:

```bash
cd backend
./copy_fire_smoke_models.sh
```

Or manually copy the file:

```bash
cp ~/Downloads/best_model1.pt backend/models/fire_detection.pt
```

**Note**: We only need `fire_detection.pt` as it detects both fire and smoke!

### Step 2: Verify Models

Check that models are in place:

```bash
ls -lh backend/models/*.pt
```

You should see:
- `fire_detection.pt` (Fire/Smoke detection model - detects both!)
- `yolo11s-pose.pt` (Fall detection - already there)
- `gru_model_binary_old.pth` (Fall GRU model - already there)

### Step 3: Restart Backend Server

The backend needs to be restarted to load the new models:

```bash
# Kill current backend process (Ctrl+C in the terminal)
# Then restart:
cd backend
source venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see in the logs:
```
INFO | ✅ Loaded fire/smoke detection model from ./models/fire_detection.pt
INFO |    Model classes: {0: 'smoke', 1: 'fire'}
INFO |    Fire class ID: 1, Smoke class ID: 0
```

## 🎯 Testing Fire and Smoke Detection

### Option 1: Using the Frontend (Easiest)

1. Go to http://192.168.1.17:3000/detection
2. Upload an image with fire or smoke
3. Check the "Fire" checkbox
4. Click "Run Detection"
5. View results with bounding boxes!

### Option 2: Using API Docs (Swagger UI)

1. Go to http://192.168.1.17:8000/api/docs
2. Find `POST /api/detection/fire-smoke`
3. Click "Try it out"
4. Upload your test image
5. Set `detection_mode` to:
   - `"fire"` - Detect only fire
   - `"smoke"` - Detect only smoke
   - `"both"` - Detect both fire and smoke
6. Click "Execute"

### Option 3: Using cURL

```bash
# Detect both fire and smoke
curl -X POST "http://192.168.1.17:8000/api/detection/fire-smoke" \
  -F "file=@test_image.jpg" \
  -F "detection_mode=both" \
  -F "confidence=0.5" \
  -F "draw_boxes=true"

# Detect only fire
curl -X POST "http://192.168.1.17:8000/api/detection/fire-smoke" \
  -F "file=@test_image.jpg" \
  -F "detection_mode=fire" \
  -F "confidence=0.5"

# Detect only smoke
curl -X POST "http://192.168.1.17:8000/api/detection/fire-smoke" \
  -F "file=@test_image.jpg" \
  -F "detection_mode=smoke" \
  -F "confidence=0.5"
```

### Option 4: Using the General Detection Endpoint

```bash
# Detect fire and smoke together with other types
curl -X POST "http://192.168.1.17:8000/api/detection/image" \
  -F "file=@test_image.jpg" \
  -F "detection_types=fire,smoke" \
  -F "confidence=0.5" \
  -F "draw_boxes=true"

# Detect all three types: PPE, Fall, Fire, Smoke
curl -X POST "http://192.168.1.17:8000/api/detection/image" \
  -F "file=@test_image.jpg" \
  -F "detection_types=ppe,fall,fire,smoke" \
  -F "confidence=0.5"
```

## 📊 Expected Response

```json
{
  "success": true,
  "detection_mode": "both",
  "fire_detections": [
    {
      "class_id": 0,
      "class_name": "fire",
      "confidence": 0.95,
      "bounding_box": {
        "x1": 100.5,
        "y1": 200.3,
        "x2": 300.7,
        "y2": 400.9
      },
      "detection_type": "fire"
    }
  ],
  "smoke_detections": [...],
  "total_detections": 2,
  "has_fire": true,
  "has_smoke": true,
  "alert_level": "critical",
  "annotated_image_url": "/results/fire_smoke_abc123.jpg",
  "timestamp": "2026-01-19T10:45:00"
}
```

## 🎨 Alert Levels

- **critical**: Both fire and smoke detected
- **high**: Fire detected
- **medium**: Smoke detected
- **none**: No detections

## 🔧 Configuration

Models are configured in `backend/core/config.py`:

```python
FIRE_DETECTION_MODEL_PATH: str = "./models/fire_detection.pt"
SMOKE_DETECTION_MODEL_PATH: str = "./models/smoke_detection.pt"
FIRE_SMOKE_CONFIDENCE_THRESHOLD: float = 0.5
```

## 📁 Files Created/Modified

### New Files:
- `backend/services/fire_smoke_detection_service.py` - Fire/smoke detection service
- `backend/copy_fire_smoke_models.sh` - Model copy script
- `FIRE_SMOKE_DETECTION_SETUP.md` - This guide

### Modified Files:
- `backend/core/config.py` - Added fire/smoke model paths
- `backend/api/detection.py` - Added fire/smoke detection endpoints
- `backend/main.py` - Updated CORS for network access

## 🎉 Success!

Once you see the models loaded in the backend logs, you're ready to detect fire and smoke in real-time!

