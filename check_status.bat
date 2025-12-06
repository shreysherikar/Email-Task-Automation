@echo off
echo Checking Gmail Integration Status...
echo.
call venv\Scripts\activate.bat
python check_gmail_status.py
pause
