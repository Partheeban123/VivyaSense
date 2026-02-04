# 📱 Android App - Quick Start Guide

**Get your Android app running in 30 minutes!**

---

## ⚡ Super Quick Setup

### **1. Install Android Studio (10 min)**
```bash
# Download from:
https://developer.android.com/studio

# Install and open Android Studio
# Install Android SDK when prompted
```

---

### **2. Create Project (2 min)**
1. Open Android Studio
2. Click **"New Project"**
3. Select **"Empty Activity"** (Compose)
4. Name: **AI Vision Alerts**
5. Package: **com.yourdomain.aivision**
6. Language: **Kotlin**
7. Minimum SDK: **API 24**
8. Click **"Finish"**

---

### **3. Add Dependencies (3 min)**

Open `build.gradle.kts` (app level) and add:

```kotlin
dependencies {
    // ... existing dependencies ...
    
    // Networking
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
    implementation("com.squareup.retrofit2:converter-gson:2.9.0")
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
    
    // Firebase
    implementation(platform("com.google.firebase:firebase-bom:32.7.0"))
    implementation("com.google.firebase:firebase-messaging")
    
    // Coroutines
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
    
    // ViewModel
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
}
```

Click **"Sync Now"**

---

### **4. Update Backend URL (1 min)**

Create `utils/Constants.kt`:

```kotlin
package com.yourdomain.aivision.utils

object Constants {
    const val BASE_URL = "http://192.168.68.105:8000/"
    const val WS_URL = "ws://192.168.68.105:8000/ws/alerts"
}
```

**⚠️ Replace `192.168.68.105` with your backend IP!**

---

### **5. Add Internet Permission (1 min)**

Open `AndroidManifest.xml` and add:

```xml
<manifest ...>
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
    
    <application
        ...
        android:usesCleartextTraffic="true">
        ...
    </application>
</manifest>
```

---

### **6. Copy Code Files (5 min)**

Copy these files from `ANDROID_APP_IMPLEMENTATION.md`:

1. **data/model/Detection.kt** - Data models
2. **data/api/ApiService.kt** - API interface
3. **data/api/RetrofitClient.kt** - Network client
4. **data/api/WebSocketClient.kt** - WebSocket client
5. **viewmodel/AlertViewModel.kt** - Business logic
6. **ui/screens/AlertListScreen.kt** - UI screen
7. **service/MyFirebaseMessagingService.kt** - Notifications

---

### **7. Update MainActivity (2 min)**

Replace `MainActivity.kt` content:

```kotlin
package com.yourdomain.aivision

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import com.yourdomain.aivision.ui.screens.AlertListScreen
import com.yourdomain.aivision.ui.theme.AIVisionAlertsTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            AIVisionAlertsTheme {
                Surface(color = MaterialTheme.colorScheme.background) {
                    AlertListScreen()
                }
            }
        }
    }
}
```

---

### **8. Build & Run (5 min)**

1. **Connect Android device** via USB (enable USB debugging)
   - OR start **Android Emulator** (Tools → Device Manager)

2. **Click Run** (green play button ▶️)

3. **Wait for build** (~2-3 minutes first time)

4. **App launches!** 🎉

---

## 🧪 Test It!

### **1. Start Backend:**
```bash
cd backend
source venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### **2. Connect Camera:**
- Open web app: `http://192.168.68.105:3000/camera`
- Connect RTSP camera
- Enable detection (Fall, PPE, Fire, or Smoke)

### **3. Trigger Detection:**
- Walk in front of camera
- Remove helmet (PPE)
- Show fire/smoke

### **4. Check Android App:**
- Should see real-time alerts! ✅
- Notification should appear! 🔔

---

## 🎯 What You Get

✅ **Real-time alerts** from all cameras  
✅ **WebSocket connection** for instant updates  
✅ **Beautiful Material Design 3 UI**  
✅ **Push notifications** (with Firebase)  
✅ **Alert history** with timestamps  
✅ **Connection status** indicator  

---

## 🐛 Troubleshooting

### **"Cannot connect to backend"**
- ✅ Check backend is running
- ✅ Check IP address in `Constants.kt`
- ✅ Make sure phone/emulator on same WiFi
- ✅ Check `usesCleartextTraffic="true"` in manifest

### **"WebSocket not connecting"**
- ✅ Check WS_URL in `Constants.kt`
- ✅ Check backend logs for WebSocket connection
- ✅ Try restarting app

### **"No notifications"**
- ✅ Enable notifications in phone settings
- ✅ Check Firebase setup
- ✅ Check notification permission granted

### **"Build errors"**
- ✅ Click "Sync Project with Gradle Files"
- ✅ Clean project: Build → Clean Project
- ✅ Rebuild: Build → Rebuild Project

---

## 📚 Full Documentation

For complete implementation details, see:
- **ANDROID_APP_GUIDE.md** - Overview & architecture
- **ANDROID_APP_IMPLEMENTATION.md** - Complete code

---

## 🚀 Next Features to Add

1. **Camera List** - View all cameras
2. **Live Feed** - Watch camera stream
3. **Alert Filtering** - Filter by type/camera
4. **Settings** - Configure notifications
5. **Dark Mode** - Theme support
6. **Alert Sounds** - Custom sounds
7. **Statistics** - Alert analytics

---

## 💡 Tips

- **Use real device** for best testing (faster than emulator)
- **Enable USB debugging** in phone developer options
- **Keep backend running** while testing
- **Check Logcat** for debugging (View → Tool Windows → Logcat)
- **Hot reload** works with Compose (Ctrl+S to update UI)

---

## 🎉 Success!

You now have a working Android app that receives real-time AI detection alerts!

**Need help?** Check the full implementation guide or ask me! 🚀

