@echo off
echo ========================================
echo Gmail Integration for Email-to-Task
echo ========================================
echo.

echo Checking configuration...
echo.

REM Check if .env file exists
if not exist .env (
    echo ERROR: .env file not found!
    echo.
    echo Please create .env file with your Gmail credentials:
    echo   GMAIL_USER=your.email@gmail.com
    echo   GMAIL_APP_PASSWORD=your_app_password
    echo.
    echo See GMAIL_SETUP.md for detailed instructions.
    echo.
    pause
    exit /b 1
)

echo Configuration found!
echo.
echo Starting Gmail integration...
echo.
echo This will:
echo  - Connect to your Gmail account
echo  - Check for new emails every 60 seconds
echo  - Send them to your task system
echo.
echo Press Ctrl+C to stop monitoring
echo.
pause

python gmail_integration.py

pause
