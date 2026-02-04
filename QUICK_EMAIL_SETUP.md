# 📧 Quick Email Setup (5 Minutes)

## Current Status
✅ Contact form is working  
❌ Emails are not being sent (SMTP not configured)

## 🚀 Quick Setup with Gmail

### Step 1: Get Gmail App Password (2 minutes)

1. **Enable 2-Factor Authentication** (if not already enabled)
   - Go to: https://myaccount.google.com/security
   - Enable "2-Step Verification"

2. **Generate App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Select: **Mail** → **Other (Custom name)**
   - Name it: "AI Vision Platform"
   - Click **Generate**
   - Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)

### Step 2: Update Configuration (1 minute)

Edit `backend/.env` file and replace these lines:

```env
SMTP_USER=your-actual-email@gmail.com
SMTP_PASSWORD=abcdefghijklmnop
ADMIN_EMAIL=your-actual-email@gmail.com
```

**Important:** Remove spaces from the app password!

### Step 3: Test Email (1 minute)

```bash
cd ai-vision-platform/backend
source venv/bin/activate
python test_email.py
```

You should see:
```
✅ User confirmation email sent successfully!
✅ Admin notification email sent successfully!
🎉 All tests passed!
```

### Step 4: Restart Backend (1 minute)

```bash
# Kill existing backend
lsof -ti :8000 | xargs kill -9

# Start backend
python main.py
```

### Step 5: Test Contact Form

1. Go to: http://localhost:3000/contact
2. Fill out and submit the form
3. Check your email inbox! 📬

---

## ✅ Success Indicators

After setup, you should see in backend logs:
```
✅ Confirmation email sent to user@example.com
✅ Admin notification sent to admin@vivyasense.com
```

Instead of:
```
⚠️ SMTP not configured. Email not sent.
```

---

## 🔧 Troubleshooting

### "Authentication failed"
- Make sure you're using the **App Password**, not your regular Gmail password
- Remove all spaces from the app password
- Verify 2FA is enabled on your Google account

### "Connection refused"
- Check your internet connection
- Try port 465 instead of 587 in `.env`:
  ```env
  SMTP_PORT=465
  ```

### Still not working?
See detailed guide: `EMAIL_SETUP_GUIDE.md`

---

## 📝 What You'll Receive

### User Confirmation Email
- Sent to: Person who submitted the form
- Subject: "Thank you for contacting Vivya Sense"
- Contains: Submission confirmation and details

### Admin Notification Email
- Sent to: Your admin email
- Subject: "🔔 New Contact Form Submission: [Subject]"
- Contains: All form details and metadata

---

## 🎯 Production Recommendations

For production, consider using:
- **SendGrid** (100 free emails/day)
- **Mailgun** (5,000 free emails/month)
- **AWS SES** (very cheap, scalable)

See `EMAIL_SETUP_GUIDE.md` for details.

---

## 📊 Current Configuration

Your `.env` file has been updated with placeholders.

**Files Updated:**
- ✅ `backend/.env` - Email configuration added
- ✅ `backend/core/config.py` - Email settings added
- ✅ `backend/test_email.py` - Test script created
- ✅ `EMAIL_SETUP_GUIDE.md` - Detailed guide
- ✅ `QUICK_EMAIL_SETUP.md` - This quick guide

**Next Step:** Follow the 5-minute setup above! 🚀

