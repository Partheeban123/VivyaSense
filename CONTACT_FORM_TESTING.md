# Contact Form Testing Guide

## Overview
This document provides a comprehensive testing guide for the newly implemented contact form feature.

## Features Implemented

### 1. Backend API (`/api/contact`)
- ✅ Input validation (email format, required fields, length limits)
- ✅ Rate limiting (3 submissions per IP per hour)
- ✅ Database storage (PostgreSQL)
- ✅ Email notifications (user confirmation + admin notification)
- ✅ Comprehensive error handling
- ✅ Logging with loguru

### 2. Frontend UI (`/contact`)
- ✅ Real-time client-side validation
- ✅ Error message display for each field
- ✅ Rate limit warnings
- ✅ Character counter for message field
- ✅ Loading states
- ✅ Success confirmation
- ✅ Responsive design

### 3. Database
- ✅ `contact_submissions` table created
- ✅ Stores all form submissions with timestamps
- ✅ Tracks submission status

## Test Scenarios

### Test 1: Valid Submission
**Steps:**
1. Navigate to http://localhost:3000/contact
2. Fill in all required fields with valid data:
   - Name: "John Doe"
   - Email: "john@example.com"
   - Subject: "Request a Demo"
   - Message: "I would like to schedule a demo"
3. Click "Send Message"

**Expected Result:**
- ✅ Form submits successfully
- ✅ Success message displayed
- ✅ Entry saved in database
- ✅ Confirmation email sent to user
- ✅ Notification email sent to admin

### Test 2: Client-Side Validation
**Steps:**
1. Try to submit with empty required fields
2. Enter invalid email format (e.g., "notanemail")
3. Enter a name with less than 2 characters
4. Enter a message longer than 2000 characters

**Expected Result:**
- ✅ Red border appears on invalid fields
- ✅ Error messages displayed below each field
- ✅ Form does not submit until all validations pass

### Test 3: Rate Limiting
**Steps:**
1. Submit the form 3 times in quick succession
2. Try to submit a 4th time

**Expected Result:**
- ✅ First 3 submissions succeed
- ✅ 4th submission shows rate limit warning
- ✅ Submit button disabled
- ✅ Warning message shows retry time

### Test 4: Server-Side Validation
**Steps:**
1. Use browser dev tools to bypass client validation
2. Send invalid data directly to API

**Expected Result:**
- ✅ Server returns 400 Bad Request
- ✅ Detailed validation errors returned
- ✅ No data saved to database

### Test 5: Email Functionality
**Steps:**
1. Submit a valid form
2. Check email logs in backend terminal

**Expected Result:**
- ✅ Confirmation email logged for user
- ✅ Notification email logged for admin
- ✅ Emails contain correct information

### Test 6: Database Persistence
**Steps:**
1. Submit a form
2. Check database for entry:
   ```bash
   cd ai-vision-platform/backend
   python -c "from database.database import SessionLocal; from database.models import ContactSubmission; db = SessionLocal(); print(db.query(ContactSubmission).all())"
   ```

**Expected Result:**
- ✅ Entry exists in database
- ✅ All fields correctly stored
- ✅ Timestamps recorded

### Test 7: Error Handling
**Steps:**
1. Stop the backend server
2. Try to submit the form

**Expected Result:**
- ✅ Network error message displayed
- ✅ Form remains filled (data not lost)
- ✅ User can retry after server restart

## API Endpoints

### POST /api/contact
**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "company": "Acme Corp",
  "phone": "+1 (555) 123-4567",
  "subject": "Request a Demo",
  "message": "I would like to schedule a demo"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Thank you for contacting us! We'll get back to you within 24 hours.",
  "submission_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

**Rate Limit Response (429):**
```json
{
  "detail": "Too many submissions. Please try again in 45 minutes."
}
```

**Validation Error Response (400):**
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

## Configuration

### Environment Variables
Make sure these are set in `backend/.env`:
```
# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
ADMIN_EMAIL=admin@yourdomain.com
```

### Rate Limiting
- Default: 3 submissions per IP per hour
- Can be adjusted in `backend/utils/rate_limiter.py`

## Troubleshooting

### Issue: Emails not sending
**Solution:** Check SMTP credentials in `.env` file

### Issue: Rate limit not working
**Solution:** Ensure Redis is running or check in-memory rate limiter

### Issue: Database errors
**Solution:** Run migration script:
```bash
cd ai-vision-platform/backend
python -m database.create_contact_table
```

### Issue: Frontend not connecting to backend
**Solution:** Verify backend is running on port 8000 and frontend on port 3000

## Next Steps
1. Configure real SMTP credentials for production
2. Set up email templates with company branding
3. Add CAPTCHA for additional spam protection
4. Implement admin dashboard to view submissions
5. Add export functionality for submissions

