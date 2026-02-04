"""
Authentication API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from core.config import settings
from core.logger import log
from database.database import get_db
from database import models
from database.models import UserRole
from schemas.auth import (
    UserRegister, UserLogin, Token, TokenRefresh, TokenVerifyResponse,
    PasswordChange, PasswordResetRequest, PasswordReset, UserUpdate, UserResponse
)
from schemas.common import SuccessResponse, ErrorResponse, ErrorDetail, MessageResponse
from schemas.organization import OrganizationResponse
from schemas.preferences import UserPreferencesResponse
from utils.password import hash_password, verify_password, validate_password_strength
from utils.activity_logger import log_activity

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Token expiration settings
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour
REFRESH_TOKEN_EXPIRE_DAYS = 7  # 7 days


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    """Create JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        token_type: str = payload.get("type")

        if username is None or token_type != "access":
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # Fetch user from database
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    return user


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user and create organization"""
    try:
        log.info(f"User registration attempt: {user_data.email}")

        # Check if user already exists
        existing_user = db.query(models.User).filter(
            (models.User.email == user_data.email) | (models.User.username == user_data.username)
        ).first()

        if existing_user:
            if existing_user.email == user_data.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )

        # Check if organization already exists
        existing_org = db.query(models.Organization).filter(
            models.Organization.name == user_data.organization_name
        ).first()

        if existing_org:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Organization name already taken"
            )

        # Hash password
        hashed_password = hash_password(user_data.password)

        # Create organization first
        organization = models.Organization(
            name=user_data.organization_name,
            subscription_plan=models.SubscriptionPlan.FREE,
            max_cameras=5,
            max_users=10,
            features=[],
            is_active=True
        )
        db.add(organization)
        db.flush()  # Get organization ID

        # Create new user as ADMIN of the organization
        db_user = models.User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            phone_number=user_data.phone_number,
            organization_id=organization.id,
            role=UserRole.ADMIN,  # First user is admin
            department=user_data.department,
            employee_id=user_data.employee_id,
            is_active=True,
            is_superuser=False
        )
        db.add(db_user)
        db.flush()  # Get user ID

        # Update organization admin
        organization.admin_user_id = db_user.id

        # Create default user preferences
        preferences = models.UserPreferences(
            user_id=db_user.id,
            notification_push_enabled=True,
            notification_email_enabled=True,
            notification_sms_enabled=True,
            alert_types=["FALL", "FIRE", "SMOKE", "PPE"],
            minimum_confidence=0.5,
            language="en",
            timezone="UTC",
            theme="light",
            default_view="dashboard"
        )
        db.add(preferences)

        db.commit()
        db.refresh(db_user)
        db.refresh(organization)

        log.info(f"User and organization registered successfully: {user_data.email}")

        return SuccessResponse(
            data={
                "user": UserResponse.from_orm(db_user),
                "organization": OrganizationResponse.from_orm(organization)
            },
            message="Registration successful"
        )

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Registration error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    request: Request = None,
    db: Session = Depends(get_db)
):
    """Login and get access token with refresh token"""
    try:
        log.info(f"Login attempt: {form_data.username}")

        # Find user by username or email
        user = db.query(models.User).filter(
            (models.User.username == form_data.username) | (models.User.email == form_data.username)
        ).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verify password
        if not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )

        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()

        # Create tokens
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "user_id": user.id},
            expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(
            data={"sub": user.username, "user_id": user.id}
        )

        # Get organization
        organization = db.query(models.Organization).filter(
            models.Organization.id == user.organization_id
        ).first()

        # Log activity
        log_activity(
            db=db,
            user=user,
            action="login",
            details={"method": "password"},
            request=request
        )

        log.info(f"User logged in successfully: {user.username}")

        return SuccessResponse(
            data={
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "full_name": user.full_name,
                    "role": user.role.value,
                    "organization": {
                        "id": organization.id,
                        "name": organization.name,
                        "subscription_plan": organization.subscription_plan.value
                    } if organization else None
                }
            },
            message="Login successful"
        )

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )




@router.post("/login/json")
async def login_json(
    login_data: UserLogin,
    request: Request = None,
    db: Session = Depends(get_db)
):
    """Login with JSON payload (for mobile apps)"""
    try:
        log.info(f"JSON login attempt: {login_data.username}")

        # Find user by username or email
        user = db.query(models.User).filter(
            (models.User.username == login_data.username) | (models.User.email == login_data.username)
        ).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verify password
        if not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )

        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()

        # Create tokens
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.id, "email": user.email},
            expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(data={"sub": user.id})

        # Log activity
        activity_log = models.ActivityLog(
            user_id=user.id,
            organization_id=user.organization_id,
            action="login",
            resource_type="auth",
            details={"method": "json", "username": login_data.username},
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("user-agent") if request else None
        )
        db.add(activity_log)
        db.commit()

        log.info(f"JSON login successful: {user.email}")

        return {
            "success": True,
            "data": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                "user": UserResponse.from_orm(user)
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"JSON login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.get("/me")
async def get_me(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user profile with organization and preferences"""
    try:
        # Get organization
        organization = db.query(models.Organization).filter(
            models.Organization.id == current_user.organization_id
        ).first()

        # Get preferences
        preferences = db.query(models.UserPreferences).filter(
            models.UserPreferences.user_id == current_user.id
        ).first()

        return SuccessResponse(
            data={
                "user": UserResponse.from_orm(current_user),
                "organization": OrganizationResponse.from_orm(organization) if organization else None,
                "preferences": UserPreferencesResponse.from_orm(preferences) if preferences else None
            },
            message="User profile retrieved successfully"
        )

    except Exception as e:
        log.error(f"Get user profile error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user profile"
        )


