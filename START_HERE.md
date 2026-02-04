# 🚀 Quick Start - AI Vision Platform

## ✅ Setup Complete!

Your AI Vision Platform is now set up and ready to use!

## 📍 Where to Run Commands

**IMPORTANT**: Run all commands from the `ai-vision-platform` directory:

```bash
cd /Users/partheebandevaraj/ai-vision-platform
```

## 🎯 Step 1: Add Your YOLO Models

Before starting the servers, copy your trained model files:

```bash
# Copy your .pt files to the models directory
cp /path/to/your/ppe_detection.pt backend/models/
cp /path/to/your/fall_detection.pt backend/models/
cp /path/to/your/fire_smoke_detection.pt backend/models/
```

**Note**: The platform will work without models, but detection features won't function until you add them.

## 🚀 Step 2: Start the Backend Server

Open a **new terminal** and run:

```bash
cd /Users/partheebandevaraj/ai-vision-platform/backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Backend will be available at**: http://localhost:8000

## 🎨 Step 3: Start the Frontend Server

Open **another new terminal** and run:

```bash
cd /Users/partheebandevaraj/ai-vision-platform/frontend
npm run dev
```

You should see:
```
  ▲ Next.js 14.1.0
  - Local:        http://localhost:3000
  - Ready in 2.5s
```

**Frontend will be available at**: http://localhost:3000

## 🌐 Step 4: Access the Platform

Open your browser and visit:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs

## 🎯 What You Can Do Now

### 1. Explore the Landing Page
Visit http://localhost:3000 to see the beautiful landing page with:
- Feature showcase
- Technology highlights
- Call-to-action buttons

### 2. Try the Detection Demo
Go to http://localhost:3000/detection to:
- Upload images for detection
- Select detection types (PPE, Fall, Fire)
- Adjust confidence threshold
- View results with bounding boxes

### 3. Test the API
Visit http://localhost:8000/api/docs to:
- See all available endpoints
- Test API calls directly
- View request/response schemas

## 🔧 Troubleshooting

### Issue: "localhost refused to connect"

**Solution**: Make sure both servers are running:
1. Check backend: http://localhost:8000/health
2. Check frontend: http://localhost:3000

### Issue: "Models not found"

**Solution**: Add your .pt model files to `backend/models/` directory

### Issue: Port already in use

**Solution**: Change the port:
```bash
# Backend - use port 8001
uvicorn main:app --reload --port 8001

# Frontend - use port 3001
npm run dev -- -p 3001
```

## 📁 Project Structure

```
ai-vision-platform/
├── backend/              # FastAPI backend
│   ├── venv/            # Python virtual environment
│   ├── models/          # Your YOLO models go here
│   ├── api/             # API endpoints
│   └── main.py          # Main application
├── frontend/            # Next.js frontend
│   ├── app/            # Pages
│   ├── components/     # React components
│   └── package.json    # Dependencies
└── docs/               # Documentation
```

## 🎓 Next Steps

1. **Add Your Models**: Copy your .pt files to `backend/models/`
2. **Test Detection**: Upload an image at http://localhost:3000/detection
3. **Customize**: Modify the frontend components to match your brand
4. **Deploy**: Follow DEPLOYMENT.md for production deployment

## 📚 Documentation

- **README.md** - Complete documentation
- **QUICKSTART.md** - Quick reference guide
- **GETTING_STARTED.md** - Detailed setup guide
- **DEPLOYMENT.md** - Production deployment
- **PROJECT_SUMMARY.md** - Project overview

## 🆘 Need Help?

1. Check the documentation files above
2. Visit http://localhost:8000/api/docs for API reference
3. Review the error messages in the terminal

## 🎉 You're All Set!

Your AI Vision Platform is ready to use. Start by adding your YOLO models and testing the detection features!

---

**Happy Detecting! 🚀**

