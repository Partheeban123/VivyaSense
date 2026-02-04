"""
Detection and alert schemas
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class DetectionResponse(BaseModel):
    """Detection response schema"""
    id: str
    camera_id: str
    organization_id: str
    detection_type: str
    class_name: Optional[str]
    confidence: float
    bounding_box: Optional[Dict[str, Any]]
    image_path: Optional[str]
    video_timestamp: Optional[float]
    detected_at: datetime
    status: str
    severity: str
    alert_sent: bool
    alert_acknowledged: bool
    acknowledged_at: Optional[datetime]
    acknowledged_by: Optional[str]
    assigned_to: Optional[str]
    notes: Optional[str]
    response_time: Optional[int]
    resolution_time: Optional[int]
    
    class Config:
        from_attributes = True


class AlertAcknowledge(BaseModel):
    """Alert acknowledgment schema"""
    notes: Optional[str] = None


class AlertStatusUpdate(BaseModel):
    """Alert status update schema"""
    status: str = Field(..., pattern=r'^(NEW|ACKNOWLEDGED|IN_PROGRESS|RESOLVED|FALSE_POSITIVE)$')
    notes: Optional[str] = None


class AlertAssign(BaseModel):
    """Alert assignment schema"""
    user_id: str
    notes: Optional[str] = None


class AlertNoteAdd(BaseModel):
    """Add note to alert schema"""
    note: str = Field(..., min_length=1, max_length=1000)


class AlertFalsePositive(BaseModel):
    """Mark alert as false positive schema"""
    reason: Optional[str] = None


class AlertDetailResponse(BaseModel):
    """Detailed alert response"""
    id: str
    camera_id: str
    camera_name: Optional[str]
    organization_id: str
    detection_type: str
    class_name: Optional[str]
    confidence: float
    bounding_box: Optional[Dict[str, Any]]
    image_path: Optional[str]
    video_timestamp: Optional[float]
    detected_at: datetime
    status: str
    severity: str
    alert_sent: bool
    alert_acknowledged: bool
    acknowledged_at: Optional[datetime]
    acknowledged_by: Optional[str]
    acknowledged_by_name: Optional[str]
    assigned_to: Optional[str]
    assigned_to_name: Optional[str]
    notes: Optional[str]
    response_time: Optional[int]
    resolution_time: Optional[int]
    extra_data: Optional[Dict[str, Any]]
    
    class Config:
        from_attributes = True

