# 🚀 Quick Start - Network Access

## One-Command Startup

```bash
./start-network.sh
```

This will:
- ✅ Auto-detect your IP address
- ✅ Update configuration files
- ✅ Start backend server
- ✅ Start frontend server
- ✅ Show access URLs

---

## Manual Startup

### Terminal 1 - Backend:
```bash
cd backend
source venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

---

## 📱 Access URLs

**Your IP:** `192.168.1.23`

### From Any Device on Same WiFi:
- **Web App:** http://192.168.1.23:3001
- **API:** http://192.168.1.23:8000

### From This Computer:
- **Web App:** http://localhost:3001
- **API:** http://localhost:8000

---

## 🛑 Stop Servers

```bash
pkill -f "uvicorn main:app"
pkill -f "next dev"
```

---

## 📱 Mobile Access

1. Connect phone/tablet to same WiFi
2. Open browser
3. Go to: **http://192.168.1.23:3001**
4. Add to home screen for app-like experience!

---

## 🔍 Check Status

```bash
# Backend health
curl http://192.168.1.23:8000/health

# Frontend
curl http://192.168.1.23:3001
```

---

## 💡 Tips

- **IP Changed?** Run `./start-network.sh` again
- **Can't Connect?** Check firewall settings
- **Slow Loading?** Ensure good WiFi signal
- **Need Help?** See `NETWORK_SETUP.md` for detailed guide

---

**Last Updated:** 2024-01-20

