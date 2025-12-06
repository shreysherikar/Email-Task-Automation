# 🚀 Outlook Integration - Quick Start

## Super Simple 3-Step Setup

### Step 1: Download ngrok (One-time setup)
1. Go to: https://ngrok.com/download
2. Download for Windows
3. Extract the `ngrok.exe` file to your project folder
4. Done! (No installation needed)

### Step 2: Run the System
Double-click: **`start_with_ngrok.bat`**

This will:
- ✅ Start your Flask server
- ✅ Start ngrok tunnel
- ✅ Give you a public URL

**Copy the HTTPS URL** from the ngrok window (looks like: `https://abc123.ngrok.io`)

### Step 3: Set Up Power Automate
1. Go to: https://make.powerautomate.com
2. Sign in with your Outlook account
3. Click "Create" → "Automated cloud flow"
4. Name it: "Email to Tasks"
5. Trigger: "When a new email arrives (V3)"
6. Add action: "HTTP"
7. Configure:
   - Method: **POST**
   - URI: **`https://YOUR-NGROK-URL.ngrok.io/ingest-email`**
   - Headers: `Content-Type: application/json`
   - Body:
   ```json
   {
     "subject": "@{triggerOutputs()?['body/subject']}",
     "body": "@{triggerOutputs()?['body/bodyPreview']}",
     "sender": "@{triggerOutputs()?['body/from']}"
   }
   ```
8. Save and test!

---

## 🧪 Test Before Setting Up Outlook

Run: **`test_email_api.bat`**

This sends a test email to your API. Check http://localhost:8000 to see if it appears!

---

## 📧 How to Use

Once set up, just send emails like:

**Example 1:**
```
Subject: TODO: Finish report
Body: Complete the Q4 financial report by Friday
```

**Example 2:**
```
Subject: URGENT: Server down
Body: Fix production server immediately
```

**Example 3:**
```
Subject: Meeting action items
Body:
1. Review budget proposal
2. Schedule client call
3. Update timeline
```

The system will automatically:
- ✅ Extract all tasks
- ✅ Detect due dates
- ✅ Categorize (Work, Personal, Urgent, etc.)
- ✅ Show on your dashboard

---

## 💡 Pro Tips

### Filter Specific Emails
In Power Automate, add conditions:
- **From**: Only from specific people
- **Subject contains**: "TODO", "Task", "Action"
- **Folder**: Only from specific Outlook folder

### Create Multiple Flows
- One for work emails
- One for personal emails  
- One for urgent emails

### Use Email Rules
In Outlook, create rules to:
- Move task emails to a specific folder
- Flag emails with keywords
- Forward to Power Automate

---

## 🔧 Troubleshooting

### Can't access dashboard?
- Make sure Flask is running
- Go to: http://localhost:8000
- Hard refresh: Ctrl + Shift + R

### ngrok URL not working?
- Make sure ngrok is running
- Use the HTTPS URL (not HTTP)
- Copy the full URL including https://

### Tasks not appearing?
- Check Flask server logs
- Run `test_email_api.bat` first
- Verify Power Automate flow ran (check run history)

### ngrok URL keeps changing?
- Free ngrok URLs change each restart
- Sign up for free account to get static URL
- Or use Cloudflare Tunnel instead

---

## 📊 What You Get

✅ **Automatic task extraction** from emails  
✅ **Smart categorization** (Work, Personal, Academic, Urgent)  
✅ **Due date detection** from email text  
✅ **Priority assignment** based on keywords  
✅ **Beautiful dashboard** with charts and filters  
✅ **Dark mode** support  
✅ **No manual data entry** needed  

---

## 🎯 Ready?

1. **Download ngrok** (if you haven't)
2. **Run**: `start_with_ngrok.bat`
3. **Copy the ngrok URL**
4. **Set up Power Automate** (5 minutes)
5. **Send a test email**
6. **Watch it appear on your dashboard!** 🎉

---

**Need help? Check the full guide: `OUTLOOK_EMAIL_SETUP.md`**
