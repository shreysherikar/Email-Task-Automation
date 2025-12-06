# 📧 Gmail Integration - Complete Setup Guide

## 100% FREE Gmail Integration

This guide will help you connect your Gmail account to automatically extract tasks from emails.

**What you get:**
- ✅ Completely FREE (no paid services)
- ✅ Automatic email monitoring
- ✅ Works with any Gmail account
- ✅ Checks for new emails every minute
- ✅ Processes emails in real-time

---

## 🚀 Quick Setup (5 Minutes)

### Step 1: Enable Gmail IMAP Access (1 minute)

1. Go to Gmail Settings: https://mail.google.com/mail/u/0/#settings/fwdandpop
2. Click on **"Forwarding and POP/IMAP"** tab
3. Under **"IMAP access"**, select **"Enable IMAP"**
4. Click **"Save Changes"**

✅ Done! IMAP is now enabled.

---

### Step 2: Create Gmail App Password (2 minutes)

**Important**: You need an "App Password" (not your regular Gmail password) for security.

1. **Go to Google Account Security**: https://myaccount.google.com/security

2. **Enable 2-Step Verification** (if not already enabled):
   - Click "2-Step Verification"
   - Follow the setup wizard
   - This is required for App Passwords

3. **Create App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Or: Security → 2-Step Verification → App passwords
   - Select app: **"Mail"**
   - Select device: **"Windows Computer"** (or your device)
   - Click **"Generate"**

4. **Copy the 16-character password**:
   - It looks like: `abcd efgh ijkl mnop`
   - Save it somewhere safe!

✅ You now have your App Password!

---

### Step 3: Configure the Integration (1 minute)

1. **Open your `.env` file** in the project folder

2. **Add these lines**:
   ```env
   GMAIL_USER=your.email@gmail.com
   GMAIL_APP_PASSWORD=abcdefghijklmnop
   ```

3. **Replace with your details**:
   - `GMAIL_USER`: Your full Gmail address
   - `GMAIL_APP_PASSWORD`: The 16-character password (remove spaces)

**Example `.env` file:**
```env
# Gmail Configuration
GMAIL_USER=john.doe@gmail.com
GMAIL_APP_PASSWORD=abcdefghijklmnop

# API Configuration
API_URL=http://localhost:8000/ingest-email
CHECK_INTERVAL=60
```

✅ Configuration complete!

---

### Step 4: Run the Integration (1 minute)

1. **Make sure Flask server is running**:
   ```bash
   python app.py
   ```

2. **In a NEW terminal, run the Gmail integration**:
   ```bash
   python gmail_integration.py
   ```

3. **You should see**:
   ```
   ✓ Connected to Gmail successfully!
   ✓ Monitoring Gmail for new emails...
   ```

✅ Integration is running!

---

## 🧪 Test It!

### Send yourself a test email:

1. **From any email account**, send an email to your Gmail:
   ```
   To: your.email@gmail.com
   Subject: TODO: Test task extraction
   Body: Please complete the project report by Friday and review the presentation slides.
   ```

2. **Watch the terminal** - you should see:
   ```
   📧 Processing: TODO: Test task extraction...
      From: sender@example.com
     ✓ Processed: 2 tasks added, 0 duplicates
   ```

3. **Check your dashboard**: http://localhost:8000
   - Refresh the page
   - You should see the new tasks!

---

## ⚙️ Configuration Options

Edit these in your `.env` file:

### Check Interval
How often to check for new emails (in seconds):
```env
CHECK_INTERVAL=60    # Check every 60 seconds (1 minute)
CHECK_INTERVAL=300   # Check every 5 minutes
CHECK_INTERVAL=30    # Check every 30 seconds
```

### API URL
If running on a different port:
```env
API_URL=http://localhost:8000/ingest-email
API_URL=http://localhost:5000/ingest-email
```

### Filter Options
You can modify `gmail_integration.py` to:
- Only process emails from specific senders
- Only process emails with specific subjects
- Process emails from specific labels/folders

---

## 📁 Advanced: Filter Specific Emails

### Option 1: Filter by Sender

Edit `gmail_integration.py`, find the `process_emails` function and add:

```python
# Only process emails from specific senders
allowed_senders = ['boss@company.com', 'manager@company.com']
if sender not in allowed_senders:
    continue
```

### Option 2: Filter by Subject Keywords

```python
# Only process emails with TODO, Task, or Action in subject
keywords = ['TODO', 'Task', 'Action', 'URGENT']
if not any(keyword.lower() in subject.lower() for keyword in keywords):
    continue
```

