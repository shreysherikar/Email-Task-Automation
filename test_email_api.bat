@echo off
echo ========================================
echo Testing Email Ingestion API
echo ========================================
echo.

echo Sending test email to the API...
echo.

curl -X POST http://localhost:8000/ingest-email -H "Content-Type: application/json" -d "{\"subject\":\"TODO: Test Task from Outlook\",\"body\":\"This is a test email. Please complete the project report by Friday and review the presentation slides.\",\"sender\":\"test@outlook.com\"}"

echo.
echo.
echo ========================================
echo Test complete!
echo ========================================
echo.
echo Check your dashboard at: http://localhost:8000
echo You should see a new task appear!
echo.
pause
