# 🌐 Network Access Guide

## How to Access from Other Devices

Your AI Vision Platform is now configured to be accessible from other devices on the same network!

---

## 📋 Quick Setup

### 1. Find Your IP Address

**On macOS:**
```bash
ipconfig getifaddr en0
```

**Or manually:**
- Open **System Preferences** → **Network**
- Select your active connection (Wi-Fi or Ethernet)
- Look for **IP Address** (e.g., `192.168.1.100`)

---

### 2. Start Both Servers

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

---

### 3. Access from Other Devices

Replace `YOUR_IP` with your actual IP address (e.g., `192.168.1.100`)

**Frontend (Website):**
```
http://YOUR_IP:3000
```

**Backend API:**
```
http://YOUR_IP:8000
```

**API Documentation:**
```
http://YOUR_IP:8000/api/docs
```

---

## 📱 Example

If your IP is `192.168.1.100`:

- **Website:** `http://192.168.1.100:3000`
- **API:** `http://192.168.1.100:8000`
- **Docs:** `http://192.168.1.100:8000/api/docs`

---

## ✅ What's Been Configured

### Frontend (Next.js)
- ✅ Server now listens on `0.0.0.0` (all network interfaces)
- ✅ Accessible from any device on the network

### Backend (FastAPI)
- ✅ Server already configured to listen on `0.0.0.0`
- ✅ CORS configured to allow all HTTP origins
- ✅ WebSocket connections enabled for network access

---

## 🔒 Security Notes

### ⚠️ Important
This configuration is for **local network development only**. 

**Do NOT expose this to the public internet without:**
1. Proper authentication
2. HTTPS/SSL certificates
3. Rate limiting
4. Firewall rules
5. Security hardening

---

## 🛠️ Troubleshooting

### Can't Connect from Other Devices?

**1. Check Firewall**
```bash
# macOS - Allow ports 3000 and 8000
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/local/bin/node
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/bin/python3
```

**2. Verify Servers are Running**
- Check Terminal 1: Backend should show "Uvicorn running on http://0.0.0.0:8000"
- Check Terminal 2: Frontend should show "ready - started server on 0.0.0.0:3000"

**3. Confirm Same Network**
- All devices must be on the same Wi-Fi network
- Check IP range (e.g., all should be `192.168.1.x`)

**4. Test Connection**
From another device, try:
```bash
ping YOUR_IP
```

---

## 📞 Quick Reference Script

Run this to see your network info:
```bash
./get-network-info.sh
```

---

## 🎯 Common Use Cases

### Mobile Testing
Access the website from your phone/tablet on the same Wi-Fi

### Team Demo
Share your IP with team members for live demos

### Multi-Device Testing
Test the application across different devices simultaneously

---

## 🔄 Reverting to Localhost Only

If you want to restrict access to localhost only:

**Frontend (`package.json`):**
```json
"dev": "next dev"
```

**Backend (`core/config.py`):**
```python
HOST: str = "127.0.0.1"
```

**Backend (`main.py`):**
```python
allow_origins=settings.CORS_ORIGINS,
```

---

## 📚 Additional Resources

- [Next.js Network Access](https://nextjs.org/docs/api-reference/cli#development)
- [FastAPI CORS](https://fastapi.tiangolo.com/tutorial/cors/)
- [Uvicorn Deployment](https://www.uvicorn.org/deployment/)

