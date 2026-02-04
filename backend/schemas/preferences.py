"""
User preferences schemas
"""
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import time


class UserPreferencesUpdate(BaseModel):
    """User preferences update schema"""
    notification_push_enabled: Optional[bool] = None
    notification_email_enabled: Optional[bool] = None
    notification_sms_enabled: Optional[bool] = None
    quiet_hours_start: Optional[time] = None
    quiet_hours_end: Optional[time] = None
    alert_types: Optional[List[str]] = None
    minimum_confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    language: Optional[str] = None
    timezone: Optional[str] = None
    theme: Optional[str] = Field(None, pattern=r'^(light|dark|system)$')
    default_view: Optional[str] = Field(None, pattern=r'^(dashboard|cameras|alerts)$')


class UserPreferencesResponse(BaseModel):
    """User preferences response schema"""
    id: str
    user_id: str
    notification_push_enabled: bool
    notification_email_enabled: bool
    notification_sms_enabled: bool
    quiet_hours_start: Optional[time]
    quiet_hours_end: Optional[time]
    alert_types: List[str]
    minimum_confidence: float
    language: str
    timezone: str
    theme: str
    default_view: str
    
    class Config:
        from_attributes = True

