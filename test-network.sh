#!/bin/bash

# Network Configuration Test Script
# Tests if the AI Vision Platform is properly configured for network access

echo "🧪 AI Vision Platform - Network Configuration Test"
echo "===================================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get current IP
CURRENT_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)

if [ -z "$CURRENT_IP" ]; then
    echo -e "${RED}❌ Error: Could not detect IP address${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Detected IP: $CURRENT_IP${NC}"
echo ""

# Test 1: Check if backend is running
echo "Test 1: Backend Server"
echo "----------------------"
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend is running on localhost:8000${NC}"
    
    # Test network access
    if curl -s http://$CURRENT_IP:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Backend accessible via network ($CURRENT_IP:8000)${NC}"
    else
        echo -e "${RED}❌ Backend NOT accessible via network${NC}"
        echo -e "${YELLOW}   Check firewall settings${NC}"
    fi
else
    echo -e "${RED}❌ Backend is NOT running${NC}"
    echo -e "${YELLOW}   Start with: cd backend && source venv/bin/activate && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000${NC}"
fi
echo ""

# Test 2: Check if frontend is running
echo "Test 2: Frontend Server"
echo "----------------------"
if curl -s http://localhost:3001 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend is running on localhost:3001${NC}"
    
    # Test network access
    if curl -s http://$CURRENT_IP:3001 > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Frontend accessible via network ($CURRENT_IP:3001)${NC}"
    else
        echo -e "${RED}❌ Frontend NOT accessible via network${NC}"
        echo -e "${YELLOW}   Check firewall settings${NC}"
    fi
else
    echo -e "${RED}❌ Frontend is NOT running${NC}"
    echo -e "${YELLOW}   Start with: cd frontend && npm run dev${NC}"
fi
echo ""

# Test 3: Check .env.local configuration
echo "Test 3: Frontend Configuration"
echo "------------------------------"
if [ -f "frontend/.env.local" ]; then
    if grep -q "$CURRENT_IP" "frontend/.env.local"; then
        echo -e "${GREEN}✅ Frontend .env.local has correct IP${NC}"
    else
        echo -e "${YELLOW}⚠️  Frontend .env.local may have outdated IP${NC}"
        echo -e "${YELLOW}   Run: ./start-network.sh to update${NC}"
    fi
else
    echo -e "${RED}❌ frontend/.env.local not found${NC}"
fi
echo ""

# Test 4: Check backend .env configuration
echo "Test 4: Backend Configuration"
echo "-----------------------------"
if [ -f "backend/.env" ]; then
    if grep -q "HOST=0.0.0.0" "backend/.env"; then
        echo -e "${GREEN}✅ Backend configured for network access${NC}"
    else
        echo -e "${YELLOW}⚠️  Backend may not be configured for network access${NC}"
        echo -e "${YELLOW}   Add: HOST=0.0.0.0 to backend/.env${NC}"
    fi
    
    if grep -q "CORS_ORIGINS" "backend/.env"; then
        echo -e "${GREEN}✅ CORS configuration found${NC}"
    else
        echo -e "${YELLOW}⚠️  CORS configuration not found${NC}"
    fi
else
    echo -e "${RED}❌ backend/.env not found${NC}"
fi
echo ""

# Test 5: Port availability
echo "Test 5: Port Availability"
echo "------------------------"
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Port 8000 is in use (Backend)${NC}"
else
    echo -e "${YELLOW}⚠️  Port 8000 is not in use${NC}"
fi

if lsof -Pi :3001 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Port 3001 is in use (Frontend)${NC}"
else
    echo -e "${YELLOW}⚠️  Port 3001 is not in use${NC}"
fi
echo ""

# Test 6: Network connectivity
echo "Test 6: Network Connectivity"
echo "---------------------------"
if ping -c 1 $CURRENT_IP > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Can ping own IP address${NC}"
else
    echo -e "${RED}❌ Cannot ping own IP address${NC}"
fi
echo ""

# Summary
echo "===================================================="
echo "📊 Test Summary"
echo "===================================================="
echo ""
echo "Access URLs:"
echo "------------"
echo -e "🌐 Frontend (Network): ${GREEN}http://$CURRENT_IP:3001${NC}"
echo -e "🔌 Backend (Network):  ${GREEN}http://$CURRENT_IP:8000${NC}"
echo -e "❤️  Health Check:       ${GREEN}http://$CURRENT_IP:8000/health${NC}"
echo ""
echo -e "💻 Frontend (Local):   ${GREEN}http://localhost:3001${NC}"
echo -e "🔌 Backend (Local):    ${GREEN}http://localhost:8000${NC}"
echo ""
echo "===================================================="
echo ""
echo "📱 To access from other devices:"
echo "   1. Connect to the same WiFi network"
echo "   2. Open browser"
echo "   3. Go to: http://$CURRENT_IP:3001"
echo ""
echo "🔧 To start servers:"
echo "   ./start-network.sh"
echo ""
echo "===================================================="

