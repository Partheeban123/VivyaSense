"""
Database models for AI Vision Platform
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, JSON, Enum, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


# Enums
class UserRole(str, enum.Enum):
    """User role enumeration"""
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    OPERATOR = "OPERATOR"
    VIEWER = "VIEWER"


class SubscriptionPlan(str, enum.Enum):
    """Subscription plan enumeration"""
    FREE = "FREE"
    BASIC = "BASIC"
    PROFESSIONAL = "PROFESSIONAL"
    ENTERPRISE = "ENTERPRISE"


class AlertStatus(str, enum.Enum):
    """Alert status enumeration"""
    NEW = "NEW"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    FALSE_POSITIVE = "FALSE_POSITIVE"


class AlertSeverity(str, enum.Enum):
    """Alert severity enumeration"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Organization(Base):
    """Organization model"""
    __tablename__ = "organizations"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, unique=True, nullable=False, index=True)
    industry = Column(String)  # Security, Healthcare, Retail, etc.
    address = Column(String)
    city = Column(String)
    country = Column(String)
    logo = Column(String)  # URL to logo image

    # Subscription
    subscription_plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.FREE)
    max_cameras = Column(Integer, default=5)
    max_users = Column(Integer, default=10)
    features = Column(JSON, default=list)  # ["analytics", "reports", "api_access"]

    # Admin
    admin_user_id = Column(String, ForeignKey("users.id"), nullable=True)

    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    users = relationship("User", back_populates="organization", foreign_keys="User.organization_id")
    cameras = relationship("Camera", back_populates="organization")
    detections = relationship("Detection", back_populates="organization")
    activity_logs = relationship("ActivityLog", back_populates="organization")


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)  # Required for SMS alerts

    # Organization
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False, index=True)
    role = Column(Enum(UserRole), default=UserRole.VIEWER, nullable=False)
    department = Column(String)
    employee_id = Column(String)

    # Profile
    profile_image = Column(String)  # URL to profile image

    # Status
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    organization = relationship("Organization", back_populates="users", foreign_keys=[organization_id])
    cameras = relationship("Camera", back_populates="owner", foreign_keys="Camera.owner_id")
    created_cameras = relationship("Camera", back_populates="creator", foreign_keys="Camera.created_by")
    detections = relationship("Detection", back_populates="user", foreign_keys="Detection.user_id")
    preferences = relationship("UserPreferences", back_populates="user", uselist=False)
    activity_logs = relationship("ActivityLog", back_populates="user")
    acknowledged_detections = relationship("Detection", back_populates="acknowledged_user", foreign_keys="Detection.acknowledged_by")
    assigned_detections = relationship("Detection", back_populates="assigned_user", foreign_keys="Detection.assigned_to")


class UserPreferences(Base):
    """User preferences model"""
    __tablename__ = "user_preferences"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), unique=True, nullable=False)

    # Notification preferences
    notification_push_enabled = Column(Boolean, default=True)
    notification_email_enabled = Column(Boolean, default=True)
    notification_sms_enabled = Column(Boolean, default=False)

    # Quiet hours
    quiet_hours_start = Column(Time)  # e.g., 22:00
    quiet_hours_end = Column(Time)  # e.g., 07:00

    # Alert preferences
    alert_types = Column(JSON, default=list)  # ["FALL", "FIRE", "SMOKE", "PPE"]
    minimum_confidence = Column(Float, default=0.7)

    # UI preferences
    language = Column(String, default="en")
    timezone = Column(String, default="UTC")
    theme = Column(String, default="light")  # light, dark, system
    default_view = Column(String, default="dashboard")  # dashboard, cameras, alerts

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="preferences")


class Camera(Base):
    """Camera/Video source model"""
    __tablename__ = "cameras"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    description = Column(Text)
    stream_url = Column(String)  # RTSP URL or video file path
    camera_type = Column(String)  # 'rtsp', 'file', 'webcam'
    location = Column(String)

    # Organization
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False, index=True)
    owner_id = Column(String, ForeignKey("users.id"))
    created_by = Column(String, ForeignKey("users.id"))

    # Configuration
    detection_types = Column(JSON)  # ['ppe', 'fall', 'fire']
    confidence_threshold = Column(Float, default=0.5)
    alert_enabled = Column(Boolean, default=True)

    # Statistics
    last_detection_at = Column(DateTime)
    detection_count_today = Column(Integer, default=0)

    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    organization = relationship("Organization", back_populates="cameras")
    owner = relationship("User", back_populates="cameras", foreign_keys=[owner_id])
    creator = relationship("User", back_populates="created_cameras", foreign_keys=[created_by])
    detections = relationship("Detection", back_populates="camera")


