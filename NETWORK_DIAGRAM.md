# Network Architecture Diagram

## 🌐 Multi-Device Access Setup

```
┌─────────────────────────────────────────────────────────────────┐
│                        WiFi Network                              │
│                     (192.168.1.x)                                │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
   ┌─────────┐          ┌─────────┐          ┌─────────┐
   │ 📱 Phone│          │ 💻 Laptop│          │ 📱 Tablet│
   │         │          │         │          │         │
   │ Safari  │          │ Chrome  │          │ Browser │
   └─────────┘          └─────────┘          └─────────┘
        │                     │                     │
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Host Computer   │
                    │  192.168.1.23    │
                    └──────────────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
        ┌──────────────┐            ┌──────────────┐
        │   Frontend   │            │   Backend    │
        │   Next.js    │◄──────────►│   FastAPI    │
        │   Port 3001  │   HTTP     │   Port 8000  │
        └──────────────┘            └──────────────┘
                                            │
                                            ▼
                                    ┌──────────────┐
                                    │  AI Models   │
                                    │  - PPE       │
                                    │  - Fall      │
                                    │  - Fire      │
                                    └──────────────┘
```

## 🔌 Port Configuration

| Service  | Port | Protocol | Access                    |
|----------|------|----------|---------------------------|
| Frontend | 3001 | HTTP     | 0.0.0.0 (All interfaces) |
| Backend  | 8000 | HTTP     | 0.0.0.0 (All interfaces) |
| WebSocket| 8000 | WS       | 0.0.0.0 (All interfaces) |

## 📡 Network Flow

### 1. Device Connection
```
Device → WiFi Router → Host Computer (192.168.1.23)
```

### 2. Frontend Request
```
Browser → http://192.168.1.23:3001 → Next.js Server → HTML/CSS/JS
```

### 3. API Request
```
Frontend → http://192.168.1.23:8000/api → FastAPI → AI Model → Response
```

### 4. WebSocket Stream
```
Frontend → ws://192.168.1.23:8000/ws → FastAPI → Real-time Video Stream
```

## 🔒 CORS Configuration

The backend allows requests from:
- `http://localhost:3000`
- `http://localhost:3001`
- `http://127.0.0.1:3000`
- `http://127.0.0.1:3001`
- `http://192.168.1.23:3000`
- `http://192.168.1.23:3001`
- `http://0.0.0.0:3000`
- `http://0.0.0.0:3001`

## 📱 Device Compatibility

| Device Type | Browser | Status |
|-------------|---------|--------|
| iPhone      | Safari  | ✅ Supported |
| Android     | Chrome  | ✅ Supported |
| iPad        | Safari  | ✅ Supported |
| Android Tab | Chrome  | ✅ Supported |
| Windows PC  | Chrome/Edge | ✅ Supported |
| Mac         | Safari/Chrome | ✅ Supported |
| Linux       | Firefox/Chrome | ✅ Supported |

## 🛡️ Security Considerations

### Current Setup (Development)
- ✅ Local network only
- ✅ No internet exposure
- ✅ CORS restricted to known origins
- ⚠️ HTTP (not HTTPS)
- ⚠️ No authentication required

### Production Recommendations
- 🔒 Use HTTPS/SSL certificates
- 🔒 Implement authentication (JWT/OAuth)
- 🔒 Use reverse proxy (nginx/Apache)
- 🔒 Enable rate limiting
- 🔒 Add API key authentication
- 🔒 Use environment-specific secrets
- 🔒 Enable logging and monitoring

## 🔧 Firewall Rules

### macOS
```bash
# Allow Node.js (Frontend)
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/local/bin/node

# Allow Python (Backend)
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/local/bin/python3
```

### Linux (UFW)
```bash
sudo ufw allow 3001/tcp comment "AI Vision Frontend"
sudo ufw allow 8000/tcp comment "AI Vision Backend"
sudo ufw reload
```

### Windows
```powershell
# Run as Administrator
New-NetFirewallRule -DisplayName "AI Vision Frontend" -Direction Inbound -LocalPort 3001 -Protocol TCP -Action Allow
New-NetFirewallRule -DisplayName "AI Vision Backend" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

## 📊 Network Performance

### Recommended Network Specs
- **Minimum:** 10 Mbps WiFi
- **Recommended:** 50+ Mbps WiFi
- **Optimal:** Gigabit Ethernet

### Latency Expectations
- **Same Machine:** < 1ms
- **Same WiFi:** 1-10ms
- **Wired Connection:** < 1ms

### Bandwidth Usage
- **Video Upload:** 1-5 MB/s (depends on video quality)
- **Real-time Stream:** 2-10 MB/s
- **API Requests:** < 100 KB/s
- **WebSocket:** 1-5 MB/s

## 🧪 Testing Checklist

- [ ] Backend health check: `curl http://192.168.1.23:8000/health`
- [ ] Frontend accessible: Open `http://192.168.1.23:3001` in browser
- [ ] API responds: Test detection endpoint
- [ ] WebSocket connects: Test real-time streaming
- [ ] Mobile access: Test from phone/tablet
- [ ] Cross-device: Test from multiple devices simultaneously
- [ ] File upload: Test video upload from mobile
- [ ] Camera access: Test live camera feed from mobile

## 📞 Troubleshooting

### Can't connect from other devices?
1. ✅ Check if both servers are running
2. ✅ Verify IP address is correct
3. ✅ Ensure all devices on same WiFi
4. ✅ Check firewall settings
5. ✅ Restart servers with `./start-network.sh`

### Slow performance?
1. ✅ Check WiFi signal strength
2. ✅ Reduce video quality/resolution
3. ✅ Close other bandwidth-heavy apps
4. ✅ Use wired connection if possible

### Connection drops?
1. ✅ Check WiFi stability
2. ✅ Verify IP hasn't changed
3. ✅ Check server logs for errors
4. ✅ Restart servers

---

**Last Updated:** 2024-01-20
**Network:** 192.168.1.x
**Host IP:** 192.168.1.23

