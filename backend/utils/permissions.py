"""
Role-based access control utilities
"""
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from database.models import User, UserRole
from core.logger import log


class PermissionChecker:
    """Permission checker for role-based access control"""
    
    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles
    
    def __call__(self, current_user: User = Depends(get_current_user)):
        """Check if user has required role"""
        if current_user.role not in self.allowed_roles:
            log.warning(f"Permission denied for user {current_user.id} with role {current_user.role}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "code": "INSUFFICIENT_PERMISSIONS",
                    "message": "You don't have permission to perform this action",
                    "required_roles": [role.value for role in self.allowed_roles],
                    "your_role": current_user.role.value
                }
            )
        return current_user


# Permission dependencies for different access levels
require_super_admin = PermissionChecker([UserRole.SUPER_ADMIN])

require_admin = PermissionChecker([
    UserRole.SUPER_ADMIN,
    UserRole.ADMIN
])

require_manager = PermissionChecker([
    UserRole.SUPER_ADMIN,
    UserRole.ADMIN,
    UserRole.MANAGER
])

require_operator = PermissionChecker([
    UserRole.SUPER_ADMIN,
    UserRole.ADMIN,
    UserRole.MANAGER,
    UserRole.OPERATOR
])

require_viewer = PermissionChecker([
    UserRole.SUPER_ADMIN,
    UserRole.ADMIN,
    UserRole.MANAGER,
    UserRole.OPERATOR,
    UserRole.VIEWER
])


def check_organization_access(user: User, organization_id: str):
    """Check if user has access to organization"""
    if user.organization_id != organization_id and user.role != UserRole.SUPER_ADMIN:
        log.warning(f"Organization access denied for user {user.id} to org {organization_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "ORGANIZATION_ACCESS_DENIED",
                "message": "You don't have access to this organization's data"
            }
        )


def check_resource_ownership(user: User, resource_owner_id: str, resource_type: str):
    """Check if user owns the resource or has admin rights"""
    if user.id != resource_owner_id and user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN]:
        log.warning(f"Resource ownership check failed for user {user.id} on {resource_type}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "RESOURCE_ACCESS_DENIED",
                "message": f"You don't have access to this {resource_type}"
            }
        )


# Import get_current_user from auth module (will be defined later)
from api.auth import get_current_user

