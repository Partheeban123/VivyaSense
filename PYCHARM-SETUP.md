# 🐍 PyCharm IDE Setup Guide

## ✅ Yes, You Have `main.py`!

Your backend has a `main.py` file at:
```
/Users/partheebandevaraj/ai-vision-platform/backend/main.py
```

---

## 🚀 How to Run Backend in PyCharm

### **Method 1: Direct Run (Easiest)**

1. **Open PyCharm**
2. **Open the backend folder:**
   - File → Open → Select `/Users/partheebandevaraj/ai-vision-platform/backend`

3. **Configure Python Interpreter:**
   - PyCharm → Preferences → Project → Python Interpreter
   - Click the gear icon → Add
   - Select "Existing Environment"
   - Choose: `/Users/partheebandevaraj/ai-vision-platform/backend/venv/bin/python`
   - Click OK

4. **Run main.py:**
   - Open `main.py` in the editor
   - Right-click anywhere in the file
   - Select "Run 'main'"
   - Or press `Ctrl + Shift + R` (Mac: `Cmd + Shift + R`)

5. **Server should start:**
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

---

### **Method 2: Create Run Configuration**

1. **Open Run/Debug Configurations:**
   - Run → Edit Configurations...

2. **Add New Python Configuration:**
   - Click `+` → Python

3. **Configure:**
   - **Name:** `Backend Server`
   - **Script path:** `/Users/partheebandevaraj/ai-vision-platform/backend/main.py`
   - **Working directory:** `/Users/partheebandevaraj/ai-vision-platform/backend`
   - **Python interpreter:** Select the venv interpreter
   - **Environment variables:** (Optional)
     ```
     PYTHONUNBUFFERED=1
     ```

4. **Apply and Run:**
   - Click Apply → OK
   - Click the green play button ▶️

---

### **Method 3: Using Terminal in PyCharm**

1. **Open Terminal in PyCharm:**
   - View → Tool Windows → Terminal
   - Or press `Alt + F12` (Mac: `Option + F12`)

2. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Run the server:**
   ```bash
   python main.py
   ```

---

## 📁 Project Structure in PyCharm

When you open the backend folder, you'll see:

```
backend/
├── main.py              ← Main entry point (THIS IS WHAT YOU RUN!)
├── requirements.txt     ← Dependencies
├── venv/               ← Virtual environment
├── api/                ← API endpoints
│   ├── auth.py
│   ├── detection.py
│   ├── video.py
│   ├── camera.py
│   └── dashboard.py
├── core/               ← Core configuration
│   ├── config.py
│   └── logger.py
├── database/           ← Database models
│   ├── database.py
│   └── models.py
├── services/           ← Business logic
│   ├── detection_service.py
│   └── video_service.py
└── websocket/          ← WebSocket handlers
    └── stream_handler.py
```

---

## 🔧 PyCharm Configuration Tips

### **1. Mark Directories as Sources Root**
Right-click on `backend` folder → Mark Directory as → Sources Root

### **2. Enable Auto-Import**
- Preferences → Editor → General → Auto Import
- Check "Show import popup"
- Check "Optimize imports on the fly"

### **3. Configure Code Style**
- Preferences → Editor → Code Style → Python
- Set to PEP 8

### **4. Enable Type Checking**
- Preferences → Editor → Inspections → Python
- Enable "Type checker"

---

## 🐛 Debugging in PyCharm

### **Set Breakpoints:**
1. Click in the left margin next to line numbers
2. Red dot appears = breakpoint set

### **Debug Mode:**
1. Click the bug icon 🐛 next to the run button
2. Or press `Shift + F9` (Mac: `Cmd + Shift + D`)
3. Server starts in debug mode
4. Execution pauses at breakpoints

### **Debug Console:**
- Evaluate expressions
- Inspect variables
- Step through code

---

## 📦 Installing Dependencies in PyCharm

### **Option 1: Using PyCharm UI**
1. Open `requirements.txt`
2. PyCharm shows a banner: "Package requirements are not satisfied"
3. Click "Install requirements"

### **Option 2: Using Terminal**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🌐 Running with Network Access

The `main.py` is already configured to run on `0.0.0.0:8000`, which means:
- ✅ Accessible from localhost
- ✅ Accessible from network (192.168.0.199:8000)

No changes needed!

---

## ⚡ Quick Start Checklist

- [ ] Open backend folder in PyCharm
- [ ] Configure Python interpreter (venv)
- [ ] Install dependencies from requirements.txt
- [ ] Open main.py
- [ ] Click Run ▶️
- [ ] Server starts on http://0.0.0.0:8000
- [ ] Access at http://localhost:8000 or http://192.168.0.199:8000

---

## 🎯 What Happens When You Run main.py

1. **FastAPI app initializes**
2. **Database connection established**
3. **API routes registered:**
   - `/api/auth` - Authentication
   - `/api/detection` - Detection endpoints
   - `/api/video` - Video processing
   - `/api/camera` - Camera management
   - `/api/dashboard` - Dashboard data

4. **Uvicorn server starts:**
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000
   INFO:     Application startup complete
   ```

5. **Access API docs:**
   - http://localhost:8000/api/docs
   - http://192.168.0.199:8000/api/docs

---

## 🔍 Verify It's Working

### **In PyCharm Console:**
You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup
INFO:     Application startup complete
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### **In Browser:**
Open: http://localhost:8000
Should return:
```json
{
  "message": "Welcome to AI Vision Platform",
  "version": "1.0.0",
  "docs": "/api/docs"
}
```

---

## 🆘 Troubleshooting

### **"No module named 'fastapi'"**
**Solution:** Install dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### **"Port 8000 is already in use"**
**Solution:** Kill existing process
```bash
lsof -ti:8000 | xargs kill -9
```

### **"Cannot find main.py"**
**Solution:** Make sure you opened the `backend` folder, not the root `ai-vision-platform` folder

### **Virtual environment not activated**
**Solution:** In PyCharm terminal:
```bash
source venv/bin/activate
```

---

## 💡 Pro Tips

### **1. Use PyCharm's HTTP Client**
- Tools → HTTP Client → Test RESTful Web Service
- Test your API endpoints directly in PyCharm

### **2. Database Tool Window**
- View → Tool Windows → Database
- Connect to your SQLite database
- Browse tables and data

### **3. Git Integration**
- VCS → Enable Version Control Integration
- Commit, push, pull directly from PyCharm

### **4. TODO Comments**
- Add `# TODO: ` comments in code
- View → Tool Windows → TODO
- See all TODOs in one place

---

## 🎉 You're All Set!

Your backend is ready to run in PyCharm! Just:
1. Open `main.py`
2. Click Run ▶️
3. Start coding! 🚀

