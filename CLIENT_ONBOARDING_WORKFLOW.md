# 🎯 VivyaSense Platform - Complete Client Onboarding Workflow

## 📋 Table of Contents
1. [Client Signup & Form Submission](#1-client-signup--form-submission)
2. [Technical Discovery & Requirements](#2-technical-discovery--requirements)
3. [Camera Integration (RTSP/RTMP)](#3-camera-integration-rtsprtmp)
4. [Alert Configuration](#4-alert-configuration)
5. [Hosting & Deployment](#5-hosting--deployment)
6. [Monitoring & Maintenance](#6-monitoring--maintenance)
7. [Billing & Subscription](#7-billing--subscription)

---

## 1. Client Signup & Form Submission

### **What Client Provides:**
```
Contact Form Submission:
├── Company Name
├── Contact Person
├── Email Address
├── Phone Number
├── Industry Type (Construction, Manufacturing, Retail, etc.)
├── Use Case (PPE Detection, Fire Detection, etc.)
├── Number of Cameras
└── Preferred Deployment (Cloud/On-Premise)
```

### **Your Immediate Actions:**
1. ✅ **Send Automated Email** (within 5 minutes)
   - Thank you message
   - What happens next
   - Expected response time (24-48 hours)
   - Link to schedule discovery call

2. ✅ **Create Client Record** in CRM/Database
   - Assign unique Client ID
   - Set status: "Lead - Pending Discovery"
   - Assign account manager

3. ✅ **Schedule Discovery Call** (within 24-48 hours)
   - 30-60 minute technical consultation
   - Understand requirements
   - Assess technical feasibility

---

## 2. Technical Discovery & Requirements

### **Discovery Call Checklist:**

#### **A. Camera Infrastructure Assessment**
```
Questions to Ask:
├── How many cameras do you have?
├── What camera brands/models? (Hikvision, Dahua, Axis, etc.)
├── Are cameras IP-based or analog?
├── Do cameras support RTSP/RTMP streaming?
├── What is the camera resolution? (1080p, 4K, etc.)
├── What is the frame rate? (15fps, 30fps, etc.)
├── Where are cameras located? (Indoor/Outdoor)
├── Do you have existing NVR/DVR system?
├── What is your network bandwidth?
└── Do you have VPN access for remote connection?
```

#### **B. Use Case & Detection Requirements**
```
Questions to Ask:
├── What do you want to detect? (PPE, Fire, Falls, etc.)
├── Which areas need monitoring? (Specific zones/ROI)
├── What are your compliance requirements? (OSHA, ISO, etc.)
├── Do you need 24/7 monitoring or specific hours?
├── How many concurrent video streams?
├── Do you need video recording/storage?
├── How long should recordings be retained? (7 days, 30 days, etc.)
└── Do you need historical video search?
```

#### **C. Alert & Notification Requirements**
```
Questions to Ask:
├── Who should receive alerts? (Email, SMS, Push, etc.)
├── What types of alerts? (Real-time, Daily summary, etc.)
├── Alert priority levels? (Critical, Warning, Info)
├── Integration with existing systems? (Email, Slack, Teams, etc.)
├── Do you need escalation rules? (If no response in X minutes)
├── Alert frequency limits? (Max alerts per hour)
└── Do you need alert acknowledgment tracking?
```

#### **D. Deployment Preferences**
```
Questions to Ask:
├── Cloud or On-Premise deployment?
├── If Cloud: Which region? (US, EU, Asia)
├── If On-Premise: Do you have server infrastructure?
├── What is your internet bandwidth?
├── Do you have IT team for support?
├── Security requirements? (Firewall, VPN, etc.)
├── Compliance requirements? (GDPR, HIPAA, SOC2, etc.)
└── Budget constraints?
```

---

## 3. Camera Integration (RTSP/RTMP)

### **Step 1: Get Camera Credentials**

**What You Need from Client:**
```json
{
  "camera_id": "CAM-001",
  "camera_name": "Main Entrance",
  "camera_brand": "Hikvision",
  "camera_model": "DS-2CD2143G0-I",
  "ip_address": "192.168.1.100",
  "rtsp_port": 554,
  "username": "admin",
  "password": "********",
  "rtsp_url": "rtsp://admin:password@192.168.1.100:554/Streaming/Channels/101",
  "location": "Building A - Main Entrance",
  "detection_types": ["ppe", "intrusion"],
  "recording_enabled": true,
  "resolution": "1920x1080",
  "fps": 25
}
```

### **Step 2: Test Camera Connection**

**Create Camera Testing Script:**
```python
# test_camera_connection.py
import cv2
import time

def test_rtsp_connection(rtsp_url, camera_name):
    """Test RTSP camera connection"""
    print(f"Testing camera: {camera_name}")
    print(f"RTSP URL: {rtsp_url}")
    
    try:
        cap = cv2.VideoCapture(rtsp_url)
        
        if not cap.isOpened():
            print("❌ Failed to connect to camera")
            return False
        
        # Read a few frames to ensure stable connection
        for i in range(10):
            ret, frame = cap.read()
            if not ret:
                print(f"❌ Failed to read frame {i+1}")
                return False
        
        # Get camera properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        
        print(f"✅ Camera connected successfully!")
        print(f"   Resolution: {width}x{height}")
        print(f"   FPS: {fps}")
        
        cap.release()
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

# Test camera
rtsp_url = "rtsp://admin:password@192.168.1.100:554/Streaming/Channels/101"
test_rtsp_connection(rtsp_url, "Main Entrance")
```

### **Step 3: Add Camera to Database**

**Database Schema:**
```sql
CREATE TABLE cameras (
    id UUID PRIMARY KEY,
    client_id UUID REFERENCES clients(id),
    camera_name VARCHAR(255),
    camera_brand VARCHAR(100),
    camera_model VARCHAR(100),
    ip_address VARCHAR(50),
    rtsp_url TEXT ENCRYPTED,  -- Encrypt credentials!
    location VARCHAR(255),
    detection_types JSONB,
    status VARCHAR(50),  -- active, inactive, error
    last_seen TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### **Step 4: Configure Camera Stream Processing**

**Stream Configuration:**
```json
{
  "camera_id": "CAM-001",
  "processing_config": {
    "frame_skip": 2,  -- Process every 2nd frame (optimize performance)
    "resize_width": 640,  -- Resize for faster processing
    "detection_interval": 1,  -- Run detection every 1 second
    "confidence_threshold": 0.5,
    "roi_zones": [
      {
        "name": "Restricted Area",
        "coordinates": [[100, 100], [500, 100], [500, 400], [100, 400]],
        "detection_types": ["intrusion", "ppe"]
      }
    ],
    "recording": {
      "enabled": true,
      "retention_days": 30,
      "record_on_detection_only": true
    }
  }
}
```

---

## 4. Alert Configuration

### **Alert Types & Channels**

#### **A. Alert Channels**
```
1. Email Alerts
   ├── SMTP Configuration
   ├── Email Templates
   ├── Attachment: Detection snapshot
   └── Priority: High/Medium/Low

2. SMS Alerts
   ├── Twilio/AWS SNS Integration
   ├── Phone number verification
   ├── Message templates
   └── Rate limiting (avoid spam)

3. Push Notifications
   ├── Mobile app (iOS/Android)
   ├── Web push notifications
   └── Desktop notifications

4. Webhook/API
   ├── POST to client's endpoint
   ├── JSON payload with detection data
   └── Retry logic on failure

5. Third-Party Integrations
   ├── Slack
   ├── Microsoft Teams
   ├── PagerDuty
   ├── Jira (create tickets)
   └── Custom integrations
```

#### **B. Alert Rules Configuration**

**Create Alert Rules Table:**
```sql
CREATE TABLE alert_rules (
    id UUID PRIMARY KEY,
    client_id UUID REFERENCES clients(id),
    camera_id UUID REFERENCES cameras(id),
    detection_type VARCHAR(50),  -- ppe, fire, fall, intrusion
    severity VARCHAR(20),  -- critical, warning, info
    channels JSONB,  -- ["email", "sms", "slack"]
    recipients JSONB,  -- List of email/phone numbers
    conditions JSONB,  -- Alert conditions
    throttle_minutes INTEGER,  -- Min time between alerts
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP
);
```

**Example Alert Rule:**
```json
{
  "rule_id": "RULE-001",
  "rule_name": "PPE Violation - Critical",
  "client_id": "CLIENT-123",
  "camera_id": "CAM-001",
  "detection_type": "ppe",
  "conditions": {
    "compliance_status": "non-compliant",
    "min_confidence": 0.7,
    "consecutive_detections": 3  -- Alert after 3 consecutive violations
  },
  "severity": "critical",
  "channels": ["email", "sms", "slack"],
  "recipients": {
    "email": ["safety@company.com", "manager@company.com"],
    "sms": ["+1234567890"],
    "slack": ["#safety-alerts"]
  },
  "throttle_minutes": 5,  -- Max 1 alert per 5 minutes
  "escalation": {
    "enabled": true,
    "escalate_after_minutes": 15,
    "escalate_to": ["director@company.com"]
  }
}
```

#### **C. Alert Notification Service**

**Backend Implementation:**
```python
# backend/services/alert_service.py
from typing import List, Dict
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import requests
from twilio.rest import Client

class AlertService:
    def __init__(self):
        self.smtp_config = {
            'host': 'smtp.gmail.com',
            'port': 587,
            'username': 'alerts@vivyasense.com',
            'password': 'your-app-password'
        }
        self.twilio_client = Client('account_sid', 'auth_token')
        self.slack_webhook = 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'

    async def send_alert(self, alert_data: Dict):
        """Send alert through configured channels"""
        channels = alert_data.get('channels', [])

        if 'email' in channels:
            await self.send_email_alert(alert_data)

        if 'sms' in channels:
            await self.send_sms_alert(alert_data)

        if 'slack' in channels:
            await self.send_slack_alert(alert_data)

    async def send_email_alert(self, alert_data: Dict):
        """Send email alert with detection snapshot"""
        msg = MIMEMultipart()
        msg['From'] = self.smtp_config['username']
        msg['To'] = ', '.join(alert_data['recipients']['email'])
        msg['Subject'] = f"🚨 {alert_data['severity'].upper()}: {alert_data['detection_type']} Detected"

        # Email body with detection details
        body = f"""
        <html>
        <body>
            <h2>Detection Alert</h2>
            <p><strong>Camera:</strong> {alert_data['camera_name']}</p>
            <p><strong>Location:</strong> {alert_data['location']}</p>
            <p><strong>Detection Type:</strong> {alert_data['detection_type']}</p>
            <p><strong>Time:</strong> {alert_data['timestamp']}</p>
            <p><strong>Confidence:</strong> {alert_data['confidence']}%</p>
        </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        # Send email
        with smtplib.SMTP(self.smtp_config['host'], self.smtp_config['port']) as server:
            server.starttls()
            server.login(self.smtp_config['username'], self.smtp_config['password'])
            server.send_message(msg)
```

---

## 5. Hosting & Deployment

### **Deployment Options**

#### **Option A: Cloud Deployment (Recommended)**

**Infrastructure Stack:**
```
Cloud Provider: AWS / Azure / Google Cloud
├── Compute: GPU-enabled instances for AI processing
├── Storage: S3/Blob Storage for video recordings
├── Database: PostgreSQL/MongoDB
├── Networking: VPC with VPN Gateway
└── Services: Kubernetes/Docker containers
```

**Cost Estimation (Per Client):**
```
Monthly Cloud Costs:
├── Compute (GPU Instance): $300-500/month
├── Storage (1TB): $23/month
├── Database: $50-100/month
├── Data Transfer: $50-100/month
└── Total: ~$450-750/month

Pricing to Client: $1,500-3,000/month
Margin: 50-75%
```

#### **Option B: On-Premise Deployment**

**Hardware Requirements:**
```
Server Specifications:
├── CPU: Intel Xeon (16+ cores)
├── RAM: 64GB minimum
├── GPU: NVIDIA RTX 3090 / A4000
├── Storage: 4TB SSD + 20TB HDD
└── OS: Ubuntu 22.04 LTS

Cost: $8,000-15,000 one-time
```

---

## 6. Monitoring & Maintenance

### **System Monitoring**

**What to Monitor:**
```
1. Camera Health
   ├── Connection status
   ├── Frame rate
   ├── Video quality
   └── Last seen timestamp

2. AI Processing
   ├── Detection latency
   ├── GPU utilization
   ├── Queue depth
   └── Error rate

3. Alert System
   ├── Alerts sent
   ├── Delivery success rate
   └── Response time

4. Storage
   ├── Disk usage
   ├── Recording retention
   └── Backup status
```

**Monitoring Tools:**
```
├── Prometheus (Metrics)
├── Grafana (Visualization)
├── ELK Stack (Logs)
└── PagerDuty (Incidents)
```

---

## 7. Billing & Subscription

### **Pricing Models**

#### **Per Camera Pricing**
```
Basic (1-5 cameras): $200/camera/month
├── Basic detection
├── Email alerts
└── 7 days storage

Professional (6-20 cameras): $150/camera/month
├── All detections
├── Multi-channel alerts
└── 30 days storage

Enterprise (21+ cameras): $100/camera/month
├── Custom AI models
├── Dedicated support
└── 90 days storage
```

#### **Flat Rate Pricing**
```
Small Business: $1,500/month
├── Up to 10 cameras
├── All detection types
└── 30 days storage

Enterprise: $5,000/month
├── Up to 50 cameras
├── Custom AI models
└── 90 days storage
```

