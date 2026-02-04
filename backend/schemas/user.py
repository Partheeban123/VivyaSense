"""
User management schemas
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserCreate(BaseModel):
    """User creation schema (admin)"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=2, max_length=100)
    phone_number: str = Field(..., pattern=r'^\+?[1-9]\d{1,14}$')
    role: str = Field(..., pattern=r'^(ADMIN|MANAGER|OPERATOR|VIEWER)$')
    department: Optional[str] = None
    employee_id: Optional[str] = None


class UserUpdateAdmin(BaseModel):
    """User update schema (admin)"""
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone_number: Optional[str] = Field(None, pattern=r'^\+?[1-9]\d{1,14}$')
    role: Optional[str] = Field(None, pattern=r'^(ADMIN|MANAGER|OPERATOR|VIEWER)$')
    department: Optional[str] = None
    employee_id: Optional[str] = None
    is_active: Optional[bool] = None


class UserListResponse(BaseModel):
    """User list item response"""
    id: str
    email: str
    username: str
    full_name: str
    phone_number: str
    role: str
    department: Optional[str]
    employee_id: Optional[str]
    is_active: bool
    last_login: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserDetailResponse(BaseModel):
    """User detail response"""
    id: str
    email: str
    username: str
    full_name: str
    phone_number: str
    organization_id: str
    role: str
    department: Optional[str]
    employee_id: Optional[str]
    profile_image: Optional[str]
    is_active: bool
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AdminPasswordReset(BaseModel):
    """Admin password reset schema"""
    new_password: str = Field(..., min_length=8)

