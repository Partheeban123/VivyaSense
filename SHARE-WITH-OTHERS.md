# 📱 Share AI Vision Platform with Others

## 🌐 Your Network Access Information

**Your IP Address:** `192.168.0.199`

---

## 🚀 Quick Start for Others

### **Access the Website**
Open this URL in any browser:
```
http://192.168.0.199:3000
```

### **Access the API**
```
http://192.168.0.199:8000
```

### **View API Documentation**
```
http://192.168.0.199:8000/api/docs
```

---

## ✅ Requirements

1. **Same Wi-Fi Network** - All devices must be connected to the same Wi-Fi
2. **Servers Running** - Both frontend and backend must be running on your laptop
3. **Firewall** - Your laptop's firewall must allow connections on ports 3000 and 8000

---

## 🖥️ For You (Host Machine)

### **Start Backend Server**
```bash
cd /Users/partheebandevaraj/ai-vision-platform/backend
source venv/bin/activate
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### **Start Frontend Server**
Open a new terminal:
```bash
cd /Users/partheebandevaraj/ai-vision-platform/frontend
npm run dev
```

You should see:
```
- Local:   http://localhost:3000
- Network: http://0.0.0.0:3000
```

---

## 📱 For Others (Mobile/Tablet/Other Computers)

### **Step 1: Connect to Same Wi-Fi**
Make sure you're on the same Wi-Fi network as the host laptop

### **Step 2: Open Browser**
Use any browser (Chrome, Safari, Firefox, etc.)

### **Step 3: Enter URL**
```
http://192.168.0.199:3000
```

### **Step 4: Start Using!**
You should see the AI Vision Platform homepage with full functionality

---

## 🎯 What Others Can Do

✅ Upload videos for detection
✅ View real-time detection results
✅ Access the dashboard
✅ View analytics
✅ Use all features just like on localhost

---

## 🔧 Troubleshooting

### **"This site can't be reached"**

**1. Check if servers are running on host machine**
- Backend should show: `Uvicorn running on http://0.0.0.0:8000`
- Frontend should show: `ready - started server on 0.0.0.0:3000`

**2. Verify same Wi-Fi network**
- Host and client must be on same network
- Check Wi-Fi name on both devices

**3. Test connection**
From the other device, try pinging:
```bash
ping 192.168.0.199
```

**4. Check firewall on host machine**
- Go to System Preferences → Security & Privacy → Firewall
- Allow incoming connections for Node and Python

### **Website loads but API doesn't work**

Make sure backend is running and accessible:
```
http://192.168.0.199:8000/api/docs
```

If this doesn't load, restart the backend server.

---

## 📊 Testing the Connection

### **From Another Device:**

**1. Test Backend API:**
```
http://192.168.0.199:8000/api/health
```
Should return: `{"status": "healthy"}`

**2. Test Frontend:**
```
http://192.168.0.199:3000
```
Should show the homepage

**3. Test API Docs:**
```
http://192.168.0.199:8000/api/docs
```
Should show Swagger UI

---

## 🔒 Security Note

⚠️ **This is for local network use only!**

- ✅ Safe for home/office Wi-Fi
- ✅ Perfect for demos and testing
- ❌ Do NOT expose to public internet
- ❌ Do NOT use on public Wi-Fi

---

## 💡 Use Cases

### **Team Demo**
Share `http://192.168.0.199:3000` with your team members

### **Mobile Testing**
Test the app on your phone/tablet

### **Multi-Device Testing**
Test across different browsers and devices simultaneously

### **Client Presentation**
Show the app to clients on their devices during meetings

---

## 📞 Quick Reference

**Your URLs:**
- Frontend: http://192.168.0.199:3000
- Backend: http://192.168.0.199:8000
- API Docs: http://192.168.0.199:8000/api/docs

**Share this file with others who need access!**

