# Network Configuration Guide

## 🌐 Access from Multiple Devices

This guide will help you access the AI Vision Platform from any device on your local network (phones, tablets, other computers).

---

## 📱 Current Configuration

**Your Local IP Address:** `192.168.1.23`

### Access URLs:

- **Frontend (Web Interface):** `http://192.168.1.23:3001`
- **Backend API:** `http://192.168.1.23:8000`
- **API Health Check:** `http://192.168.1.23:8000/health`

---

## 🚀 Quick Start

### 1. Start the Backend Server
```bash
cd backend
source venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start the Frontend Server
```bash
cd frontend
npm run dev
```

### 3. Access from Other Devices

On any device connected to the same WiFi network:

- **Open browser and go to:** `http://192.168.1.23:3001`

---

## 📲 Tested Devices

✅ **Desktop/Laptop** - Same machine (localhost)
✅ **Other Computers** - On same network
✅ **Smartphones** - iOS/Android on same WiFi
✅ **Tablets** - iPad/Android tablets on same WiFi

---

## 🔧 Configuration Files

### Backend Configuration
**File:** `backend/.env`
```env
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,http://192.168.1.23:3000,http://192.168.1.23:3001
```

### Frontend Configuration
**File:** `frontend/.env.local`
```env
NEXT_PUBLIC_API_URL=http://192.168.1.23:8000
NEXT_PUBLIC_WS_URL=ws://192.168.1.23:8000
```

---

## 🔍 Find Your IP Address

If your IP address changes (e.g., after router restart):

### macOS/Linux:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}'
```

### Windows:
```cmd
ipconfig | findstr IPv4
```

### Update Configuration:
1. Update `backend/.env` - Add new IP to `CORS_ORIGINS`
2. Update `frontend/.env.local` - Change `NEXT_PUBLIC_API_URL` and `NEXT_PUBLIC_WS_URL`
3. Restart both servers

---

## 🛡️ Firewall Configuration

### macOS:
```bash
# Allow incoming connections on ports 3001 and 8000
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/local/bin/node
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/local/bin/python3
```

### Windows:
1. Open Windows Defender Firewall
2. Click "Advanced settings"
3. Create new Inbound Rules for ports 3001 and 8000

### Linux (Ubuntu):
```bash
sudo ufw allow 3001/tcp
sudo ufw allow 8000/tcp
sudo ufw reload
```

---

## 🧪 Testing Connection

### Test Backend API:
```bash
# From any device on the network
curl http://192.168.1.23:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-20T..."
}
```

### Test Frontend:
Open browser on any device and navigate to:
```
http://192.168.1.23:3001
```

---

## 📱 Mobile Access Tips

### For Best Mobile Experience:

1. **Add to Home Screen** (iOS/Android)
   - Open `http://192.168.1.23:3001` in Safari/Chrome
   - Tap Share → Add to Home Screen
   - Now you have an app-like experience!

2. **Landscape Mode**
   - Rotate device for better dashboard viewing
   - Full-screen mode recommended

3. **Camera Upload**
   - Mobile browsers support direct camera access
   - Use "Take Photo" option in detection page

---

## 🔒 Security Notes

⚠️ **Important:**
- This configuration is for **LOCAL NETWORK ONLY**
- Do NOT expose these ports to the internet without proper security
- For production deployment, use:
  - HTTPS/SSL certificates
  - Proper authentication
  - Reverse proxy (nginx/Apache)
  - Environment-specific secrets

---

## 🐛 Troubleshooting

### Can't connect from other devices?

1. **Check if servers are running:**
   ```bash
   # Check backend
   curl http://localhost:8000/health
   
   # Check frontend
   curl http://localhost:3001
   ```

2. **Verify IP address:**
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```

3. **Check firewall settings:**
   - Ensure ports 3001 and 8000 are not blocked

4. **Verify same network:**
   - All devices must be on the same WiFi network
   - Check WiFi name on all devices

5. **Restart servers:**
   ```bash
   # Kill existing processes
   pkill -f "uvicorn main:app"
   pkill -f "next dev"
   
   # Restart backend
   cd backend && source venv/bin/activate && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   
   # Restart frontend (in new terminal)
   cd frontend && npm run dev
   ```

---

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all configuration files
3. Check server logs for errors
4. Ensure all dependencies are installed

---

**Last Updated:** 2024-01-20
**Current IP:** 192.168.1.23

