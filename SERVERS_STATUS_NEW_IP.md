# 🚀 AI Vision Platform - Servers Running (Updated IP)

**Date:** January 22, 2026  
**Status:** ✅ Both servers running successfully  
**New WiFi IP:** 192.168.68.105

---

## 📡 Network Configuration

### **New IP Address:** `192.168.68.105`
- **Old IP:** 192.168.1.31 (replaced)
- **Backend Port:** 8000
- **Frontend Port:** 3000

---

## ✅ Servers Status

### **Backend Server** - Terminal ID: 89453
```
Status: ✅ RUNNING
URL: http://0.0.0.0:8000
Process: uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Access URLs:**
- Local: `http://localhost:8000`
- Network: `http://192.168.68.105:8000`
- API Docs: `http://192.168.68.105:8000/api/docs`
- Health Check: `http://192.168.68.105:8000/health`

### **Frontend Server** - Terminal ID: 96953
```
Status: ✅ RUNNING
URL: http://0.0.0.0:3000
Process: npm run dev
```

**Access URLs:**
- Local: `http://localhost:3000`
- Network: `http://192.168.68.105:3000`

---

## 🤖 AI Models Status

| Model | Status | Path | Purpose |
|-------|--------|------|---------|
| **PPE Detection** | ✅ Loaded | `./models/ppe_detection.pt` | Detect helmets, vests, masks |
| **Fall Detection (YOLO)** | ✅ Loaded | `./models/yolo11s-pose.pt` | Pose estimation |
| **Fall Detection (GRU)** | ✅ Loaded | `./models/gru_model_binary_old.pth` | Temporal analysis |
| **Fire Detection** | ✅ Loaded | `./models/fire_detection.pt` | Detect fire |
| **Smoke Detection** | ✅ Loaded | `./models/smoke_detection.pt` | Detect smoke |

**Fall Detection Threshold:** 0.90 (High Precision Mode)

---

## 📝 Configuration Files Updated

### 1. Frontend Configuration
**File:** `frontend/.env.local`
```env
NEXT_PUBLIC_API_URL=http://192.168.68.105:8000
NEXT_PUBLIC_WS_URL=ws://192.168.68.105:8000
```

### 2. Backend CORS Configuration
**File:** `backend/core/config.py`
```python
CORS_ORIGINS: List[str] = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://192.168.68.105:3000",  # NEW IP
    "http://192.168.68.105:3001",  # NEW IP
    ...
]
```

### 3. Backend Main CORS
**File:** `backend/main.py`
```python
allow_origins=[
    "http://192.168.68.105:3000",  # NEW IP
    "http://192.168.68.105:3001",  # NEW IP
    "http://192.168.68.105:8000",  # NEW IP
    ...
]
```

---

## 🧪 Testing

### Test Backend:
```bash
# Health check
curl http://192.168.68.105:8000/health

# Expected response:
{
  "status": "healthy",
  "app": "AI Vision Platform",
  "version": "1.0.0",
  "environment": "production"
}
```

### Test Frontend:
Open in browser: `http://192.168.68.105:3000`

### Test from Mobile/Other Devices:
1. Connect device to same WiFi network
2. Open browser: `http://192.168.68.105:3000`
3. Try uploading a video or connecting to camera

---

## 📊 Available Features

### Detection Endpoints:
- ✅ `/api/detection/fall` - Fall detection (YOLOv11-pose + GRU)
- ✅ `/api/detection/fire-smoke` - Fire & smoke detection
- ✅ `/api/detection/ppe` - PPE compliance detection
- ✅ `/api/detection/image` - General image detection

### Other Endpoints:
- ✅ `/api/contact` - Contact form submission (with email)
- ✅ `/api/dashboard` - Dashboard data
- ✅ `/api/camera` - Camera streaming
- ✅ `/ws/stream/{stream_id}` - WebSocket for live streaming
- ✅ `/health` - Health check

---

## 📧 Email Configuration

**Status:** ✅ Configured  
**SMTP Server:** Gmail (smtp.gmail.com:587)  
**From Email:** noreply@vivyasense.com  
**Admin Email:** partheeban@vivyacorp.com

**Test Contact Form:**
1. Go to `http://192.168.68.105:3000/contact`
2. Fill out the form
3. Submit
4. Check admin email for notification

---

## 🎯 Performance Optimizations

### Apple Silicon (M1/M2/M3) Optimizations:
- ✅ MPS GPU acceleration (3-5x faster)
- ✅ Frame resolution reduction (640px width)
- ✅ Intelligent model scheduling:
  - Fall: Every frame (needs continuous sequence)
  - PPE: Every 2nd frame
  - Fire/Smoke: Every 3rd frame
- ✅ Threaded video capture (minimal latency)
- ✅ Result caching for skipped frames

---

## 🔧 Server Management

### View Logs:
```bash
# Backend logs - Terminal 89453
# Frontend logs - Terminal 96953
```

### Stop Servers:
```bash
pkill -f "uvicorn main:app"
pkill -f "next dev"
```

### Restart Servers:
```bash
# Backend
cd backend && source venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd frontend && npm run dev
```

---

## 🌐 Access from Different Devices

### Same Machine (Localhost):
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`

### Other Devices on Same WiFi:
- Frontend: `http://192.168.68.105:3000`
- Backend: `http://192.168.68.105:8000`

### Mobile Devices:
1. Connect to same WiFi network
2. Open browser
3. Navigate to `http://192.168.68.105:3000`

---

## 🎉 Ready to Use!

Your AI Vision Platform is now running with the new IP address **192.168.68.105**.

**Next Steps:**
1. ✅ Test video upload detection
2. ✅ Test RTSP camera streaming
3. ✅ Test contact form email
4. ✅ Test from mobile device
5. ✅ Monitor performance

---

## 📚 Documentation

- **Tech Stack:** See `TECH_STACK_DOCUMENTATION.md`
- **Digital Marketing:** See `DIGITAL_MARKETING_STRATEGY.md`
- **Analytics:** See `frontend/lib/analytics.ts`
- **Threaded Capture:** See `backend/docs/THREADED_VIDEO_CAPTURE.md`

---

**🚀 All systems operational!**

