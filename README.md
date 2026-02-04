# VivyaSense - AI Vision Platform 🎥🤖

**AI CCTV Surveillance System**

A production-ready AI-powered video surveillance platform with real-time detection capabilities for PPE, fall, and fire/smoke detection using advanced deep learning models.

## 🌟 Features

- **PPE Detection**: Automatically detect missing safety equipment (helmets, vests, gloves)
- **Fall Detection**: Instant alerts when a person falls
- **Fire & Smoke Detection**: Early detection of fire and smoke hazards
- **Real-time Processing**: Process video streams in real-time
- **Dashboard & Analytics**: Comprehensive monitoring and reporting
- **Multi-camera Support**: Manage multiple camera feeds simultaneously
- **REST API**: Full-featured API for integration
- **WebSocket Streaming**: Real-time video streaming with detections

## 🏗️ Architecture

```
ai-vision-platform/
├── backend/          # FastAPI backend with AI models
├── frontend/         # Next.js frontend
├── docker/           # Docker configurations
└── docs/            # Documentation
```

## 🚀 Quick Start

### 📱 Network Access (Access from Any Device)

**One-command startup for network access:**
```bash
./start-network.sh
```

This automatically:
- Detects your IP address
- Configures backend and frontend
- Starts both servers
- Shows access URLs for all devices

**Access from any device on your WiFi:**
- Web Interface: `http://192.168.1.23:3001`
- API Backend: `http://192.168.1.23:8000`

📖 **See [QUICK_START.md](QUICK_START.md) for detailed network setup**
📖 **See [NETWORK_SETUP.md](NETWORK_SETUP.md) for troubleshooting**

---

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 15+ (optional, SQLite by default)
- Redis 7+ (optional)
- Docker & Docker Compose (optional)

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
```bash
git clone <your-repo>
cd ai-vision-platform
```

2. **Add your trained models**
```bash
# Place your trained .pt files in backend/models/
cp /path/to/your/ppe_detection.pt backend/models/
cp /path/to/your/fall_detection.pt backend/models/
cp /path/to/your/fire_smoke_detection.pt backend/models/
```

3. **Configure environment**
```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your settings
```

4. **Start all services**
```bash
docker-compose up -d
```

5. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

### Option 2: Manual Setup

#### Backend Setup

1. **Create virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup database**
```bash
# Start PostgreSQL and Redis
# Update DATABASE_URL in .env

# Run migrations
python -c "from database.database import init_db; init_db()"
```

4. **Add your models**
```bash
mkdir -p models
cp /path/to/your/*.pt models/
```

5. **Start backend**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

1. **Install dependencies**
```bash
cd frontend
npm install
```

2. **Configure environment**
```bash
# Create .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

3. **Start frontend**
```bash
npm run dev
```

## 📁 Project Structure

### Backend
```
backend/
├── api/              # API endpoints
│   ├── auth.py       # Authentication
│   ├── detection.py  # Detection endpoints
│   ├── video.py      # Video processing
│   ├── camera.py     # Camera management
│   └── dashboard.py  # Analytics
├── core/             # Core configurations
│   ├── config.py     # Settings
│   └── logger.py     # Logging
├── database/         # Database models
│   ├── models.py     # SQLAlchemy models
│   └── database.py   # DB connection
├── services/         # Business logic
│   ├── detection_service.py  # AI detection
│   └── video_service.py      # Video processing
├── websocket/        # WebSocket handlers
└── main.py          # FastAPI app
```

### Frontend
```
frontend/
├── app/              # Next.js app directory
│   ├── page.tsx      # Landing page
│   ├── dashboard/    # Dashboard pages
│   ├── detection/    # Detection demo
│   └── cameras/      # Camera management
├── components/       # React components
│   ├── layout/       # Layout components
│   ├── ui/          # UI components
│   └── features/    # Feature components
└── lib/             # Utilities
```

## 🔧 Configuration

### Backend Configuration (.env)

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ai_vision_db

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Security
SECRET_KEY=your-secret-key-here

# AI Models
PPE_MODEL_PATH=./models/ppe_detection.pt
FALL_MODEL_PATH=./models/fall_detection.pt
FIRE_MODEL_PATH=./models/fire_smoke_detection.pt
CONFIDENCE_THRESHOLD=0.5
```

## 📡 API Endpoints

### Detection
- `POST /api/detection/image` - Detect objects in image
- `GET /api/detection/models` - List available models

### Video
- `POST /api/video/upload` - Upload and process video
- `GET /api/video/status/{job_id}` - Get processing status

### Camera
- `POST /api/camera/` - Create camera
- `GET /api/camera/` - List cameras
- `POST /api/camera/{id}/start` - Start camera stream

### Dashboard
- `GET /api/dashboard/stats` - Get statistics
- `GET /api/dashboard/trends` - Get detection trends

Full API documentation: http://localhost:8000/api/docs

## 🎯 Usage Examples

### 1. Image Detection

```python
import requests

url = "http://localhost:8000/api/detection/image"
files = {"file": open("image.jpg", "rb")}
data = {"detection_types": "ppe,fall,fire", "confidence": 0.5}

response = requests.post(url, files=files, data=data)
print(response.json())
```

### 2. Video Processing

```python
url = "http://localhost:8000/api/video/upload"
files = {"file": open("video.mp4", "rb")}
data = {"detection_types": "ppe,fall,fire"}

response = requests.post(url, files=files, data=data)
job_id = response.json()["job_id"]
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📊 Performance

- **Detection Speed**: ~30 FPS on GPU, ~10 FPS on CPU
- **Supported Formats**: MP4, AVI, MOV, MKV
- **Max Video Size**: 500 MB (configurable)
- **Concurrent Streams**: Up to 100 (configurable)

## 🔒 Security

- JWT-based authentication
- HTTPS support
- CORS configuration
- Rate limiting
- Input validation

## 📝 License

MIT License - see LICENSE file

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md

## 📧 Support

For issues and questions, please open a GitHub issue.

---

Built with ❤️ using FastAPI, Next.js, and advanced AI technologies
