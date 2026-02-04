"""
Camera management API endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from core.logger import log

router = APIRouter()


class CameraCreate(BaseModel):
    name: str
    description: Optional[str] = None
    stream_url: str
    camera_type: str  # 'rtsp', 'file', 'webcam'
    location: Optional[str] = None
    detection_types: List[str]
    confidence_threshold: float = 0.5
    alert_enabled: bool = True


class CameraResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    stream_url: str
    camera_type: str
    location: Optional[str]
    is_active: bool
    detection_types: List[str]
    confidence_threshold: float
    alert_enabled: bool
    created_at: datetime


@router.post("/", response_model=CameraResponse)
async def create_camera(camera: CameraCreate):
    """Create a new camera"""
    log.info(f"Creating camera: {camera.name}")
    
    # In production, save to database
    return {
        "id": "cam_123",
        "name": camera.name,
        "description": camera.description,
        "stream_url": camera.stream_url,
        "camera_type": camera.camera_type,
        "location": camera.location,
        "is_active": True,
        "detection_types": camera.detection_types,
        "confidence_threshold": camera.confidence_threshold,
        "alert_enabled": camera.alert_enabled,
        "created_at": datetime.utcnow()
    }


@router.get("/", response_model=List[CameraResponse])
async def list_cameras():
    """List all cameras"""
    # In production, fetch from database
    return []


@router.get("/{camera_id}", response_model=CameraResponse)
async def get_camera(camera_id: str):
    """Get camera by ID"""
    # In production, fetch from database
    raise HTTPException(status_code=404, detail="Camera not found")


@router.put("/{camera_id}", response_model=CameraResponse)
async def update_camera(camera_id: str, camera: CameraCreate):
    """Update camera"""
    log.info(f"Updating camera: {camera_id}")
    # In production, update in database
    raise HTTPException(status_code=404, detail="Camera not found")


@router.delete("/{camera_id}")
async def delete_camera(camera_id: str):
    """Delete camera"""
    log.info(f"Deleting camera: {camera_id}")
    # In production, delete from database
    return {"message": "Camera deleted successfully"}


@router.post("/{camera_id}/start")
async def start_camera(camera_id: str):
    """Start camera stream processing"""
    log.info(f"Starting camera: {camera_id}")
    # In production, start video processing
    return {"message": "Camera started", "status": "active"}


@router.post("/{camera_id}/stop")
async def stop_camera(camera_id: str):
    """Stop camera stream processing"""
    log.info(f"Stopping camera: {camera_id}")
    # In production, stop video processing
    return {"message": "Camera stopped", "status": "inactive"}

