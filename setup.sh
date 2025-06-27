#!/bin/bash

# Daily Briefing Agent - Quick Setup Script
# ==========================================

echo "🚀 Daily Briefing Agent - Quick Setup"
echo "======================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first:"
    echo "   https://git-scm.com/downloads"
    exit 1
fi

echo "✅ Git is installed"

# Check if this is already a git repository
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: Daily Briefing Agent"
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Check for GitHub CLI
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI is available"
    echo ""
    echo "🎯 Would you like to create a GitHub repository? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo "📝 Enter repository name (default: daily-briefing-agent):"
        read -r repo_name
        repo_name=${repo_name:-daily-briefing-agent}
        
        echo "🌐 Creating GitHub repository..."
        if gh repo create "$repo_name" --public --source=. --remote=origin --push; then
            echo "✅ Repository created successfully!"
            echo "🔗 Repository URL: https://github.com/$(gh api user --jq .login)/$repo_name"
            
            echo ""
            echo "🌐 Would you like to enable GitHub Pages? (y/n)"
            read -r pages_response
            if [[ "$pages_response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
                echo "⚙️ Enabling GitHub Pages..."
                gh api -X POST "/repos/$(gh api user --jq .login)/$repo_name/pages" \
                    -f source='{"branch":"main","path":"/"}' || echo "ℹ️ Enable GitHub Pages manually in repository settings"
                echo "✅ GitHub Pages configuration attempted"
                echo "🌐 Your site will be available at: https://$(gh api user --jq .login).github.io/$repo_name/"
            fi
        else
            echo "❌ Failed to create repository. You can create it manually at github.com"
        fi
    fi
else
    echo "ℹ️ GitHub CLI not found. Install it for automatic setup:"
    echo "   https://cli.github.com/"
    echo ""
    echo "📋 Manual steps:"
    echo "1. Go to https://github.com/new"
    echo "2. Create a repository named 'daily-briefing-agent'"
    echo "3. Run: git remote add origin https://github.com/YOUR_USERNAME/daily-briefing-agent.git"
    echo "4. Run: git push -u origin main"
    echo "5. Enable GitHub Pages in repository settings"
fi

echo ""
echo "⚙️ Next Steps:"
echo "=============="
echo "1. 🔑 Get API keys:"
echo "   - News API: https://newsapi.org/register"
echo "   - Weather API: https://openweathermap.org/api"
echo "   - OpenAI API: https://platform.openai.com/api-keys"
echo ""
echo "2. 🌐 Deploy backend to:"
echo "   - Heroku: https://heroku.com"
echo "   - Railway: https://railway.app"
echo "   - Render: https://render.com"
echo ""
echo "3. ⚙️ Update config.js with your API endpoint"
echo ""
echo "4. 📖 Read GITHUB_PAGES_DEPLOYMENT.md for detailed instructions"
echo ""
echo "🎉 Setup complete! Happy briefing!"
