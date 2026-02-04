# 🔍 Android App Backend Endpoints Investigation

**Date:** 2026-01-23
**Current IP:** 192.168.68.122 (Updated)
**Issue:** Android app trying to connect to non-existent endpoints

---

## ❌ **What's NOT Working:**

### **1. GET /api/alerts - 404 Not Found**
```
Android trying: GET http://192.168.68.122:8000/api/alerts
Backend response: 404 Not Found
```

**Actual endpoint:** `GET /api/dashboard/alerts`

### **2. WebSocket /ws/alerts - 403 Forbidden**
```
Android trying: ws://192.168.68.122:8000/ws/alerts
Backend response: 403 Forbidden (Expected HTTP 101)
```

**Actual endpoint:** `ws://192.168.68.122:8000/ws/stream/{stream_id}`

---

## ✅ **Correct Backend Endpoints:**

### **1. Alerts Endpoint**
```
❌ Wrong: GET /api/alerts
✅ Correct: GET /api/dashboard/alerts
```

**Location:** `backend/api/dashboard.py` (line 70)

**Response:**
```json
{
  "alerts": [],
  "total": 0
}
```

### **2. WebSocket Endpoint**
```
❌ Wrong: ws://192.168.68.122:8000/ws/alerts
✅ Correct: ws://192.168.68.122:8000/ws/stream/{stream_id}
```

**Location:** `backend/main.py` (line 105)

**How it works:**
1. Connect to: `ws://192.168.68.122:8000/ws/stream/camera_123`
2. Send start command:
```json
{
  "action": "start",
  "stream_url": "rtsp://camera_url",
  "detection_types": ["fall", "ppe", "fire", "smoke"],
  "confidence": 0.5
}
```
3. Receive frames with detections:
```json
{
  "type": "frame",
  "stream_id": "camera_123",
  "frame": "base64_encoded_jpeg",
  "detections": [
    {
      "type": "fall",
      "confidence": 0.95,
      "bbox": [x, y, width, height],
      "label": "Fall Detected"
    }
  ],
  "frame_number": 123
}
```

---

## 📋 **All Available Backend Endpoints:**

### **Authentication** (`/api/auth`)
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get token
- `GET /api/auth/me` - Get current user info

### **Detection** (`/api/detection`)
- `POST /api/detection/image` - Detect objects in image
- `POST /api/detection/fall` - Fall detection
- `POST /api/detection/ppe` - PPE detection
- `POST /api/detection/fire-smoke` - Fire/smoke detection
- `GET /api/detection/models` - List available models
- `GET /api/detection/classes/{model_name}` - Get model classes

### **Video** (`/api/video`)
- `POST /api/video/upload` - Upload and process video
- `GET /api/video/status/{job_id}` - Get processing status
- `GET /api/video/result/{job_id}` - Get detection results

### **Camera** (`/api/camera`) ⚠️ **NOTE: No 's' at the end!**
- ✅ `POST /api/camera/` - Create camera
- ✅ `GET /api/camera/` - List all cameras (**NOT /api/cameras**)
- `GET /api/camera/{id}` - Get camera details
- `PUT /api/camera/{id}` - Update camera
- `DELETE /api/camera/{id}` - Delete camera
- `POST /api/camera/{id}/start` - Start camera stream
- `POST /api/camera/{id}/stop` - Stop camera stream

### **Dashboard** (`/api/dashboard`)
- `GET /api/dashboard/stats` - Get dashboard statistics
- `GET /api/dashboard/trends` - Get detection trends
- `GET /api/dashboard/recent-detections` - Get recent detections
- ✅ `GET /api/dashboard/alerts` - **Get alerts (THIS IS THE ONE!)**

### **Contact** (`/api`)
- `POST /api/contact` - Submit contact form
- `GET /api/contact/stats` - Get contact statistics

### **WebSocket**
- ✅ `WS /ws/stream/{stream_id}` - **Real-time video streaming with detections**

### **Health**
- `GET /health` - Health check
- `GET /` - Root endpoint

---

## 🔧 **What Needs to Change in Android App:**

### **1. Update API Service Interface**

