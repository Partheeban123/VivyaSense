"""
Email service for sending notifications
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from datetime import datetime
from loguru import logger as log
from core.config import settings


class EmailService:
    """Service for sending emails"""
    
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.email_from = settings.EMAIL_FROM
    
    def _send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """
        Send an email using SMTP
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML content of the email
            text_content: Plain text content (fallback)
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        # Skip if SMTP is not configured
        if not self.smtp_user or not self.smtp_password:
            log.warning("SMTP not configured. Email not sent.")
            log.info(f"Would have sent email to {to_email}: {subject}")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email_from
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add text and HTML parts
            if text_content:
                part1 = MIMEText(text_content, 'plain')
                msg.attach(part1)
            
            part2 = MIMEText(html_content, 'html')
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            log.info(f"✅ Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            log.error(f"❌ Failed to send email to {to_email}: {str(e)}")
            return False
    
    def send_contact_confirmation(
        self,
        name: str,
        email: str,
        subject: str,
        message: str
    ) -> bool:
        """
        Send confirmation email to user who submitted contact form
        
        Args:
            name: User's name
            email: User's email
            subject: Contact form subject
            message: Contact form message
        
        Returns:
            bool: True if email sent successfully
        """
        email_subject = "Thank you for contacting Vivya Sense"
        current_year = datetime.now().year

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Thank You for Reaching Out!</h1>
                </div>
                <div class="content">
                    <p>Hi <strong>{name}</strong>,</p>
                    <p>Thank you for contacting <strong>Vivya Sense</strong>! We've received your message and our team will get back to you within 24 hours.</p>
                    
                    <h3>Your Message Details:</h3>
                    <p><strong>Subject:</strong> {subject}</p>
                    <p><strong>Message:</strong><br>{message}</p>
                    
                    <p>If you have any urgent questions, feel free to call us at <strong>+1 (555) 123-4567</strong>.</p>
                    
                    <a href="https://vivyasense.com" class="button">Visit Our Website</a>
                </div>
                <div class="footer">
                    <p>© {current_year} Vivya Sense - AI-Powered Safety Solutions</p>
                    <p>This is an automated message. Please do not reply to this email.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Hi {name},
        
        Thank you for contacting Vivya Sense! We've received your message and our team will get back to you within 24 hours.
        
        Your Message Details:
        Subject: {subject}
        Message: {message}

        If you have any urgent questions, feel free to call us at +1 (555) 123-4567.

        © {current_year} Vivya Sense - AI-Powered Safety Solutions
        """
        
        return self._send_email(email, email_subject, html_content, text_content)

    def send_admin_notification(
        self,
        name: str,
        email: str,
        company: Optional[str],
        phone: Optional[str],
        subject: str,
        message: str,
        submission_id: str,
        ip_address: Optional[str] = None
    ) -> bool:
        """
        Send notification email to admin about new contact form submission

        Args:
            name: User's name
            email: User's email
            company: User's company
            phone: User's phone
            subject: Contact form subject
            message: Contact form message
            submission_id: Unique submission ID
            ip_address: User's IP address

        Returns:
            bool: True if email sent successfully
        """
        # Use SMTP_USER as admin email or a default admin email
        admin_email = settings.SMTP_USER or "admin@vivyasense.com"
        current_year = datetime.now().year

        email_subject = f"🔔 New Contact Form Submission: {subject}"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 700px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #2c3e50; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .info-box {{ background: white; padding: 15px; margin: 10px 0; border-left: 4px solid #667eea; }}
                .label {{ font-weight: bold; color: #667eea; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>🔔 New Contact Form Submission</h2>
                </div>
                <div class="content">
                    <div class="info-box">
                        <p><span class="label">Submission ID:</span> {submission_id}</p>
                        <p><span class="label">Name:</span> {name}</p>
                        <p><span class="label">Email:</span> <a href="mailto:{email}">{email}</a></p>
                        <p><span class="label">Company:</span> {company or 'N/A'}</p>
                        <p><span class="label">Phone:</span> {phone or 'N/A'}</p>
                        <p><span class="label">IP Address:</span> {ip_address or 'N/A'}</p>
                    </div>

                    <div class="info-box">
                        <p><span class="label">Subject:</span> {subject}</p>
                        <p><span class="label">Message:</span></p>
                        <p>{message}</p>
                    </div>

                    <p style="margin-top: 20px; color: #e74c3c;">
                        <strong>⚠️ Action Required:</strong> Please respond to this inquiry within 24 hours.
                    </p>
                </div>
                <div class="footer">
                    <p>© {current_year} Vivya Sense - Contact Form Notification</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        New Contact Form Submission

        Submission ID: {submission_id}
        Name: {name}
        Email: {email}
        Company: {company or 'N/A'}
        Phone: {phone or 'N/A'}
        IP Address: {ip_address or 'N/A'}

        Subject: {subject}
        Message: {message}

        Action Required: Please respond to this inquiry within 24 hours.
        """

        return self._send_email(admin_email, email_subject, html_content, text_content)


# Global email service instance
email_service = EmailService()

