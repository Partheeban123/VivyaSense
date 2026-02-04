"""
Dashboard and analytics API endpoints
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime, timedelta

from core.logger import log

router = APIRouter()


class DashboardStats(BaseModel):
    total_cameras: int
    active_cameras: int
    total_detections_today: int
    total_alerts_today: int
    detection_breakdown: Dict[str, int]


class DetectionTrend(BaseModel):
    date: str
    count: int
    detection_type: str


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats():
    """Get dashboard statistics"""
    # In production, fetch from database
    return {
        "total_cameras": 10,
        "active_cameras": 7,
        "total_detections_today": 245,
        "total_alerts_today": 12,
        "detection_breakdown": {
            "ppe": 120,
            "fall": 15,
            "fire": 10
        }
    }


@router.get("/trends", response_model=List[DetectionTrend])
async def get_detection_trends(days: int = 7):
    """Get detection trends over time"""
    # In production, fetch from database
    trends = []
    for i in range(days):
        date = (datetime.utcnow() - timedelta(days=i)).strftime("%Y-%m-%d")
        trends.append({
            "date": date,
            "count": 30 + i * 5,
            "detection_type": "ppe"
        })
    return trends


@router.get("/recent-detections")
async def get_recent_detections(limit: int = 10):
    """Get recent detections"""
    # In production, fetch from database
    return {
        "detections": [],
        "total": 0
    }


@router.get("/alerts")
async def get_alerts(limit: int = 10):
    """Get recent alerts"""
    # In production, fetch from database
    return {
        "alerts": [],
        "total": 0
    }

