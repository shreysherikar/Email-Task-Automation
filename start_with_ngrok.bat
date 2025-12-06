@echo off
echo ========================================
echo Email-to-Task System with ngrok
echo ========================================
echo.

echo Step 1: Starting Flask server...
start "Flask Server" cmd /k "python app.py"
timeout /t 3 /nobreak > nul

echo.
echo Step 2: Starting ngrok tunnel...
echo.
echo IMPORTANT: Copy the HTTPS URL that ngrok provides!
echo Example: https://abc123.ngrok.io
echo.
echo You'll need this URL for Power Automate setup.
echo.
pause

start "ngrok" cmd /k "ngrok http 8000"

echo.
echo ========================================
echo Both services are now running!
echo ========================================
echo.
echo Flask Dashboard: http://localhost:8000
echo ngrok URL: Check the ngrok window
echo.
echo Next steps:
echo 1. Copy the ngrok HTTPS URL
echo 2. Follow OUTLOOK_EMAIL_SETUP.md
echo 3. Set up Power Automate flow
echo.
echo Press any key to open the setup guide...
pause > nul

start OUTLOOK_EMAIL_SETUP.md

echo.
echo Setup guide opened!
echo Keep both windows running.
echo.
pause
