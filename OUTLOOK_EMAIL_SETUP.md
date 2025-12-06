# 📧 Outlook Email Integration Guide

## Option 2: Email Forwarding Setup (Easy & Recommended)

This guide will help you automatically forward emails from Outlook to your Email-to-Task system.

---

## 🎯 Overview

We'll use **Power Automate** (formerly Microsoft Flow) - a free service included with Outlook that can automatically forward emails to your task system.

**What you'll get:**
- ✅ Automatic email processing
- ✅ No coding required
- ✅ Works with Outlook.com and Office 365
- ✅ Can filter by sender, subject, or keywords
- ✅ Free for basic use

---

## 📋 Prerequisites

1. ✅ Outlook/Microsoft account
2. ✅ Your Flask server running (http://localhost:8000)
3. ✅ Internet connection

---

## 🚀 Setup Steps

### Step 1: Expose Your Local Server to the Internet

Since your server is running on `localhost:8000`, we need to make it accessible from the internet so Power Automate can reach it.

**Option A: Using ngrok (Recommended - Free & Easy)**

1. **Download ngrok**: https://ngrok.com/download
2. **Extract and run**:
   ```bash
   ngrok http 8000
   ```
3. **Copy the HTTPS URL** (looks like: `https://abc123.ngrok.io`)
4. **Keep ngrok running** while you want email forwarding to work

**Option B: Using localtunnel (Alternative)**

1. **Install**:
   ```bash
   npm install -g localtunnel
   ```
2. **Run**:
   ```bash
   lt --port 8000
   ```
3. **Copy the URL** provided

**Option C: Using Cloudflare Tunnel (Most Reliable)**

1. **Install Cloudflare Tunnel**: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/
2. **Run**:
   ```bash
   cloudflared tunnel --url http://localhost:8000
   ```
3. **Copy the URL**

---

### Step 2: Set Up Power Automate Flow

1. **Go to Power Automate**: https://make.powerautomate.com/

2. **Sign in** with your Outlook account

3. **Create a new flow**:
   - Click "Create" → "Automated cloud flow"
   - Name it: "Email to Task Automation"
   - Search for trigger: "When a new email arrives (V3)"
   - Click "Create"

4. **Configure the trigger**:
   - **Folder**: Inbox (or specific folder)
   - **Include Attachments**: No
   - **Only with Attachments**: No
   - Click "Show advanced options"
   - **From**: (Optional) Add specific senders if you want to filter
   - **Subject Filter**: (Optional) Add keywords like "TODO", "Task", "Action"

5. **Add an action**:
   - Click "+ New step"
   - Search for "HTTP"
   - Select "HTTP" action

6. **Configure HTTP request**:
   ```
   Method: POST
   URI: https://YOUR-NGROK-URL.ngrok.io/ingest-email
   Headers:
     Content-Type: application/json
   Body:
   {
     "subject": "@{triggerOutputs()?['body/subject']}",
     "body": "@{triggerOutputs()?['body/bodyPreview']}",
     "sender": "@{triggerOutputs()?['body/from']}"
   }
   ```

7. **Save the flow**

8. **Test it**:
   - Click "Test" → "Manually"
   - Send yourself a test email
   - Check if it appears in your dashboard!

---

## 🎨 Alternative: Outlook Rules + Webhook

If you don't want to use Power Automate, here's a simpler approach:

### Using Outlook Rules

1. **In Outlook**, go to Settings → Mail → Rules
2. **Create a new rule**:
   - Name: "Forward to Task System"
   - Condition: Subject contains "TODO" or "Task"
   - Action: Forward to a webhook email address

3. **Use a webhook service**:
   - **Zapier** (Free tier available): https://zapier.com
   - **Make.com** (Free tier available): https://make.com
   - **IFTTT** (Free): https://ifttt.com

4. **Configure webhook** to POST to your ngrok URL

---

## 📝 Example Email Formats

Send emails like this to automatically create tasks:

**Example 1: Simple Task**
```
Subject: TODO: Complete project report
Body: Please finish the Q4 report by Friday
```

**Example 2: Multiple Tasks**
```
Subject: Action Items from Meeting
Body:
1. Review the budget proposal
2. Schedule follow-up with client
3. Update the project timeline
```

**Example 3: Urgent Task**
```
Subject: URGENT: Server Issue
Body: Fix the production server immediately - customers are affected
```

---

## 🔧 Configuration Tips

### Filter Specific Senders
In Power Automate trigger, add:
- **From**: boss@company.com, manager@company.com

### Filter by Subject Keywords
Add condition:
- **Subject contains**: TODO, Task, Action, URGENT

### Filter by Folder
- Create an "Tasks" folder in Outlook
- Move emails there manually or with rules
- Set Power Automate to watch that folder

---

## 🧪 Testing Your Setup

### Test 1: Send a Test Email
```
To: yourself@outlook.com
Subject: TODO: Test task extraction
Body: This is a test email to verify the automation works. Please complete this task by tomorrow.
```

### Test 2: Check the Dashboard
1. Go to http://localhost:8000
2. Refresh the page
3. You should see the new task appear!

### Test 3: Check Server Logs
Look at your terminal where Flask is running - you should see:
```
Processing email from yourself@outlook.com: TODO: Test task extraction
```

---

## 🐛 Troubleshooting

### Issue: "Connection refused" or "Cannot reach server"
**Solution**: 
- Make sure Flask server is running (`python app.py`)
- Make sure ngrok is running
- Use the HTTPS URL from ngrok (not HTTP)

### Issue: "Unauthorized" or "403 Forbidden"
**Solution**:
- Check that your ngrok URL is correct
- Make sure the `/ingest-email` endpoint is included in the URL

### Issue: Tasks not appearing
**Solution**:
- Check Flask server logs for errors
- Verify the email was sent to Power Automate (check run history)
- Test the API directly with curl first

### Issue: ngrok URL keeps changing
**Solution**:
- Sign up for free ngrok account to get a static URL
- Or use Cloudflare Tunnel for permanent URL
- Update Power Automate flow with new URL when it changes

---

## 💡 Pro Tips

### 1. Create Multiple Flows
- One for work emails (filters @company.com)
- One for personal emails
- One for urgent emails (subject contains "URGENT")

### 2. Add Email Filtering
Only forward emails that:
- Contain specific keywords
- Are from specific people
- Have certain labels/categories

### 3. Use Email Templates
Create email templates in Outlook for common tasks:
- "TODO: [Task Name]"
- "URGENT: [Issue]"
- "Action Items: [List]"

### 4. Set Up Notifications
In Power Automate, add a notification action to alert you when tasks are created

---

## 🔒 Security Notes

⚠️ **Important**: Your ngrok URL is publicly accessible!

**To secure it:**

1. **Add API Key Authentication** (I can implement this)
2. **Use ngrok password protection**:
   ```bash
   ngrok http 8000 --basic-auth="username:password"
   ```
3. **Whitelist Power Automate IPs** (advanced)
4. **Use Cloudflare Tunnel** with access policies

**For production use**, you should:
- Deploy to a proper server (not localhost)
- Use HTTPS with proper SSL certificate
- Implement authentication
- Add rate limiting

---

## 📊 What Happens Next?

Once set up:

1. **You receive an email** → Outlook inbox
2. **Power Automate detects it** → Checks your rules
3. **Forwards to your API** → POST to /ingest-email
4. **LLM extracts tasks** → Analyzes email content
5. **Tasks are stored** → Saved to tasks.json
6. **Dashboard updates** → Refresh to see new tasks!

---

## 🎯 Quick Start Checklist

- [ ] Flask server running (`python app.py`)
- [ ] ngrok running (`ngrok http 8000`)
- [ ] Copy ngrok HTTPS URL
- [ ] Create Power Automate flow
- [ ] Configure HTTP POST action
- [ ] Save and test flow
- [ ] Send test email
- [ ] Check dashboard for new task
- [ ] Celebrate! 🎉

---

## 📞 Need Help?

If you get stuck:
1. Check Flask server logs
2. Check Power Automate run history
3. Test API with curl first
4. Verify ngrok is running and URL is correct

---

## 🚀 Next Steps

Once this is working, you can:
- Add more email filters
- Create multiple flows for different email types
- Set up notifications
- Add task priorities based on sender
- Implement automatic task assignment

---

**Ready to set it up? Start with Step 1 (ngrok) and let me know if you need help!** 🎉
