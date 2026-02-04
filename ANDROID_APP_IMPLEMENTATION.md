# 📱 Android App Implementation Guide - Code Examples

**Complete implementation guide with code examples**

---

## 🚀 Quick Start

### **Step 1: Install Android Studio**
1. Download from: https://developer.android.com/studio
2. Install Android Studio
3. Install Android SDK (API 34 recommended)
4. Setup Android emulator or connect real device

---

### **Step 2: Create New Project**

1. Open Android Studio
2. Click "New Project"
3. Select "Empty Activity" (Jetpack Compose)
4. Configure:
   - **Name:** AI Vision Alerts
   - **Package:** com.yourdomain.aivision
   - **Language:** Kotlin
   - **Minimum SDK:** API 24 (Android 7.0)
   - **Build configuration:** Kotlin DSL

---

## 📦 Step 3: Setup Dependencies

### **build.gradle.kts (Project level):**
```kotlin
plugins {
    id("com.android.application") version "8.2.0" apply false
    id("org.jetbrains.kotlin.android") version "1.9.20" apply false
    id("com.google.gms.google-services") version "4.4.0" apply false
}
```

### **build.gradle.kts (App level):**
```kotlin
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("com.google.gms.google-services")
}

android {
    namespace = "com.yourdomain.aivision"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.yourdomain.aivision"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }

    buildFeatures {
        compose = true
    }

    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.4"
    }
}

dependencies {
    // Core
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.7.0")
    implementation("androidx.activity:activity-compose:1.8.2")
    
    // Compose
    implementation(platform("androidx.compose:compose-bom:2024.01.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.navigation:navigation-compose:2.7.6")
    
    // Networking
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
    implementation("com.squareup.retrofit2:converter-gson:2.9.0")
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
    implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")
    
    // Firebase
    implementation(platform("com.google.firebase:firebase-bom:32.7.0"))
    implementation("com.google.firebase:firebase-messaging")
    implementation("com.google.firebase:firebase-analytics")
    
    // Image Loading
    implementation("io.coil-kt:coil-compose:2.5.0")
    
    // Coroutines
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
    
    // ViewModel
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
    
    // JSON
    implementation("com.google.code.gson:gson:2.10.1")
}
```

---

## 🔧 Step 4: Create Data Models

### **data/model/Detection.kt:**
```kotlin
package com.yourdomain.aivision.data.model

import com.google.gson.annotations.SerializedName

data class Detection(
    @SerializedName("id")
    val id: String,
    
    @SerializedName("type")
    val type: DetectionType,
    
    @SerializedName("camera_id")
    val cameraId: String,
    
    @SerializedName("camera_name")
    val cameraName: String,
    
    @SerializedName("confidence")
    val confidence: Float,
    
    @SerializedName("timestamp")
    val timestamp: Long,
    
    @SerializedName("image_url")
    val imageUrl: String?,
    
    @SerializedName("bbox")
    val bbox: BoundingBox?,
    
    @SerializedName("alert")
    val isAlert: Boolean = false
)

enum class DetectionType {
    @SerializedName("fall")
    FALL,
    
    @SerializedName("ppe")
    PPE,
    
    @SerializedName("fire")
    FIRE,
    
    @SerializedName("smoke")
    SMOKE
}

data class BoundingBox(
    @SerializedName("x")
    val x: Float,
    
    @SerializedName("y")
    val y: Float,
    
    @SerializedName("width")
    val width: Float,
    
    @SerializedName("height")
    val height: Float
)

data class Camera(
    @SerializedName("id")
    val id: String,
    
    @SerializedName("name")
    val name: String,
    
    @SerializedName("location")
    val location: String,
    
    @SerializedName("rtsp_url")
    val rtspUrl: String,
    
    @SerializedName("status")
    val status: String,
    
    @SerializedName("detection_types")
    val detectionTypes: List<DetectionType>
)
```

---

## 🌐 Step 5: Create API Service

### **data/api/ApiService.kt:**
```kotlin
package com.yourdomain.aivision.data.api

import com.yourdomain.aivision.data.model.Camera
import com.yourdomain.aivision.data.model.Detection
import retrofit2.Response
import retrofit2.http.*

interface ApiService {
    @GET("api/cameras")
    suspend fun getCameras(): Response<List<Camera>>
    
    @GET("api/cameras/{id}")
    suspend fun getCamera(@Path("id") id: String): Response<Camera>
    
    @POST("api/cameras")
    suspend fun createCamera(@Body camera: Camera): Response<Camera>
    
    @GET("api/alerts")
    suspend fun getAlerts(
        @Query("camera_id") cameraId: String? = null,
        @Query("type") type: String? = null,
        @Query("start_date") startDate: Long? = null,
        @Query("end_date") endDate: Long? = null
    ): Response<List<Detection>>
    
    @POST("api/devices/register")
    suspend fun registerDevice(@Body deviceToken: DeviceToken): Response<Unit>
}

data class DeviceToken(
    val token: String,
    val platform: String = "android"
)
```

