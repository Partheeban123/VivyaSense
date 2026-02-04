#!/bin/bash

# AI Vision Platform - Network Startup Script
# This script starts both backend and frontend servers for network access

echo "🚀 Starting AI Vision Platform for Network Access"
echo "=================================================="

# Get current IP address
CURRENT_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)

if [ -z "$CURRENT_IP" ]; then
    echo "❌ Error: Could not detect IP address"
    echo "Please check your network connection"
    exit 1
fi

echo "📡 Detected IP Address: $CURRENT_IP"
echo ""

# Check if .env.local has the correct IP
FRONTEND_ENV="frontend/.env.local"
if grep -q "$CURRENT_IP" "$FRONTEND_ENV"; then
    echo "✅ Frontend configuration is up to date"
else
    echo "⚠️  Updating frontend configuration with current IP..."
    cat > "$FRONTEND_ENV" << EOF
# Network Configuration for Multi-Device Access
# Current Local IP: $CURRENT_IP

# Use WiFi IP for network access from all devices (phones, tablets, other computers)
NEXT_PUBLIC_API_URL=http://$CURRENT_IP:8000
NEXT_PUBLIC_WS_URL=ws://$CURRENT_IP:8000

# For localhost only access (same machine), use:
# NEXT_PUBLIC_API_URL=http://localhost:8000
# NEXT_PUBLIC_WS_URL=ws://localhost:8000

# Note: If your IP changes, update the IP address above
# To find your current IP: ifconfig | grep "inet " | grep -v 127.0.0.1
EOF
    echo "✅ Frontend configuration updated"
fi

echo ""
echo "🔧 Starting Backend Server..."
echo "================================"

# Kill existing backend process
pkill -f "uvicorn main:app" 2>/dev/null

# Start backend in background
cd backend
source venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

echo "✅ Backend started (PID: $BACKEND_PID)"
echo "   Logs: backend.log"

# Wait for backend to start
echo "⏳ Waiting for backend to be ready..."
sleep 5

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "⚠️  Backend may still be starting..."
fi

echo ""
echo "🎨 Starting Frontend Server..."
echo "================================"

# Kill existing frontend process
pkill -f "next dev" 2>/dev/null

# Start frontend in background
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo "✅ Frontend started (PID: $FRONTEND_PID)"
echo "   Logs: frontend.log"

echo ""
echo "=================================================="
echo "✨ AI Vision Platform is now running!"
echo "=================================================="
echo ""
echo "📱 Access from ANY device on your network:"
echo ""
echo "   🌐 Web Interface:  http://$CURRENT_IP:3001"
echo "   🔌 API Backend:    http://$CURRENT_IP:8000"
echo "   ❤️  Health Check:   http://$CURRENT_IP:8000/health"
echo ""
echo "💻 Local access (this machine only):"
echo ""
echo "   🌐 Web Interface:  http://localhost:3001"
echo "   🔌 API Backend:    http://localhost:8000"
echo ""
echo "=================================================="
echo ""
echo "📱 On your phone/tablet:"
echo "   1. Connect to the same WiFi network"
echo "   2. Open browser"
echo "   3. Go to: http://$CURRENT_IP:3001"
echo ""
echo "🛑 To stop servers:"
echo "   pkill -f 'uvicorn main:app'"
echo "   pkill -f 'next dev'"
echo ""
echo "📊 View logs:"
echo "   tail -f backend.log"
echo "   tail -f frontend.log"
echo ""
echo "=================================================="
echo "Press Ctrl+C to stop monitoring (servers will continue running)"
echo "=================================================="

# Monitor logs
tail -f backend.log frontend.log 2>/dev/null

