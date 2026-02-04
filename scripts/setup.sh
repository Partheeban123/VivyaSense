#!/bin/bash

# AI Vision Platform Setup Script
# This script helps you set up the development environment

set -e

echo "🚀 AI Vision Platform Setup"
echo "============================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python 3 found${NC}"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js found${NC}"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}⚠ Docker is not installed (optional)${NC}"
else
    echo -e "${GREEN}✓ Docker found${NC}"
fi

echo ""
echo "📦 Setting up Backend..."
echo "------------------------"

# Backend setup
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo -e "${YELLOW}⚠ Please edit backend/.env with your configuration${NC}"
fi

# Create necessary directories
echo "Creating directories..."
mkdir -p models uploads results logs

echo -e "${GREEN}✓ Backend setup complete${NC}"

cd ..

echo ""
echo "🎨 Setting up Frontend..."
echo "-------------------------"

# Frontend setup
cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local file..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
    echo "NEXT_PUBLIC_WS_URL=ws://localhost:8000" >> .env.local
fi

echo -e "${GREEN}✓ Frontend setup complete${NC}"

cd ..

echo ""
echo "✅ Setup Complete!"
echo "=================="
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Add your YOLO model files (.pt) to backend/models/"
echo "   - backend/models/ppe_detection.pt"
echo "   - backend/models/fall_detection.pt"
echo "   - backend/models/fire_smoke_detection.pt"
echo ""
echo "2. Configure your database in backend/.env"
echo ""
echo "3. Start the services:"
echo ""
echo "   Option A - Using Docker Compose (Recommended):"
echo "   $ docker-compose up -d"
echo ""
echo "   Option B - Manual:"
echo "   Terminal 1 (Backend):"
echo "   $ cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo ""
echo "   Terminal 2 (Frontend):"
echo "   $ cd frontend && npm run dev"
echo ""
echo "4. Access the application:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/api/docs"
echo ""
echo -e "${GREEN}Happy coding! 🎉${NC}"