@router.put("/me")
async def update_me(
    user_update: UserUpdate,
    current_user: models.User = Depends(get_current_user),
    request: Request = None,
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    try:
        # Update user fields
        if user_update.full_name is not None:
            current_user.full_name = user_update.full_name

        if user_update.phone_number is not None:
            current_user.phone_number = user_update.phone_number

        if user_update.profile_image is not None:
            current_user.profile_image = user_update.profile_image

        if user_update.department is not None:
            current_user.department = user_update.department

        current_user.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(current_user)

        # Log activity
        log_activity(
            db=db,
            user=current_user,
            action="update_profile",
            resource_type="user",
            resource_id=current_user.id,
            details=user_update.dict(exclude_none=True),
            request=request
        )

        log.info(f"User profile updated: {current_user.id}")

        return SuccessResponse(
            data=UserResponse.from_orm(current_user),
            message="Profile updated successfully"
        )

    except Exception as e:
        log.error(f"Update profile error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )


@router.post("/logout")
async def logout(
    current_user: models.User = Depends(get_current_user),
    request: Request = None,
    db: Session = Depends(get_db)
):
    """Logout user"""
    try:
        # Log activity
        log_activity(
            db=db,
            user=current_user,
            action="logout",
            request=request
        )

        # In production, invalidate token (add to blacklist)
        return MessageResponse(message="Successfully logged out")

    except Exception as e:
        log.error(f"Logout error: {e}")
        return MessageResponse(message="Logout completed")



@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: models.User = Depends(get_current_user),
    request: Request = None,
    db: Session = Depends(get_db)
):
    """Change user password"""
    try:
        # Verify old password
        if not verify_password(password_data.old_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect current password"
            )

        # Validate new password strength
        is_valid, error_msg = validate_password_strength(password_data.new_password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )

        # Hash and update password
        current_user.hashed_password = hash_password(password_data.new_password)
        current_user.updated_at = datetime.utcnow()

        db.commit()

        # Log activity
        log_activity(
            db=db,
            user=current_user,
            action="change_password",
            resource_type="user",
            resource_id=current_user.id,
            request=request
        )

        log.info(f"Password changed for user: {current_user.id}")

        return MessageResponse(message="Password changed successfully")

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Change password error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to change password"
        )


@router.post("/refresh")
async def refresh_token(
    token_data: TokenRefresh,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token"""
    try:
        # Decode refresh token
        payload = jwt.decode(token_data.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        token_type: str = payload.get("type")

        if username is None or token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        # Get user
        user = db.query(models.User).filter(models.User.username == username).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        # Create new access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "user_id": user.id},
            expires_delta=access_token_expires
        )

        log.info(f"Token refreshed for user: {user.username}")

        return SuccessResponse(
            data={
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
            },
            message="Token refreshed successfully"
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to refresh token"
        )


@router.get("/verify-token")
async def verify_token(
    current_user: models.User = Depends(get_current_user),
    token: str = Depends(oauth2_scheme)
):
    """Verify if token is valid"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        exp = payload.get("exp")
        expires_at = datetime.fromtimestamp(exp) if exp else None

        return SuccessResponse(
            data=TokenVerifyResponse(
                valid=True,
                user_id=current_user.id,
                expires_at=expires_at
            ),
            message="Token is valid"
        )

    except Exception as e:
        log.error(f"Token verification error: {e}")
        return SuccessResponse(
            data=TokenVerifyResponse(valid=False),
            message="Token is invalid"
        )


@router.post("/forgot-password")
async def forgot_password(
    request_data: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """Request password reset (send email with reset token)"""
    try:
        # Find user by email
        user = db.query(models.User).filter(models.User.email == request_data.email).first()

        # Always return success to prevent email enumeration
        if not user:
            log.warning(f"Password reset requested for non-existent email: {request_data.email}")
            return MessageResponse(
                message="If the email exists, a password reset link has been sent"
            )

        # Create password reset token (valid for 1 hour)
        reset_token_expires = timedelta(hours=1)
        reset_token = create_access_token(
            data={"sub": user.username, "user_id": user.id, "purpose": "password_reset"},
            expires_delta=reset_token_expires
        )

        # TODO: Send email with reset token
        # For now, just log it (in production, use email service)
        log.info(f"Password reset token for {user.email}: {reset_token}")

        # In production, you would send an email like:
        # reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
        # send_email(user.email, "Password Reset", f"Click here to reset: {reset_link}")

        return MessageResponse(
            message="If the email exists, a password reset link has been sent"
        )

    except Exception as e:
        log.error(f"Forgot password error: {e}")
        return MessageResponse(
            message="If the email exists, a password reset link has been sent"
        )


@router.post("/reset-password")
async def reset_password(
    reset_data: PasswordReset,
    db: Session = Depends(get_db)
):
    """Reset password using reset token"""
    try:
        # Decode reset token
        payload = jwt.decode(reset_data.token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        purpose: str = payload.get("purpose")

        if username is None or purpose != "password_reset":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )

        # Get user
        user = db.query(models.User).filter(models.User.username == username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )

        # Validate new password strength
        is_valid, error_msg = validate_password_strength(reset_data.new_password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )

        # Hash and update password
        user.hashed_password = hash_password(reset_data.new_password)
        user.updated_at = datetime.utcnow()

        db.commit()

        log.info(f"Password reset successful for user: {user.id}")

        return MessageResponse(message="Password reset successfully")

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Reset password error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reset password"
        )


