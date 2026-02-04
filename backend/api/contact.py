"""
Contact form API endpoint with validation, rate limiting, and email notifications
"""
from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from loguru import logger as log
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from database.database import get_db, SessionLocal
from database.models import ContactSubmission
from services.email_service import email_service
from utils.rate_limiter import rate_limiter

router = APIRouter()


class ContactFormData(BaseModel):
    """Contact form submission model with validation"""
    name: str = Field(..., min_length=2, max_length=100, description="Full name")
    email: EmailStr = Field(..., description="Valid email address")
    company: Optional[str] = Field(None, max_length=100, description="Company name")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    subject: str = Field(..., min_length=5, max_length=200, description="Subject")
    message: str = Field(..., min_length=10, max_length=2000, description="Message")

    @validator('name')
    def validate_name(cls, v):
        """Validate name contains only letters, spaces, and common punctuation"""
        if not v.strip():
            raise ValueError("Name cannot be empty")
        # Allow letters, spaces, hyphens, apostrophes
        if not all(c.isalpha() or c.isspace() or c in "'-." for c in v):
            raise ValueError("Name contains invalid characters")
        return v.strip()

    @validator('phone')
    def validate_phone(cls, v):
        """Validate phone number format"""
        if v is None:
            return v
        # Remove common formatting characters
        cleaned = ''.join(c for c in v if c.isdigit() or c in '+()-. ')
        if len(cleaned.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('+', '').replace('.', '')) < 10:
            raise ValueError("Phone number must be at least 10 digits")
        return v.strip()

    @validator('message')
    def validate_message(cls, v):
        """Validate message is not spam"""
        if not v.strip():
            raise ValueError("Message cannot be empty")

        # Basic spam detection
        spam_keywords = ['viagra', 'casino', 'lottery', 'prize', 'click here', 'buy now']
        message_lower = v.lower()
        if any(keyword in message_lower for keyword in spam_keywords):
            raise ValueError("Message appears to be spam")

        return v.strip()


def get_client_ip(request: Request) -> str:
    """Extract client IP address from request"""
    # Check for forwarded IP (behind proxy/load balancer)
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()

    # Check for real IP header
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip

    # Fall back to direct client IP
    return request.client.host if request.client else "unknown"


