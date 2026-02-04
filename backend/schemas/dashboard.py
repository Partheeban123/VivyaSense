"""
Dashboard schemas
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel
from datetime import datetime


class DashboardStats(BaseModel):
    """Dashboard statistics schema"""
    total_cameras: int
    active_cameras: int
    total_alerts_today: int
    total_alerts_week: int
    total_alerts_month: int
    critical_alerts_count: int
    detection_type_breakdown: Dict[str, int]  # {FALL: 5, FIRE: 2, etc.}
    average_response_time: Optional[float]  # in seconds
    alerts_by_severity: Dict[str, int]  # {CRITICAL: 3, HIGH: 5, etc.}
    top_cameras_by_alerts: List[Dict[str, Any]]  # [{camera_id, camera_name, count}]


class AlertsOverTime(BaseModel):
    """Alerts over time schema"""
    period: str  # hour, day, week, month
    data: List[Dict[str, Any]]  # [{timestamp, count, detection_type}]


class DetectionBreakdown(BaseModel):
    """Detection type breakdown schema"""
    FALL: int = 0
    FIRE: int = 0
    SMOKE: int = 0
    PPE: int = 0
    total: int


class CameraActivity(BaseModel):
    """Camera activity schema"""
    camera_id: str
    camera_name: str
    alert_count: int
    last_alert_at: Optional[datetime]


class ResponseMetrics(BaseModel):
    """Response time metrics schema"""
    avg_response_time: Optional[float]  # seconds
    avg_resolution_time: Optional[float]  # seconds
    fastest_response: Optional[float]  # seconds
    slowest_response: Optional[float]  # seconds
    total_alerts: int
    acknowledged_alerts: int
    resolved_alerts: int


class UserActivity(BaseModel):
    """User activity schema"""
    user_id: str
    user_name: str
    action: str
    resource_type: Optional[str]
    resource_id: Optional[str]
    timestamp: datetime
    details: Optional[Dict[str, Any]]