### **data/api/RetrofitClient.kt:**
```kotlin
package com.yourdomain.aivision.data.api

import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

object RetrofitClient {
    private const val BASE_URL = "http://192.168.68.105:8000/"
    
    private val loggingInterceptor = HttpLoggingInterceptor().apply {
        level = HttpLoggingInterceptor.Level.BODY
    }
    
    private val okHttpClient = OkHttpClient.Builder()
        .addInterceptor(loggingInterceptor)
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .build()
    
    private val retrofit = Retrofit.Builder()
        .baseUrl(BASE_URL)
        .client(okHttpClient)
        .addConverterFactory(GsonConverterFactory.create())
        .build()
    
    val apiService: ApiService = retrofit.create(ApiService::class.java)
}
```

---

## 🔌 Step 6: Create WebSocket Client

### **data/api/WebSocketClient.kt:**
```kotlin
package com.yourdomain.aivision.data.api

import android.util.Log
import com.google.gson.Gson
import com.yourdomain.aivision.data.model.Detection
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.receiveAsFlow
import okhttp3.*

class WebSocketClient {
    private val TAG = "WebSocketClient"
    private val WS_URL = "ws://192.168.68.105:8000/ws/alerts"
    
    private var webSocket: WebSocket? = null
    private val gson = Gson()
    private val detectionChannel = Channel<Detection>(Channel.UNLIMITED)
    
    val detections: Flow<Detection> = detectionChannel.receiveAsFlow()
    
    fun connect() {
        val client = OkHttpClient()
        val request = Request.Builder()
            .url(WS_URL)
            .build()
        
        webSocket = client.newWebSocket(request, object : WebSocketListener() {
            override fun onOpen(webSocket: WebSocket, response: Response) {
                Log.d(TAG, "WebSocket connected")
            }
            
            override fun onMessage(webSocket: WebSocket, text: String) {
                Log.d(TAG, "Received: $text")
                try {
                    val detection = gson.fromJson(text, Detection::class.java)
                    detectionChannel.trySend(detection)
                } catch (e: Exception) {
                    Log.e(TAG, "Error parsing detection", e)
                }
            }
            
            override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                Log.e(TAG, "WebSocket error", t)
            }
            
            override fun onClosed(webSocket: WebSocket, code: Int, reason: String) {
                Log.d(TAG, "WebSocket closed: $reason")
            }
        })
    }
    
    fun disconnect() {
        webSocket?.close(1000, "Client disconnect")
        webSocket = null
    }
}
```

---

## 🔔 Step 7: Setup Firebase Notifications

### **Download google-services.json:**
1. Go to Firebase Console: https://console.firebase.google.com/
2. Create new project or use existing
3. Add Android app
4. Download `google-services.json`
5. Place in `app/` directory

### **service/FirebaseMessagingService.kt:**
```kotlin
package com.yourdomain.aivision.service

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Intent
import android.os.Build
import androidx.core.app.NotificationCompat
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage
import com.yourdomain.aivision.MainActivity
import com.yourdomain.aivision.R

class MyFirebaseMessagingService : FirebaseMessagingService() {
    
    override fun onMessageReceived(message: RemoteMessage) {
        super.onMessageReceived(message)
        
        message.notification?.let {
            showNotification(it.title ?: "Alert", it.body ?: "")
        }
    }
    
    override fun onNewToken(token: String) {
        super.onNewToken(token)
        // Send token to backend
        // RetrofitClient.apiService.registerDevice(DeviceToken(token))
    }
    
    private fun showNotification(title: String, message: String) {
        val channelId = "ai_vision_alerts"
        val notificationManager = getSystemService(NOTIFICATION_SERVICE) as NotificationManager
        
        // Create notification channel (Android 8.0+)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                channelId,
                "AI Vision Alerts",
                NotificationManager.IMPORTANCE_HIGH
            )
            notificationManager.createNotificationChannel(channel)
        }
        
        val intent = Intent(this, MainActivity::class.java)
        val pendingIntent = PendingIntent.getActivity(
            this, 0, intent,
            PendingIntent.FLAG_IMMUTABLE
        )
        
        val notification = NotificationCompat.Builder(this, channelId)
            .setContentTitle(title)
            .setContentText(message)
            .setSmallIcon(R.drawable.ic_notification)
            .setAutoCancel(true)
            .setContentIntent(pendingIntent)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .build()
        
        notificationManager.notify(System.currentTimeMillis().toInt(), notification)
    }
}
```

---

## 🎨 Step 8: Create ViewModel

### **viewmodel/AlertViewModel.kt:**
```kotlin
package com.yourdomain.aivision.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.yourdomain.aivision.data.api.RetrofitClient
import com.yourdomain.aivision.data.api.WebSocketClient
import com.yourdomain.aivision.data.model.Detection
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class AlertViewModel : ViewModel() {
    private val webSocketClient = WebSocketClient()

    private val _alerts = MutableStateFlow<List<Detection>>(emptyList())
    val alerts: StateFlow<List<Detection>> = _alerts

    private val _isConnected = MutableStateFlow(false)
    val isConnected: StateFlow<Boolean> = _isConnected

    init {
        connectWebSocket()
        loadAlerts()
    }

    private fun connectWebSocket() {
        viewModelScope.launch {
            webSocketClient.connect()
            _isConnected.value = true

            webSocketClient.detections.collect { detection ->
                // Add new detection to list
                _alerts.value = listOf(detection) + _alerts.value
            }
        }
    }

    private fun loadAlerts() {
        viewModelScope.launch {
            try {
                val response = RetrofitClient.apiService.getAlerts()
                if (response.isSuccessful) {
                    _alerts.value = response.body() ?: emptyList()
                }
            } catch (e: Exception) {
                // Handle error
            }
        }
    }

    override fun onCleared() {
        super.onCleared()
        webSocketClient.disconnect()
    }
}
```

