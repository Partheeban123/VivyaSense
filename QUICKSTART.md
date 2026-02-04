# Quick Start Guide 🚀

Get your AI Vision Platform up and running in 5 minutes!

## Prerequisites

- Python 3.10+
- Node.js 18+
- Your trained YOLO models (.pt files)

## Step 1: Clone and Setup

```bash
# Run the automated setup script
./scripts/setup.sh
```

This will:
- Create Python virtual environment
- Install all dependencies
- Create configuration files
- Set up directory structure

## Step 2: Add Your YOLO Models

Copy your trained model files to the backend/models directory:

```bash
cp /path/to/your/ppe_detection.pt backend/models/
cp /path/to/your/fall_detection.pt backend/models/
cp /path/to/your/fire_smoke_detection.pt backend/models/
```

## Step 3: Configure Database (Optional for Quick Start)

For quick testing, you can use SQLite instead of PostgreSQL:

Edit `backend/.env`:
```env
DATABASE_URL=sqlite:///./ai_vision.db
```

## Step 4: Start the Backend

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload
```

Backend will start at: http://localhost:8000

## Step 5: Start the Frontend

Open a new terminal:

```bash
cd frontend
npm run dev
```

Frontend will start at: http://localhost:3000

## Step 6: Test the Platform

### Test Image Detection

1. Go to http://localhost:3000/detection
2. Upload an image
3. Select detection types (PPE, Fall, Fire)
4. Click "Detect"
5. View results with bounding boxes

### Test API Directly

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test detection with an image
curl -X POST "http://localhost:8000/api/detection/image" \
  -F "file=@test_image.jpg" \
  -F "detection_types=ppe,fall,fire" \
  -F "confidence=0.5"
```

### View API Documentation

Visit: http://localhost:8000/api/docs

## Common Issues

### Issue: Models not loading

**Solution**: Check that your .pt files are in `backend/models/` and the paths in `.env` are correct.

### Issue: Database connection error

**Solution**: For quick start, use SQLite:
```env
DATABASE_URL=sqlite:///./ai_vision.db
```

### Issue: Port already in use

**Solution**: Change ports in configuration:
- Backend: Edit `backend/.env` PORT variable
- Frontend: Use `npm run dev -- -p 3001`

## Next Steps

1. **Add Cameras**: Go to http://localhost:3000/cameras to add RTSP streams
2. **View Dashboard**: Check http://localhost:3000/dashboard for analytics
3. **Process Videos**: Upload videos for batch processing
4. **Configure Alerts**: Set up email/SMS alerts for detections

## Production Deployment

For production deployment with Docker:

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Need Help?

- Check the full README.md for detailed documentation
- View API docs at http://localhost:8000/api/docs
- Open an issue on GitHub

---

**Congratulations! 🎉** Your AI Vision Platform is now running!

