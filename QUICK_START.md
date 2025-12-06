# 🚀 Quick Start Guide

## Get Running in 3 Steps

### Step 1: Install Dependencies
```bash
setup.bat
```
Or manually:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Configure (Optional)
```bash
copy .env.example .env
# Edit .env and add your OpenAI API key
```
**Note**: System works without API key using fallback extraction!

### Step 3: Start the Server
```bash
python app.py
```

### Step 4: Open Dashboard
Navigate to: **http://localhost:8000**

---

## 🧪 Test the System

### View Sample Tasks
The dashboard loads with 7 pre-seeded sample tasks automatically.

### Test Email Ingestion
```bash
curl -X POST http://localhost:8000/ingest-email -H "Content-Type: application/json" -d @examples/sample_emails.json
```

### Test Kiro Hook
```bash
python kiro_email_hook.py "{\"subject\":\"Test\",\"body\":\"Complete the report\",\"sender\":\"test@test.com\"}"
```

---

## 📊 What You'll See

### Dashboard Features
- **Metrics**: Total, Pending, Completed, Urgent counts
- **Filters**: Category, Status, Urgency
- **Charts**: Pie chart (categories) + Bar chart (senders)
- **Dark Mode**: Toggle in header
- **Task Cards**: Color-coded by category

### Sample Tasks Include
- Work tasks (reports, presentations)
- Urgent tasks (server issues)
- Personal tasks (family events)
- Academic tasks (research papers)
- Low priority tasks (appointments)

---

## 🎯 Try These Actions

1. **Filter by Category**: Select "Work" from dropdown
2. **Show Only Urgent**: Check "Urgent Only" box
3. **Complete a Task**: Click "Mark Complete" button
4. **Toggle Dark Mode**: Click moon/sun icon
5. **View Charts**: Scroll to see visual analytics

---

## 📝 API Examples

### Get All Tasks
```bash
curl http://localhost:8000/tasks
```

### Complete a Task
```bash
curl -X POST http://localhost:8000/tasks/complete/TASK_ID
```

### Ingest Email
```bash
curl -X POST http://localhost:8000/ingest-email \
  -H "Content-Type: application/json" \
  -d "{\"subject\":\"Meeting\",\"body\":\"Prepare slides by Friday\",\"sender\":\"boss@company.com\"}"
```

---

## ❓ Troubleshooting

### Port 8000 Already in Use
Change port in `.env`:
```
FLASK_PORT=8001
```

### Dependencies Won't Install
Make sure Python 3.8+ is installed:
```bash
python --version
```

### Dashboard Won't Load
1. Check Flask server is running
2. Verify no errors in terminal
3. Try: http://127.0.0.1:8000

---

## 📚 More Information

- Full documentation: `README.md`
- Implementation details: `IMPLEMENTATION_SUMMARY.md`
- Example emails: `examples/` folder
- Test commands: `examples/test_commands.txt`

---

**That's it! You're ready to automate your email-to-task workflow! 🎉**
