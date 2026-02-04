"""
Configuration management for AI Vision Platform
"""
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, validator
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "AI Vision Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    
    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 0
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS - Allow access from localhost and network
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:8000",
        "http://192.168.68.94:3000",
        "http://192.168.68.94:3001",
        "http://0.0.0.0:3000",
        "http://0.0.0.0:3001"
    ]
    
    # AI Models
    MODEL_PATH: str = "./models"
    PPE_MODEL_PATH: str = "./models/ppe_detection.pt"
    FALL_MODEL_PATH: str = "./models/fall_detection.pt"
    FIRE_MODEL_PATH: str = "./models/fire_smoke_detection.pt"
    CONFIDENCE_THRESHOLD: float = 0.5
    IOU_THRESHOLD: float = 0.45

    # Fall Detection (Advanced - YOLOv11-pose + GRU)
    FALL_YOLO_MODEL_PATH: str = "./models/yolo11s-pose.pt"
    FALL_GRU_MODEL_PATH: str = "./models/gru_model_binary_old.pth"
    FALL_SEQUENCE_LENGTH: int = 15  # Number of frames to analyze
    FALL_THRESHOLD: float = 0.90  # Probability threshold for fall detection (high precision)
    FALL_CONFIDENCE_THRESHOLD: float = 0.5  # YOLO confidence threshold

    # Fire and Smoke Detection (Using fire_detection.pt which detects both fire and smoke)
    # Both models have 2 classes (fire_detection.pt: 0=smoke, 1=fire)
    # Currently using fire_detection.pt - can be changed to smoke_detection.pt if needed
    FIRE_SMOKE_MODEL_PATH: str = "./models/fire_detection.pt"
    FIRE_SMOKE_CONFIDENCE_THRESHOLD: float = 0.5  # Confidence threshold for fire/smoke detection
    
    # Video Processing
    MAX_VIDEO_SIZE_MB: int = 500
    SUPPORTED_VIDEO_FORMATS: List[str] = ["mp4", "avi", "mov", "mkv"]
    FRAME_RATE: int = 30
    VIDEO_RESOLUTION_WIDTH: int = 1920
    VIDEO_RESOLUTION_HEIGHT: int = 1080
    
    # WebSocket
    WS_HEARTBEAT_INTERVAL: int = 30
    WS_MAX_CONNECTIONS: int = 100
    
    # Storage
    UPLOAD_DIR: str = "./uploads"
    DETECTION_RESULTS_DIR: str = "./results"
    MAX_STORAGE_GB: int = 100
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"
    
    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: str = "noreply@aivision.com"
    FROM_EMAIL: Optional[str] = None
    FROM_NAME: str = "AI Vision Platform"
    ADMIN_EMAIL: str = "admin@aivision.com"
    
    # Monitoring
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    
    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("SUPPORTED_VIDEO_FORMATS", pre=True)
    def parse_video_formats(cls, v):
        if isinstance(v, str):
            return [fmt.strip() for fmt in v.split(",")]
        return v
    
    def create_directories(self):
        """Create necessary directories"""
        directories = [
            self.MODEL_PATH,
            self.UPLOAD_DIR,
            self.DETECTION_RESULTS_DIR,
            os.path.dirname(self.LOG_FILE)
        ]
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

# Create necessary directories on startup
settings.create_directories()

