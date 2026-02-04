# Getting Started with AI Vision Platform 🎯

Welcome! This guide will help you get your AI Vision Platform up and running in minutes.

## 📋 What You Need

Before starting, make sure you have:

1. **Your trained YOLO models** (.pt files):
   - PPE detection model
   - Fall detection model  
   - Fire/smoke detection model

2. **Software installed**:
   - Python 3.10 or higher
   - Node.js 18 or higher
   - Git

3. **Optional** (for easier deployment):
   - Docker Desktop
   - PostgreSQL (or use SQLite for testing)

## 🚀 Quick Start (5 Minutes)

### Step 1: Get the Code

```bash
# Clone the repository
git clone <your-repository-url>
cd ai-vision-platform
```

### Step 2: Run Setup Script

```bash
# Make setup script executable
chmod +x scripts/setup.sh

# Run automated setup
./scripts/setup.sh
```

This script will:
- ✅ Check your system requirements
- ✅ Create Python virtual environment
- ✅ Install all dependencies
- ✅ Create configuration files
- ✅ Set up directory structure

### Step 3: Add Your Models

Copy your trained YOLO model files:

```bash
# Copy your .pt files to the models directory
cp /path/to/your/ppe_detection.pt backend/models/
cp /path/to/your/fall_detection.pt backend/models/
cp /path/to/your/fire_smoke_detection.pt backend/models/
```

### Step 4: Start the Platform

**Option A - Using Docker (Easiest):**

```bash
docker-compose up -d
```

**Option B - Manual Start:**

```bash
# Terminal 1 - Start Backend
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Start Frontend
cd frontend
npm run dev
```

### Step 5: Access the Platform

Open your browser and visit:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs

## 🎯 First Steps

### 1. Test Image Detection

1. Go to http://localhost:3000/detection
2. Click "Upload Image" or drag & drop an image
3. Select detection types (PPE, Fall, Fire)
4. Adjust confidence threshold if needed
5. Click "Run Detection"
6. View results with bounding boxes!

### 2. Try the API

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test detection with an image
curl -X POST "http://localhost:8000/api/detection/image" \
  -F "file=@your_image.jpg" \
  -F "detection_types=ppe,fall,fire" \
  -F "confidence=0.5"
```

### 3. Explore the Dashboard

Visit http://localhost:3000/dashboard to see:
- Detection statistics
- Recent detections
- System status
- Analytics charts

## 📁 Project Structure

```
ai-vision-platform/
├── backend/              # FastAPI backend
│   ├── api/             # API endpoints
│   ├── services/        # Business logic
│   ├── models/          # Your YOLO models go here
│   └── main.py          # Main application
├── frontend/            # Next.js frontend
│   ├── app/            # Pages
│   ├── components/     # React components
│   └── lib/            # Utilities
├── docker-compose.yml  # Docker setup
└── scripts/            # Helper scripts
```

## ⚙️ Configuration

### Backend Configuration

Edit `backend/.env`:

```env
# Your models
PPE_MODEL_PATH=./models/ppe_detection.pt
FALL_MODEL_PATH=./models/fall_detection.pt
FIRE_MODEL_PATH=./models/fire_smoke_detection.pt

# Detection settings
CONFIDENCE_THRESHOLD=0.5

# Database (use SQLite for testing)
DATABASE_URL=sqlite:///./ai_vision.db

# Or use PostgreSQL for production
# DATABASE_URL=postgresql://user:password@localhost:5432/ai_vision_db
```

### Frontend Configuration

Edit `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

## 🔧 Common Tasks

### Add a New Camera

```bash
curl -X POST "http://localhost:8000/api/camera/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Warehouse Camera 1",
    "rtsp_url": "rtsp://camera-ip:554/stream",
    "detection_types": ["ppe", "fall"],
    "confidence_threshold": 0.5
  }'
```

### Process a Video

```bash
curl -X POST "http://localhost:8000/api/video/upload" \
  -F "file=@video.mp4" \
  -F "detection_types=ppe,fall,fire"
```

### View Detection History

```bash
curl "http://localhost:8000/api/dashboard/recent-detections?limit=10"
```

## 📊 Understanding the Results

Detection results include:

```json
{
  "total_detections": 5,
  "detection_counts": {
    "ppe": 3,
    "fall": 1,
    "fire": 1
  },
  "detections": [
    {
      "class_name": "no_helmet",
      "confidence": 0.87,
      "detection_type": "ppe",
      "bbox": [100, 150, 200, 300]
    }
  ],
  "annotated_image_url": "/results/annotated_image.jpg"
}
```

## 🐛 Troubleshooting

### Models Not Loading

**Problem**: Error loading YOLO models

**Solution**:
```bash
# Check if models exist
ls -lh backend/models/

# Verify paths in .env
cat backend/.env | grep MODEL_PATH
```

### Port Already in Use

**Problem**: Port 8000 or 3000 already in use

**Solution**:
```bash
# Backend - use different port
uvicorn main:app --reload --port 8001

# Frontend - use different port
npm run dev -- -p 3001
```

### Database Connection Error

**Problem**: Can't connect to database

**Solution**: Use SQLite for testing:
```env
DATABASE_URL=sqlite:///./ai_vision.db
```

## 📚 Next Steps

1. **Read the Full Documentation**
   - [README.md](README.md) - Complete documentation
   - [QUICKSTART.md](QUICKSTART.md) - Quick reference
   - [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment

2. **Customize the Platform**
   - Modify frontend components
   - Add custom detection logic
   - Configure alerts and notifications

3. **Deploy to Production**
   - Follow [DEPLOYMENT.md](DEPLOYMENT.md)
   - Set up SSL certificates
   - Configure monitoring

## 🎓 Learning Resources

- **FastAPI Tutorial**: https://fastapi.tiangolo.com/tutorial/
- **Next.js Documentation**: https://nextjs.org/docs
- **YOLOv8 Guide**: https://docs.ultralytics.com/
- **Docker Compose**: https://docs.docker.com/compose/

## 💡 Tips

1. **Start Simple**: Test with images before videos
2. **Adjust Confidence**: Lower threshold = more detections (but more false positives)
3. **Use GPU**: Much faster detection with CUDA-enabled GPU
4. **Monitor Logs**: Check logs for errors and performance
5. **Backup Models**: Keep copies of your trained models

## 🤝 Need Help?

- Check the [FAQ section](README.md#faq)
- View [API Documentation](http://localhost:8000/api/docs)
- Review [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- Open an issue on GitHub

## ✅ Checklist

Before going to production:

- [ ] All models are loaded successfully
- [ ] Image detection works correctly
- [ ] Video processing works
- [ ] Database is configured
- [ ] Environment variables are set
- [ ] SSL certificates are configured
- [ ] Backups are set up
- [ ] Monitoring is enabled
- [ ] Security settings are reviewed

---

**🎉 You're all set!** Start detecting with AI Vision Platform!

For detailed information, see [README.md](README.md) and [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md).

