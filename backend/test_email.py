"""
Test script to verify email configuration
Run this after setting up SMTP credentials in .env
"""
from services.email_service import email_service
from core.config import settings
from loguru import logger as log


def test_email_configuration():
    """Test email configuration by sending a test email"""
    
    log.info("=" * 80)
    log.info("📧 EMAIL CONFIGURATION TEST")
    log.info("=" * 80)
    
    # Check configuration
    log.info(f"SMTP Host: {settings.SMTP_HOST}")
    log.info(f"SMTP Port: {settings.SMTP_PORT}")
    log.info(f"SMTP User: {settings.SMTP_USER or 'NOT CONFIGURED'}")
    log.info(f"SMTP Password: {'*' * len(settings.SMTP_PASSWORD) if settings.SMTP_PASSWORD else 'NOT CONFIGURED'}")
    log.info(f"From Email: {settings.EMAIL_FROM}")
    log.info(f"Admin Email: {settings.ADMIN_EMAIL}")
    log.info("=" * 80)
    
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        log.error("❌ SMTP credentials not configured!")
        log.info("Please update backend/.env with your SMTP credentials")
        log.info("See EMAIL_SETUP_GUIDE.md for instructions")
        return False
    
    # Test email address (change this to your email)
    test_email = settings.SMTP_USER  # Send to yourself
    
    log.info(f"\n📤 Sending test email to: {test_email}")

    # Send test confirmation email
    log.info("\n1️⃣ Testing user confirmation email...")
    result1 = email_service.send_contact_confirmation(
        name="Test User",
        email=test_email,
        subject="Test Demo Request",
        message="This is a test message to verify email configuration is working correctly."
    )

    if result1:
        log.info("✅ User confirmation email sent successfully!")
    else:
        log.error("❌ Failed to send user confirmation email")

    # Send test admin notification
    log.info("\n2️⃣ Testing admin notification email...")
    result2 = email_service.send_admin_notification(
        name="Test User",
        email=test_email,
        company="Test Company",
        phone="+1 (555) 123-4567",
        subject="Test Demo Request",
        message="This is a test message to verify email configuration is working correctly.",
        submission_id="test-12345",
        ip_address="127.0.0.1"
    )
    
    if result2:
        log.info("✅ Admin notification email sent successfully!")
    else:
        log.error("❌ Failed to send admin notification email")
    
    # Summary
    log.info("\n" + "=" * 80)
    log.info("📊 TEST SUMMARY")
    log.info("=" * 80)
    log.info(f"User Confirmation Email: {'✅ SUCCESS' if result1 else '❌ FAILED'}")
    log.info(f"Admin Notification Email: {'✅ SUCCESS' if result2 else '❌ FAILED'}")
    
    if result1 and result2:
        log.info("\n🎉 All tests passed! Email configuration is working correctly.")
        log.info(f"📬 Check your inbox at: {test_email}")
        return True
    else:
        log.error("\n❌ Some tests failed. Please check your SMTP configuration.")
        log.info("See EMAIL_SETUP_GUIDE.md for troubleshooting tips")
        return False


if __name__ == "__main__":
    log.info("Starting email configuration test...\n")
    success = test_email_configuration()

    if success:
        log.info("\n✅ Email system is ready to use!")
    else:
        log.error("\n❌ Email system needs configuration")

