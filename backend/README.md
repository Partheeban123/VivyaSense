# VivyaSense Backend

FastAPI backend for the AI Vision Platform with real-time RTSP camera streaming and AI-powered detection.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- AI model files (see `models/README.md`)

### Installation

1. **Create virtual environment**:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Add AI models**:
See `models/README.md` for instructions on adding model files.

4. **Configure environment** (optional):
Create `.env` file if you need custom configuration.

5. **Start the server**:
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

## 📁 Project Structure

```
backend/
├── api/                   # API endpoints
│   ├── auth.py           # Authentication
│   ├── camera.py         # Camera management
│   ├── contact.py        # Contact form
│   ├── dashboard.py      # Dashboard stats
│   ├── detection.py      # Detection endpoints
│   └── video.py          # Video streaming
├── core/                 # Core configuration
│   ├── config.py         # App configuration
│   └── logger.py         # Logging setup
├── database/             # Database models and setup
│   ├── database.py       # Database connection
│   └── models.py         # SQLAlchemy models
├── models/               # AI model files (NOT in Git)
│   ├── README.md         # Model setup instructions
│   ├── best.pt           # Fall detection (add manually)
│   ├── ppe_detection.pt  # PPE detection (add manually)
│   ├── fire_detection.pt # Fire detection (add manually)
│   └── smoke_detection.pt # Smoke detection (add manually)
├── schemas/              # Pydantic schemas
├── services/             # Business logic
│   ├── detection_service.py        # General detection
│   ├── fall_detection_service.py   # Fall detection
│   ├── ppe_detection_service.py    # PPE detection
│   ├── fire_smoke_detection_service.py # Fire/Smoke
│   ├── video_service.py            # Video processing
│   └── email_service.py            # Email notifications
├── utils/                # Utility functions
├── websocket/            # WebSocket handlers
│   └── stream_handler.py # Real-time streaming
├── main.py               # FastAPI application
├── requirements.txt      # Python dependencies
└── ai_vision.db          # SQLite database (auto-created)
```

## 🎯 Features

### ✅ Implemented Features
- **Real-time RTSP Streaming**: WebSocket-based live camera feeds
- **AI Detection**:
  - Fall detection with YOLOv11 (`best.pt`)
  - PPE detection (helmet, vest, gloves, boots)
  - Fire detection
  - Smoke detection
- **Camera Management**: CRUD operations for RTSP cameras
- **SQLite Database**: Lightweight database for development
- **Email Notifications**: Contact form with SMTP support
- **CORS Support**: Configured for frontend integration
- **Health Check**: `/health` endpoint for monitoring

### 🎯 Detection Services

#### 1. Fall Detection
- **Model**: `best.pt` (YOLOv11, 39 MB)
- **Classes**: 
  - Class 0: "fall" - Person is falling
  - Class 1: "no-fall" - Person is NOT falling
- **Logic**: Only triggers alert when `class_id == 0`
- **Service**: `FallDetectionService`

#### 2. PPE Detection
- **Model**: `ppe_detection.pt` (YOLOv8, 136 MB)
- **Detects**: Helmet, Vest, Gloves, Safety Boots
- **Service**: `PPEDetectionService`

#### 3. Fire Detection
- **Model**: `fire_detection.pt` (YOLOv8, 15 MB)
- **Service**: `FireSmokeDetectionService`

#### 4. Smoke Detection
- **Model**: `smoke_detection.pt` (YOLOv8, 5.4 MB)
- **Service**: `FireSmokeDetectionService`

## 🔧 Configuration

### Environment Variables

Create `.env` file (optional):

```bash
# Database
DATABASE_URL=sqlite:///./ai_vision.db

# Email (for contact form)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=your-email@gmail.com

# Detection thresholds
CONFIDENCE_THRESHOLD=0.31
IOU_THRESHOLD=0.45
```

### CORS Configuration

Update `main.py` to add your frontend URL:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://192.168.0.127:3000",
        # Add your frontend URL here
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📡 API Endpoints

### Camera Management
- `GET /api/camera/` - List all cameras
- `POST /api/camera/` - Add new camera
- `GET /api/camera/{id}` - Get camera details
- `PUT /api/camera/{id}` - Update camera
- `DELETE /api/camera/{id}` - Delete camera

### Detection
- `POST /api/detection/detect` - Run detection on image/video
- `GET /api/detection/results` - Get detection results

### WebSocket
- `WS /ws/stream/{camera_id}` - Real-time video streaming

### Health Check
- `GET /health` - Server health status

### Contact Form
- `POST /api/contact/` - Submit contact form

## 🛠️ Development

### Running Tests
```bash
# Test fall detection
python test_fall_detection.py

# Test contact form
python test_contact.py

# Test email service
python test_email.py
```

### Database Management
```bash
# The database is auto-created on first run
# Location: backend/ai_vision.db

# To reset the database, simply delete the file:
rm ai_vision.db
```

## 📦 Dependencies

### Main Dependencies
- **FastAPI**: Modern web framework
- **Uvicorn**: ASGI server
- **SQLAlchemy**: ORM for database
- **Ultralytics**: YOLOv8/YOLOv11 for AI detection
- **OpenCV**: Video processing
- **Pillow**: Image processing
- **python-multipart**: File uploads
- **python-jose**: JWT authentication
- **passlib**: Password hashing

See `requirements.txt` for full list.

## 🐛 Troubleshooting

### Model File Not Found
See `models/README.md` for instructions on adding model files.

### Port 8000 Already in Use
```bash
# Kill the process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### RTSP Camera Connection Failed
1. Verify RTSP URL is correct
2. Check camera is accessible from your network
3. Ensure firewall allows RTSP connections (port 554)

### Email Not Sending
1. Check SMTP credentials in `.env`
2. For Gmail, use App Password (not regular password)
3. Enable "Less secure app access" or use OAuth2

## 📞 Contact

- **Email**: partheeban@vivyacorp.com
- **Repository**: https://github.com/Partheeban123/VivyaSense

## 📄 License

Proprietary - VivyaCorp