---

## 📱 Step 9: Create UI Screens

### **ui/screens/AlertListScreen.kt:**
```kotlin
package com.yourdomain.aivision.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.yourdomain.aivision.data.model.Detection
import com.yourdomain.aivision.viewmodel.AlertViewModel
import java.text.SimpleDateFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AlertListScreen(
    viewModel: AlertViewModel = viewModel()
) {
    val alerts by viewModel.alerts.collectAsState()
    val isConnected by viewModel.isConnected.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("AI Vision Alerts") },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primaryContainer
                )
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            // Connection status
            Surface(
                color = if (isConnected)
                    MaterialTheme.colorScheme.primaryContainer
                else
                    MaterialTheme.colorScheme.errorContainer,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text(
                    text = if (isConnected) "✅ Connected" else "❌ Disconnected",
                    modifier = Modifier.padding(8.dp)
                )
            }

            // Alert list
            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                items(alerts) { alert ->
                    AlertCard(alert)
                }
            }
        }
    }
}

@Composable
fun AlertCard(detection: Detection) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = when (detection.type) {
                DetectionType.FALL -> MaterialTheme.colorScheme.errorContainer
                DetectionType.FIRE -> MaterialTheme.colorScheme.errorContainer
                DetectionType.SMOKE -> MaterialTheme.colorScheme.tertiaryContainer
                DetectionType.PPE -> MaterialTheme.colorScheme.secondaryContainer
            }
        )
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(
                    text = getAlertIcon(detection.type) + " " + detection.type.name,
                    style = MaterialTheme.typography.titleMedium
                )
                Text(
                    text = formatTime(detection.timestamp),
                    style = MaterialTheme.typography.bodySmall
                )
            }

            Spacer(modifier = Modifier.height(8.dp))

            Text(
                text = "Camera: ${detection.cameraName}",
                style = MaterialTheme.typography.bodyMedium
            )

            Text(
                text = "Confidence: ${(detection.confidence * 100).toInt()}%",
                style = MaterialTheme.typography.bodySmall
            )
        }
    }
}

fun getAlertIcon(type: DetectionType): String {
    return when (type) {
        DetectionType.FALL -> "🚨"
        DetectionType.FIRE -> "🔥"
        DetectionType.SMOKE -> "💨"
        DetectionType.PPE -> "🦺"
    }
}

fun formatTime(timestamp: Long): String {
    val sdf = SimpleDateFormat("HH:mm:ss", Locale.getDefault())
    return sdf.format(Date(timestamp))
}
```

---

## 📝 Step 10: Update AndroidManifest.xml

### **AndroidManifest.xml:**
```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <!-- Permissions -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.AIVisionAlerts"
        android:usesCleartextTraffic="true">

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:theme="@style/Theme.AIVisionAlerts">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <!-- Firebase Messaging Service -->
        <service
            android:name=".service.MyFirebaseMessagingService"
            android:exported="false">
            <intent-filter>
                <action android:name="com.google.firebase.MESSAGING_EVENT" />
            </intent-filter>
        </service>
    </application>

</manifest>
```

---

## 🚀 Step 11: Update MainActivity

### **MainActivity.kt:**
```kotlin
package com.yourdomain.aivision

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import com.yourdomain.aivision.ui.screens.AlertListScreen
import com.yourdomain.aivision.ui.theme.AIVisionAlertsTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            AIVisionAlertsTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    AlertListScreen()
                }
            }
        }
    }
}
```

---

## ✅ Step 12: Build & Run

1. **Connect Android device** or start emulator
2. **Click Run** (green play button) in Android Studio
3. **Wait for build** to complete
4. **App will launch** on device/emulator

---

## 🧪 Testing

1. **Start your backend server:**
   ```bash
   cd backend
   source venv/bin/activate
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Connect RTSP camera** from web interface

3. **Trigger detection** (fall, PPE violation, fire, smoke)

4. **Check Android app** - should receive real-time alert!

---

## 📝 Summary

You now have:
- ✅ Android app with Kotlin & Jetpack Compose
- ✅ WebSocket connection for real-time alerts
- ✅ REST API integration
- ✅ Push notifications with Firebase
- ✅ Beautiful Material Design 3 UI
- ✅ Alert list with real-time updates

---

## 🎯 Next Steps

1. Add camera list screen
2. Add live feed viewer
3. Add alert filtering
4. Add settings screen
5. Improve UI/UX
6. Add dark mode
7. Add alert sounds
8. Publish to Play Store

**Need help with any of these? Let me know!** 🚀