```kotlin
// In data/api/ApiService.kt
interface ApiService {
    // ❌ WRONG:
    // @GET("api/alerts")
    
    // ✅ CORRECT:
    @GET("api/dashboard/alerts")
    suspend fun getAlerts(@Query("limit") limit: Int = 10): Response<AlertsResponse>
    
    @GET("api/dashboard/stats")
    suspend fun getDashboardStats(): Response<DashboardStats>
    
    @GET("api/dashboard/recent-detections")
    suspend fun getRecentDetections(@Query("limit") limit: Int = 10): Response<DetectionsResponse>
}
```

### **2. Update WebSocket Client**

```kotlin
// In data/websocket/WebSocketClient.kt
object Constants {
    // ❌ WRONG:
    // const val WS_BASE_URL = "ws://192.168.68.122:8000/ws/alerts"

    // ✅ CORRECT:
    const val WS_BASE_URL = "ws://192.168.68.122:8000/ws/stream/"
}

class WebSocketClient {
    fun connect(streamId: String) {
        val url = "${Constants.WS_BASE_URL}$streamId"  // ws://192.168.68.122:8000/ws/stream/camera_123
        
        val request = Request.Builder()
            .url(url)
            .build()
        
        webSocket = client.newWebSocket(request, webSocketListener)
    }
    
    fun startStream(streamUrl: String, detectionTypes: List<String>) {
        val message = JSONObject().apply {
            put("action", "start")
            put("stream_url", streamUrl)
            put("detection_types", JSONArray(detectionTypes))
            put("confidence", 0.5)
        }
        webSocket?.send(message.toString())
    }
}
```

---

## 📱 **Updated Android App Prompt:**

Copy this and use in Android Studio with Augment:

```
Hi! I need to fix critical issues in my Android app.

CRITICAL ISSUES:
1. Wrong IP address: Using old IP instead of 192.168.68.122
2. Wrong camera endpoint: Using /api/cameras instead of /api/camera (no 's'!)
3. Wrong alerts endpoint: Using /api/alerts instead of /api/dashboard/alerts
4. Wrong WebSocket: Using /ws/alerts instead of /ws/stream/{stream_id}

CORRECT BACKEND ENDPOINTS (IP: 192.168.68.122):
1. Cameras: GET http://192.168.68.122:8000/api/camera (singular, no 's'!)
2. Alerts: GET http://192.168.68.122:8000/api/dashboard/alerts
3. WebSocket: ws://192.168.68.122:8000/ws/stream/{stream_id}

PLEASE UPDATE:

1. utils/Constants.kt:
   - Change BASE_URL to "http://192.168.68.122:8000/"
   - Change WS_BASE_URL to "ws://192.168.68.122:8000/ws/stream/"

2. data/api/ApiService.kt - FIX THESE ENDPOINTS:
   ❌ WRONG: @GET("api/cameras")
   ✅ CORRECT: @GET("api/camera")

   ❌ WRONG: @GET("api/alerts")
   ✅ CORRECT: @GET("api/dashboard/alerts")

   Also add:
   - @GET("api/dashboard/stats")
   - @GET("api/dashboard/recent-detections")
   - @POST("api/camera")
   - @GET("api/camera/{id}")

3. data/websocket/WebSocketClient.kt:
   - Update connect() to use: ws://192.168.68.122:8000/ws/stream/{streamId}
   - Update startStream() to send proper JSON:
     {
       "action": "start",
       "stream_url": "rtsp://...",
       "detection_types": ["fall", "ppe", "fire", "smoke"],
       "confidence": 0.5
     }

4. WebSocket stability:
   - Add reconnection logic if connection drops
   - Add heartbeat/ping to keep connection alive

IMPORTANT: The camera endpoint is /api/camera (singular), NOT /api/cameras (plural)!

Please make these changes!
```

---

## ✅ **Next Steps:**

1. **Copy the Android app prompt above** and paste it into Augment in Android Studio
2. **Augment will fix** all the endpoint URLs
3. **Test the app** again
4. **It should work!** ✅

---

**🎉 Once fixed, your Android app will connect to the correct endpoints!**