@router.post("/contact")
async def submit_contact_form(
    form_data: ContactFormData,
    request: Request
):
    """
    Handle contact form submissions with validation, rate limiting, and notifications

    Features:
    - Input validation and sanitization
    - Rate limiting (3 submissions per IP per hour)
    - Database storage
    - Email notifications (user confirmation + admin alert)
    - Analytics tracking
    - Spam detection

    Args:
        form_data: Contact form data
        request: FastAPI request object
        db: Database session (optional, will create if not provided)

    Returns:
        dict: Success response with submission details

    Raises:
        HTTPException: For validation errors, rate limiting, or server errors
    """
    # Get client IP address
    ip_address = get_client_ip(request)
    user_agent = request.headers.get("User-Agent", "unknown")
    referrer = request.headers.get("Referer", "unknown")

    log.info("🔔 Contact form endpoint called!")
    log.info(f"IP: {ip_address}, User-Agent: {user_agent[:50]}...")

    try:
        # 1. RATE LIMITING - Check if IP has exceeded rate limit
        is_limited, seconds_until_reset = rate_limiter.is_rate_limited(
            ip_address,
            max_requests=3,
            time_window=timedelta(hours=1)
        )

        if is_limited:
            log.warning(f"⚠️ Rate limit exceeded for IP {ip_address}")
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "rate_limit_exceeded",
                    "message": f"Too many submissions. Please try again in {seconds_until_reset // 60} minutes.",
                    "retry_after": seconds_until_reset
                }
            )

        # 2. LOG SUBMISSION
        log.info("=" * 80)
        log.info("📧 NEW CONTACT FORM SUBMISSION")
        log.info("=" * 80)
        log.info(f"Name:     {form_data.name}")
        log.info(f"Email:    {form_data.email}")
        log.info(f"Company:  {form_data.company or 'N/A'}")
        log.info(f"Phone:    {form_data.phone or 'N/A'}")
        log.info(f"Subject:  {form_data.subject}")
        log.info(f"Message:  {form_data.message[:100]}...")
        log.info(f"IP:       {ip_address}")
        log.info(f"Time:     {datetime.now().isoformat()}")
        log.info("=" * 80)

        # 3. SAVE TO DATABASE
        submission_id = None
        db = SessionLocal()

        try:
            submission = ContactSubmission(
                name=form_data.name,
                email=form_data.email,
                company=form_data.company,
                phone=form_data.phone,
                subject=form_data.subject,
                message=form_data.message,
                ip_address=ip_address,
                user_agent=user_agent,
                referrer=referrer,
                status="new"
            )

            db.add(submission)
            db.commit()
            db.refresh(submission)

            submission_id = submission.id
            log.info(f"✅ Saved to database with ID: {submission_id}")

        except Exception as db_error:
            log.error(f"❌ Database error: {str(db_error)}")
            db.rollback()
            # Continue even if database fails - don't block the submission
            submission_id = f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        finally:
            db.close()

        # 4. SEND EMAIL NOTIFICATIONS
        # Send confirmation email to user
        try:
            user_email_sent = email_service.send_contact_confirmation(
                name=form_data.name,
                email=form_data.email,
                subject=form_data.subject,
                message=form_data.message
            )

            if user_email_sent:
                log.info(f"✅ Confirmation email sent to {form_data.email}")
            else:
                log.warning(f"⚠️ Failed to send confirmation email to {form_data.email}")

        except Exception as email_error:
            log.error(f"❌ Error sending confirmation email: {str(email_error)}")

        # Send notification email to admin
        try:
            admin_email_sent = email_service.send_admin_notification(
                name=form_data.name,
                email=form_data.email,
                company=form_data.company,
                phone=form_data.phone,
                subject=form_data.subject,
                message=form_data.message,
                submission_id=submission_id,
                ip_address=ip_address
            )

            if admin_email_sent:
                log.info("✅ Admin notification email sent")
            else:
                log.warning("⚠️ Failed to send admin notification email")

        except Exception as email_error:
            log.error(f"❌ Error sending admin notification: {str(email_error)}")

        # 5. RECORD REQUEST FOR RATE LIMITING
        rate_limiter.record_request(ip_address)

        # 6. ANALYTICS TRACKING
        log.info(f"📊 Analytics: Contact form submission from {ip_address}")
        log.info(f"📊 Subject category: {form_data.subject}")
        log.info(f"📊 Has company: {bool(form_data.company)}")
        log.info(f"📊 Has phone: {bool(form_data.phone)}")

        # 7. RETURN SUCCESS RESPONSE
        return {
            "success": True,
            "message": "Thank you for contacting us! We'll get back to you within 24 hours.",
            "submission_id": submission_id,
            "data": {
                "name": form_data.name,
                "email": form_data.email,
                "subject": form_data.subject
            },
            "notifications": {
                "confirmation_email_sent": user_email_sent if 'user_email_sent' in locals() else False,
                "admin_notification_sent": admin_email_sent if 'admin_email_sent' in locals() else False
            }
        }

    except HTTPException:
        # Re-raise HTTP exceptions (validation errors, rate limiting)
        raise

    except ValueError as ve:
        # Validation errors from Pydantic validators
        log.error(f"❌ Validation error: {str(ve)}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": "validation_error",
                "message": str(ve)
            }
        )

    except Exception as e:
        # Unexpected errors
        log.error(f"❌ Unexpected error processing contact form: {str(e)}")
        log.exception(e)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "server_error",
                "message": "An unexpected error occurred. Please try again later."
            }
        )


@router.get("/contact/test")
async def test_contact_endpoint():
    """Test endpoint to verify contact API is working"""
    return {
        "status": "ok",
        "message": "Contact API is working",
        "timestamp": datetime.now().isoformat(),
        "features": {
            "validation": "enabled",
            "rate_limiting": "enabled (3 per hour)",
            "email_notifications": "enabled",
            "database_storage": "enabled",
            "spam_detection": "enabled"
        }
    }


@router.get("/contact/stats")
async def get_contact_stats(request: Request):
    """
    Get contact form statistics for the current IP

    Returns rate limit status and submission count
    """
    ip_address = get_client_ip(request)

    request_count = rate_limiter.get_request_count(
        ip_address,
        time_window=timedelta(hours=1)
    )

    is_limited, seconds_until_reset = rate_limiter.is_rate_limited(
        ip_address,
        max_requests=3,
        time_window=timedelta(hours=1)
    )

    return {
        "ip_address": ip_address,
        "submissions_last_hour": request_count,
        "max_submissions_per_hour": 3,
        "is_rate_limited": is_limited,
        "seconds_until_reset": seconds_until_reset,
        "can_submit": not is_limited
    }

