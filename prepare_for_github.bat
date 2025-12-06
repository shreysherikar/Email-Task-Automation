@echo off
echo ============================================================
echo   Preparing Email-to-Task Automation for GitHub
echo ============================================================
echo.

echo Step 1: Cleaning task data...
python clean_tasks.py
if errorlevel 1 (
    echo Error cleaning tasks!
    pause
    exit /b 1
)
echo.

echo Step 2: Replacing README with GitHub version...
copy /Y README_GITHUB.md README.md
echo.

echo Step 3: Creating necessary directories...
if not exist ".github" mkdir .github
if not exist ".github\ISSUE_TEMPLATE" mkdir .github\ISSUE_TEMPLATE
if not exist ".github\workflows" mkdir .github\workflows
echo.

echo Step 4: Checking for sensitive data...
echo.
echo IMPORTANT: Make sure .env is NOT committed!
echo.
findstr /C:"OPENAI_API_KEY" .env >nul 2>&1
if not errorlevel 1 (
    echo [WARNING] .env file contains API keys!
    echo [WARNING] Make sure it's in .gitignore!
)
echo.

echo Step 5: Verifying .gitignore...
findstr /C:".env" .gitignore >nul 2>&1
if errorlevel 1 (
    echo [ERROR] .env is NOT in .gitignore!
    echo [ERROR] Add it before committing!
    pause
    exit /b 1
) else (
    echo [OK] .env is in .gitignore
)
echo.

echo Step 6: Creating data directory structure...
if not exist "data" mkdir data
echo. > data\.gitkeep
echo.

echo ============================================================
echo   Preparation Complete!
echo ============================================================
echo.
echo Next steps:
echo.
echo 1. Review README.md (now updated with GitHub version)
echo 2. Check that .env is in .gitignore
echo 3. Initialize git repository:
echo    git init
echo.
echo 4. Add all files:
echo    git add .
echo.
echo 5. Check what will be committed:
echo    git status
echo    (Make sure .env is NOT in the list!)
echo.
echo 6. Create initial commit:
echo    git commit -m "feat: initial commit - Email-to-Task Automation System"
echo.
echo 7. Create GitHub repository at https://github.com/new
echo.
echo 8. Add remote and push:
echo    git remote add origin https://github.com/YOUR_USERNAME/email-task-automation.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo See GITHUB_SETUP.md for detailed instructions!
echo.
pause
