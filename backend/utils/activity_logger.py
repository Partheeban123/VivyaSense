"""
Activity logging utility
"""
from sqlalchemy.orm import Session
from database.models import ActivityLog, User
from fastapi import Request
from typing import Optional, Dict, Any
from datetime import datetime
from core.logger import log


def log_activity(
    db: Session,
    user: User,
    action: str,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    request: Optional[Request] = None
):
    """
    Log user activity
    
    Args:
        db: Database session
        user: User performing the action
        action: Action performed (e.g., "login", "acknowledge_alert", "create_camera")
        resource_type: Type of resource (e.g., "alert", "camera", "user")
        resource_id: ID of the resource
        details: Additional details as JSON
        request: FastAPI request object for IP and user agent
    """
    try:
        ip_address = None
        user_agent = None
        
        if request:
            # Get IP address
            if request.client:
                ip_address = request.client.host
            
            # Get user agent
            user_agent = request.headers.get("user-agent")
        
        activity = ActivityLog(
            user_id=user.id,
            organization_id=user.organization_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details or {},
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        db.add(activity)
        db.commit()
        
        log.info(f"Activity logged: {action} by user {user.id} on {resource_type} {resource_id}")
        
    except Exception as e:
        log.error(f"Failed to log activity: {str(e)}")
        db.rollback()


def get_user_activities(
    db: Session,
    organization_id: str,
    user_id: Optional[str] = None,
    action: Optional[str] = None,
    resource_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 100,
    offset: int = 0
):
    """
    Get activity logs with filters
    
    Args:
        db: Database session
        organization_id: Organization ID
        user_id: Filter by user ID
        action: Filter by action
        resource_type: Filter by resource type
        start_date: Filter by start date
        end_date: Filter by end date
        limit: Maximum number of results
        offset: Offset for pagination
    
    Returns:
        List of activity logs
    """
    query = db.query(ActivityLog).filter(ActivityLog.organization_id == organization_id)
    
    if user_id:
        query = query.filter(ActivityLog.user_id == user_id)
    
    if action:
        query = query.filter(ActivityLog.action == action)
    
    if resource_type:
        query = query.filter(ActivityLog.resource_type == resource_type)
    
    if start_date:
        query = query.filter(ActivityLog.created_at >= start_date)
    
    if end_date:
        query = query.filter(ActivityLog.created_at <= end_date)
    
    query = query.order_by(ActivityLog.created_at.desc())
    query = query.limit(limit).offset(offset)
    
    return query.all()