### Option 3: Process Specific Gmail Label

```python
# Process emails from a specific label
process_emails(mail, folder='Tasks', filter_unread=True)
```

---

## 🔧 Troubleshooting

### Error: "Authentication failed"
**Solution**:
- Make sure you're using an **App Password**, not your regular password
- Check that 2-Step Verification is enabled
- Verify the email and password in `.env` are correct
- Remove any spaces from the App Password

### Error: "IMAP access is disabled"
**Solution**:
- Go to Gmail Settings → Forwarding and POP/IMAP
- Enable IMAP access
- Wait a few minutes and try again

### Error: "Connection refused" or "Cannot reach API"
**Solution**:
- Make sure Flask server is running (`python app.py`)
- Check that API_URL in `.env` is correct
- Verify port 8000 is not blocked

### No emails being processed
**Solution**:
- Check that you have unread emails in your inbox
- Try sending a new test email
- Check the terminal for error messages
- Verify Gmail credentials are correct

### "Too many login attempts"
**Solution**:
- Wait 15 minutes before trying again
- Make sure you're not running multiple instances
- Check that the App Password is correct

---

## 🎯 How It Works

```
1. Gmail Integration Script runs
   ↓
2. Connects to Gmail via IMAP
   ↓
3. Checks for new/unread emails every 60 seconds
   ↓
4. For each new email:
   - Extracts subject, body, sender
   - Sends to your Flask API
   ↓
5. Flask API processes email:
   - Extracts tasks using LLM/fallback
   - Categorizes and prioritizes
   - Stores in tasks.json
   ↓
6. Tasks appear on your dashboard!
```

---

## 💡 Pro Tips

### 1. Create Gmail Filters
Set up Gmail filters to:
- Auto-label task-related emails
- Star important emails
- Forward specific emails to a folder

### 2. Use Gmail Labels
Create labels like:
- "Tasks" - for task-related emails
- "Urgent" - for urgent tasks
- "Work" - for work emails

Then modify the script to process specific labels.

### 3. Run as Background Service

**Windows (using Task Scheduler)**:
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: At startup
4. Action: Start program → `python gmail_integration.py`

**Or use a batch file**:
```batch
@echo off
cd C:\path\to\your\project
python gmail_integration.py
```

### 4. Multiple Email Accounts
Run multiple instances with different `.env` files:
```bash
# Terminal 1
python gmail_integration.py

# Terminal 2 (with different config)
GMAIL_USER=other@gmail.com python gmail_integration.py
```

---

## 🔒 Security Notes

✅ **Safe Practices**:
- App Passwords are safer than your main password
- Can be revoked anytime from Google Account settings
- Only works for this specific app
- Doesn't give access to your full Google Account

⚠️ **Important**:
- Never share your App Password
- Don't commit `.env` file to git (it's in .gitignore)
- Revoke App Password if you stop using the integration

---

## 📊 What Gets Extracted

The system automatically extracts:
- ✅ **Tasks**: Action items from email body
- ✅ **Due Dates**: "by Friday", "December 15", etc.
- ✅ **Priorities**: "URGENT", "important", "ASAP"
- ✅ **Categories**: Work, Personal, Academic, Urgent, Low Priority
- ✅ **Sender**: Who sent the email

---

## 🎉 You're All Set!

Once running, the system will:
1. ✅ Monitor your Gmail 24/7
2. ✅ Automatically extract tasks from new emails
3. ✅ Categorize and prioritize them
4. ✅ Display them on your beautiful dashboard
5. ✅ No manual work needed!

---

## 📞 Quick Reference

**Start Flask Server**:
```bash
python app.py
```

**Start Gmail Integration**:
```bash
python gmail_integration.py
```

**View Dashboard**:
```
http://localhost:8000
```

**Stop Integration**:
Press `Ctrl + C` in the terminal

---

## 🆚 Gmail vs Outlook

| Feature | Gmail (FREE) | Outlook (Power Automate) |
|---------|--------------|--------------------------|
| Cost | ✅ FREE | ⚠️ Limited free tier |
| Setup Time | 5 minutes | 10 minutes |
| Reliability | ✅ Very reliable | ✅ Very reliable |
| Real-time | ✅ 1-minute delay | ✅ Instant |
| Filtering | ✅ Full control | ✅ Full control |
| Maintenance | ✅ None | ⚠️ May need updates |

**Recommendation**: Use Gmail integration - it's completely free and works great!

---

**Need help? Check the troubleshooting section or send a test email to verify it's working!** 🚀
