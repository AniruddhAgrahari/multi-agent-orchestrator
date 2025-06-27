@echo off
title Daily Briefing Agent - Quick Setup

echo.
echo 🚀 Daily Briefing Agent - Quick Setup
echo ======================================
echo.

:: Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git is not installed. Please install Git first:
    echo    https://git-scm.com/downloads
    pause
    exit /b 1
)

echo ✅ Git is installed

:: Check if this is already a git repository
if not exist ".git" (
    echo 📁 Initializing Git repository...
    git init
    git add .
    git commit -m "Initial commit: Daily Briefing Agent"
    echo ✅ Git repository initialized
) else (
    echo ✅ Git repository already exists
)

:: Check for GitHub CLI
gh --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ GitHub CLI is available
    echo.
    set /p "create_repo=🎯 Would you like to create a GitHub repository? (y/n): "
    if /i "%create_repo%"=="y" (
        set /p "repo_name=📝 Enter repository name (default: daily-briefing-agent): "
        if "%repo_name%"=="" set repo_name=daily-briefing-agent
        
        echo 🌐 Creating GitHub repository...
        gh repo create "%repo_name%" --public --source=. --remote=origin --push
        if %errorlevel% equ 0 (
            echo ✅ Repository created successfully!
            for /f "tokens=*" %%i in ('gh api user --jq .login') do set username=%%i
            echo 🔗 Repository URL: https://github.com/%username%/%repo_name%
            
            echo.
            set /p "enable_pages=🌐 Would you like to enable GitHub Pages? (y/n): "
            if /i "%enable_pages%"=="y" (
                echo ⚙️ Enabling GitHub Pages...
                gh api -X POST "/repos/%username%/%repo_name%/pages" -f source="{\"branch\":\"main\",\"path\":\"/\"}" 2>nul || echo ℹ️ Enable GitHub Pages manually in repository settings
                echo ✅ GitHub Pages configuration attempted
                echo 🌐 Your site will be available at: https://%username%.github.io/%repo_name%/
            )
        ) else (
            echo ❌ Failed to create repository. You can create it manually at github.com
        )
    )
) else (
    echo ℹ️ GitHub CLI not found. Install it for automatic setup:
    echo    https://cli.github.com/
    echo.
    echo 📋 Manual steps:
    echo 1. Go to https://github.com/new
    echo 2. Create a repository named 'daily-briefing-agent'
    echo 3. Run: git remote add origin https://github.com/YOUR_USERNAME/daily-briefing-agent.git
    echo 4. Run: git push -u origin main
    echo 5. Enable GitHub Pages in repository settings
)

echo.
echo ⚙️ Next Steps:
echo ==============
echo 1. 🔑 Get API keys:
echo    - News API: https://newsapi.org/register
echo    - Weather API: https://openweathermap.org/api
echo    - OpenAI API: https://platform.openai.com/api-keys
echo.
echo 2. 🌐 Deploy backend to:
echo    - Heroku: https://heroku.com
echo    - Railway: https://railway.app
echo    - Render: https://render.com
echo.
echo 3. ⚙️ Update config.js with your API endpoint
echo.
echo 4. 📖 Read GITHUB_PAGES_DEPLOYMENT.md for detailed instructions
echo.
echo 🎉 Setup complete! Happy briefing!
echo.
pause
