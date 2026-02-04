"""
Common schemas for API responses
"""
from typing import Any, Optional, Dict, List
from pydantic import BaseModel


class SuccessResponse(BaseModel):
    """Standard success response"""
    success: bool = True
    data: Any
    message: str = "Operation successful"


class ErrorDetail(BaseModel):
    """Error detail"""
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Standard error response"""
    success: bool = False
    error: ErrorDetail


class PaginationMeta(BaseModel):
    """Pagination metadata"""
    page: int
    limit: int
    total: int
    pages: int


class PaginatedResponse(BaseModel):
    """Paginated response"""
    success: bool = True
    data: List[Any]
    pagination: PaginationMeta


class MessageResponse(BaseModel):
    """Simple message response"""
    message: str
    success: bool = True

