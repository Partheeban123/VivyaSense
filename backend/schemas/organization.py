"""
Organization schemas
"""
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class OrganizationCreate(BaseModel):
    """Organization creation schema"""
    name: str = Field(..., min_length=2, max_length=100)
    industry: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    logo: Optional[str] = None


class OrganizationUpdate(BaseModel):
    """Organization update schema"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    industry: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    logo: Optional[str] = None
    subscription_plan: Optional[str] = None
    max_cameras: Optional[int] = None
    max_users: Optional[int] = None
    features: Optional[List[str]] = None


class OrganizationResponse(BaseModel):
    """Organization response schema"""
    id: str
    name: str
    industry: Optional[str]
    address: Optional[str]
    city: Optional[str]
    country: Optional[str]
    logo: Optional[str]
    subscription_plan: str
    max_cameras: int
    max_users: int
    features: List[str]
    admin_user_id: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class OrganizationStats(BaseModel):
    """Organization statistics schema"""
    total_users: int
    active_users: int
    total_cameras: int
    active_cameras: int
    total_detections_today: int
    total_detections_week: int
    total_detections_month: int
    critical_alerts: int
    storage_used_gb: float