class Detection(Base):
    """Detection event model"""
    __tablename__ = "detections"

    id = Column(String, primary_key=True, default=generate_uuid)
    camera_id = Column(String, ForeignKey("cameras.id"), index=True)
    user_id = Column(String, ForeignKey("users.id"))
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False, index=True)

    # Detection details
    detection_type = Column(String, index=True)  # 'ppe', 'fall', 'fire', 'smoke'
    class_name = Column(String)  # Specific class detected
    confidence = Column(Float)
    bounding_box = Column(JSON)  # {x, y, width, height}
    image_path = Column(String)  # Path to saved detection image
    video_timestamp = Column(Float)  # Timestamp in video
    detected_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Alert management
    status = Column(Enum(AlertStatus), default=AlertStatus.NEW, nullable=False, index=True)
    severity = Column(Enum(AlertSeverity), default=AlertSeverity.MEDIUM, nullable=False)
    alert_sent = Column(Boolean, default=False)

    # Acknowledgment
    alert_acknowledged = Column(Boolean, default=False)
    acknowledged_at = Column(DateTime)
    acknowledged_by = Column(String, ForeignKey("users.id"))

    # Assignment
    assigned_to = Column(String, ForeignKey("users.id"))

    # Notes and resolution
    notes = Column(Text)
    response_time = Column(Integer)  # Seconds from detection to acknowledgment
    resolution_time = Column(Integer)  # Seconds from detection to resolution

    # Additional metadata
    extra_data = Column(JSON)  # Renamed from 'metadata' to avoid SQLAlchemy reserved name

    # Relationships
    camera = relationship("Camera", back_populates="detections")
    user = relationship("User", back_populates="detections", foreign_keys=[user_id])
    organization = relationship("Organization", back_populates="detections")
    acknowledged_user = relationship("User", back_populates="acknowledged_detections", foreign_keys=[acknowledged_by])
    assigned_user = relationship("User", back_populates="assigned_detections", foreign_keys=[assigned_to])


class Alert(Base):
    """Alert/Notification model"""
    __tablename__ = "alerts"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    detection_id = Column(String, ForeignKey("detections.id"))
    user_id = Column(String, ForeignKey("users.id"))
    alert_type = Column(String)  # 'email', 'sms', 'push', 'webhook'
    status = Column(String)  # 'pending', 'sent', 'failed'
    message = Column(Text)
    sent_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Error tracking
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)


class ActivityLog(Base):
    """Activity log model"""
    __tablename__ = "activity_logs"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False, index=True)

    # Action details
    action = Column(String, nullable=False, index=True)  # login, acknowledge_alert, create_camera, etc.
    resource_type = Column(String, index=True)  # alert, camera, user, etc.
    resource_id = Column(String)
    details = Column(JSON)

    # Request info
    ip_address = Column(String)
    user_agent = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="activity_logs")
    organization = relationship("Organization", back_populates="activity_logs")


class SystemLog(Base):
    """System activity log (legacy - kept for backward compatibility)"""
    __tablename__ = "system_logs"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    action = Column(String)
    resource_type = Column(String)
    resource_id = Column(String)
    details = Column(JSON)
    ip_address = Column(String)
    user_agent = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class ContactSubmission(Base):
    """Contact form submission model"""
    __tablename__ = "contact_submissions"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    company = Column(String)
    phone = Column(String)
    subject = Column(String, nullable=False)
    message = Column(Text, nullable=False)

    # Tracking & Analytics
    ip_address = Column(String, index=True)
    user_agent = Column(String)
    referrer = Column(String)

    # Status tracking
    status = Column(String, default="new")  # new, contacted, resolved, spam
    assigned_to = Column(String)
    notes = Column(Text)

    # Email notification tracking
    confirmation_email_sent = Column(Boolean, default=False)
    confirmation_email_sent_at = Column(DateTime)
    admin_email_sent = Column(Boolean, default=False)
    admin_email_sent_at = Column(DateTime)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    contacted_at = Column(DateTime)
    resolved_at = Column(DateTime)

