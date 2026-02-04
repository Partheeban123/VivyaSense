# Email Setup Guide for Contact Form

## 🚨 Current Status
Your contact form is working perfectly, but emails are not being sent because SMTP is not configured.

## 📧 Quick Setup Options

### Option 1: Gmail SMTP (Easiest for Testing)

#### Step 1: Enable 2-Factor Authentication
1. Go to your Google Account: https://myaccount.google.com
2. Navigate to **Security**
3. Enable **2-Step Verification** if not already enabled

#### Step 2: Generate App Password
1. Go to: https://myaccount.google.com/apppasswords
2. Select **Mail** and **Other (Custom name)**
3. Enter "AI Vision Platform" as the name
4. Click **Generate**
5. Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)

#### Step 3: Update .env File
Edit `backend/.env` and replace these values:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-actual-email@gmail.com
SMTP_PASSWORD=abcdefghijklmnop  # Remove spaces from app password
ADMIN_EMAIL=your-actual-email@gmail.com
FROM_EMAIL=your-actual-email@gmail.com
FROM_NAME=Vivya Sense Team
```

#### Step 4: Restart Backend
```bash
# Kill existing backend
lsof -ti :8000 | xargs kill -9

# Start backend
cd ai-vision-platform/backend
source venv/bin/activate
python main.py
```

#### Step 5: Test
Submit the contact form again and check your email!

---

### Option 2: SendGrid (Recommended for Production)

SendGrid offers 100 free emails per day.

#### Step 1: Create SendGrid Account
1. Sign up at: https://signup.sendgrid.com/
2. Verify your email
3. Create an API key

#### Step 2: Update .env File
```env
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your-sendgrid-api-key
ADMIN_EMAIL=admin@vivyasense.com
FROM_EMAIL=noreply@vivyasense.com
FROM_NAME=Vivya Sense Team
```

---

### Option 3: Mailgun (Alternative)

Mailgun offers 5,000 free emails per month.

#### Step 1: Create Mailgun Account
1. Sign up at: https://signup.mailgun.com/
2. Verify your domain or use sandbox domain
3. Get SMTP credentials

#### Step 2: Update .env File
```env
SMTP_HOST=smtp.mailgun.org
SMTP_PORT=587
SMTP_USER=postmaster@your-domain.mailgun.org
SMTP_PASSWORD=your-mailgun-password
ADMIN_EMAIL=admin@vivyasense.com
FROM_EMAIL=noreply@vivyasense.com
FROM_NAME=Vivya Sense Team
```

---

### Option 4: AWS SES (For Production Scale)

AWS SES is very cost-effective for high volume.

#### Step 1: Set up AWS SES
1. Go to AWS Console → SES
2. Verify your domain or email
3. Create SMTP credentials

#### Step 2: Update .env File
```env
SMTP_HOST=email-smtp.us-east-1.amazonaws.com
SMTP_PORT=587
SMTP_USER=your-aws-smtp-username
SMTP_PASSWORD=your-aws-smtp-password
ADMIN_EMAIL=admin@vivyasense.com
FROM_EMAIL=noreply@vivyasense.com
FROM_NAME=Vivya Sense Team
```

---

## 🧪 Testing Email Configuration

After configuring SMTP, test with this command:

```bash
cd ai-vision-platform/backend
python -c "
from services.email_service import email_service
import asyncio

async def test():
    result = await email_service.send_confirmation_email(
        to_email='your-email@example.com',
        name='Test User',
        subject='Test Subject',
        message='Test message'
    )
    print('Email sent!' if result else 'Email failed!')

asyncio.run(test())
"
```

---

## 📊 What Emails Are Sent?

### 1. User Confirmation Email
**To:** User who submitted the form  
**Subject:** "Thank you for contacting Vivya Sense"  
**Content:**
- Confirmation of submission
- Summary of their inquiry
- Expected response time (24 hours)

### 2. Admin Notification Email
**To:** Admin email (configured in .env)  
**Subject:** "🔔 New Contact Form Submission: [Subject]"  
**Content:**
- All form details (name, email, company, phone, message)
- Submission metadata (IP, timestamp)
- Quick action links

---

## 🔧 Troubleshooting

### Issue: "Authentication failed"
**Solution:** 
- For Gmail: Make sure you're using an App Password, not your regular password
- Check that 2FA is enabled on your Google account

### Issue: "Connection refused"
**Solution:**
- Check firewall settings
- Verify SMTP_HOST and SMTP_PORT are correct
- Try port 465 with SSL instead of 587 with TLS

### Issue: "Emails going to spam"
**Solution:**
- Use a verified domain
- Set up SPF, DKIM, and DMARC records
- Use a professional email service (SendGrid, Mailgun, AWS SES)

### Issue: "Rate limiting"
**Solution:**
- Gmail: Limited to ~500 emails/day
- Use SendGrid or Mailgun for higher volume

---

## 🎯 Recommended Setup

**For Development/Testing:**
- ✅ Gmail SMTP (free, easy setup)

**For Production:**
- ✅ SendGrid (100 free/day, then paid)
- ✅ Mailgun (5,000 free/month)
- ✅ AWS SES (very cheap, scalable)

---

## 📝 Current Configuration

Your `.env` file has been updated with Gmail SMTP placeholders.

**Next Steps:**
1. Choose an email provider (Gmail recommended for testing)
2. Get SMTP credentials
3. Update `backend/.env` with real credentials
4. Restart backend server
5. Test the contact form!

---

## ✅ Verification

After setup, you should see in the logs:
```
✅ Confirmation email sent to user@example.com
✅ Admin notification sent to admin@vivyasense.com
```

Instead of:
```
⚠️ SMTP not configured. Email not sent.
```

