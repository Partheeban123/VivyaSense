# VivyaSense Frontend

Modern Next.js 14 frontend for the AI Vision Platform with real-time RTSP camera monitoring and AI-powered detection.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Backend server running at `http://192.168.0.127:8000` (or update `.env.local`)

### Installation

1. **Install dependencies**:
```bash
cd frontend
npm install
```

2. **Configure environment variables**:
Create or update `.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://192.168.0.127:8000
NEXT_PUBLIC_WS_URL=ws://192.168.0.127:8000
```

3. **Start the development server**:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000` (or the next available port like 3001, 3002).

## 📁 Project Structure

```
frontend/
├── app/                    # Next.js 14 App Router
│   ├── page.tsx           # Home page with hero section
│   ├── dashboard/         # Main dashboard
│   ├── cameras/           # Camera management
│   ├── detection/         # Detection results
│   ├── analytics/         # Analytics and reports
│   ├── contact/           # Contact form
│   └── layout.tsx         # Root layout
├── components/            # Reusable components
│   ├── animations/        # Framer Motion animations
│   ├── layout/           # Navbar, Footer
│   └── ui/               # UI components
├── public/               # Static assets
├── .env.local           # Environment variables (create this)
└── package.json         # Dependencies
```

## 🎨 Features

### ✅ Implemented Features
- **Real-time RTSP Streaming**: Live camera feeds with WebSocket support
- **AI Detection Dashboard**: 
  - Fall detection with YOLOv11
  - PPE (Personal Protective Equipment) detection
  - Fire and smoke detection
- **Camera Management**: Add, edit, delete RTSP cameras
- **Modern UI**: Built with Tailwind CSS and Framer Motion
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Contact Form**: Email notifications via backend API

### 🎯 Detection Types
1. **Fall Detection**: Real-time fall detection with alerts
2. **PPE Detection**: Helmet, vest, gloves, safety boots
3. **Fire Detection**: Early fire detection
4. **Smoke Detection**: Early smoke detection

## 🔧 Configuration

### Environment Variables

Create `.env.local` in the frontend directory:

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://192.168.0.127:8000

# WebSocket URL for real-time streaming
NEXT_PUBLIC_WS_URL=ws://192.168.0.127:8000
```

**Important**: Update the IP address to match your backend server's IP.

### Finding Your IP Address

**On Mac/Linux**:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

**On Windows**:
```bash
ipconfig
```

## 📦 Dependencies

### Main Dependencies
- **Next.js 14.1.0**: React framework with App Router
- **React 18**: UI library
- **Tailwind CSS**: Utility-first CSS framework
- **Framer Motion**: Animation library
- **Lucide React**: Icon library

### Development Dependencies
- **TypeScript**: Type safety
- **ESLint**: Code linting
- **PostCSS**: CSS processing

## 🛠️ Available Scripts

```bash
# Development server
npm run dev

# Production build
npm run build

# Start production server
npm start

# Lint code
npm run lint
```

## 🌐 API Integration

The frontend communicates with the backend via:

### REST API
- **Base URL**: `NEXT_PUBLIC_API_URL`
- **Endpoints**:
  - `GET /api/camera/` - List all cameras
  - `POST /api/camera/` - Add new camera
  - `PUT /api/camera/{id}` - Update camera
  - `DELETE /api/camera/{id}` - Delete camera
  - `POST /api/contact/` - Submit contact form

### WebSocket
- **URL**: `NEXT_PUBLIC_WS_URL/ws/stream/{camera_id}`
- **Purpose**: Real-time video streaming and detection results

## 🎨 UI Components

### Animations
- **Framer Motion**: Smooth page transitions and micro-interactions
- **Scroll Reveal**: Elements animate on scroll
- **Counter Animation**: Animated statistics
- **Particle Background**: Dynamic background effects

### Layout
- **Navbar**: Responsive navigation with mobile menu
- **Footer**: Company information and links
- **Typography**: Consistent text styles

## 📱 Responsive Design

The UI is fully responsive and tested on:
- **Desktop**: 1920x1080 and above
- **Tablet**: 768px - 1024px
- **Mobile**: 375px - 767px

## 🐛 Troubleshooting

### Port Already in Use
If port 3000 is in use, Next.js will automatically use the next available port (3001, 3002, etc.).

### CORS Errors
Ensure the backend CORS configuration includes your frontend URL:
```python
# backend/main.py
allow_origins=[
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://192.168.0.127:3000",
    # ... add your IP and port
]
```

### WebSocket Connection Failed
1. Check backend is running
2. Verify `NEXT_PUBLIC_WS_URL` in `.env.local`
3. Ensure firewall allows WebSocket connections

## 📞 Contact

- **Email**: partheeban@vivyacorp.com
- **Repository**: https://github.com/Partheeban123/VivyaSense

## 📄 License

Proprietary - VivyaCorp

