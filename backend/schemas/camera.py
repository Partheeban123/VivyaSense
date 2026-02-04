"""
Camera schemas
"""
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class CameraCreate(BaseModel):
    """Camera creation schema"""
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    stream_url: str
    camera_type: str = Field(..., pattern=r'^(rtsp|file|webcam)$')
    location: Optional[str] = None
    detection_types: List[str] = Field(default_factory=list)
    confidence_threshold: float = Field(default=0.5, ge=0.0, le=1.0)
    alert_enabled: bool = True


class CameraUpdate(BaseModel):
    """Camera update schema"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None
    stream_url: Optional[str] = None
    camera_type: Optional[str] = Field(None, pattern=r'^(rtsp|file|webcam)$')
    location: Optional[str] = None
    detection_types: Optional[List[str]] = None
    confidence_threshold: Optional[float] = Field(None, ge=0.0, le=1.0)
    alert_enabled: Optional[bool] = None
    is_active: Optional[bool] = None


class CameraResponse(BaseModel):
    """Camera response schema"""
    id: str
    name: str
    description: Optional[str]
    stream_url: str
    camera_type: str
    location: Optional[str]
    organization_id: str
    owner_id: Optional[str]
    created_by: Optional[str]
    detection_types: List[str]
    confidence_threshold: float
    alert_enabled: bool
    last_detection_at: Optional[datetime]
    detection_count_today: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CameraStats(BaseModel):
    """Camera statistics schema"""
    camera_id: str
    camera_name: str
    total_detections: int
    detections_today: int
    last_detection_at: Optional[datetime]
    detection_breakdown: dict  # {FALL: 5, FIRE: 2, etc.}

