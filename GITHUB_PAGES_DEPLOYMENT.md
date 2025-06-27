# 🚀 GitHub Pages Deployment Guide

Complete step-by-step guide to deploy your Daily Briefing Agent to GitHub Pages.

## 📋 Prerequisites

1. **GitHub Account**: Create one at [github.com](https://github.com)
2. **Git Installed**: Download from [git-scm.com](https://git-scm.com)
3. **Backend API**: You'll need to deploy the backend separately (see Backend Options below)

## 🛠️ Step-by-Step Deployment

### Step 1: Prepare Your Repository

1. **Initialize Git** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Create GitHub Repository**:
   - Go to [github.com/new](https://github.com/new)
   - Name it `daily-briefing-agent`
   - Make it **Public** (required for free GitHub Pages)
   - Don't initialize with README (you already have one)

3. **Connect Local to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/daily-briefing-agent.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Configure API Endpoint

**IMPORTANT**: Before deploying, you must update the API configuration.

1. **Edit** `daily_briefing_generator/web_interface/frontend/config.js`
2. **Update the production baseUrl**:
   ```javascript
   production: {
       baseUrl: 'https://your-api-domain.com',  // ← CHANGE THIS
       apiBase: '/api/v1'
   }
   ```

3. **Commit the changes**:
   ```bash
   git add .
   git commit -m "Configure production API endpoint"
   git push
   ```

### Step 3: Enable GitHub Pages

1. **Go to your repository** on GitHub
2. **Click Settings** (top menu)
3. **Scroll down to Pages** (left sidebar)
4. **Under Source**:
   - Select "Deploy from a branch"
   - Choose "main" branch
   - Select "/ (root)" folder
5. **Click Save**

### Step 4: Access Your Site

Your site will be available at:
```
https://YOUR_USERNAME.github.io/daily-briefing-agent/
```

**Note**: It may take 5-10 minutes for the first deployment to complete.

## 🔧 Backend Deployment Options

Your frontend needs a backend API. Here are the best options:

### Option 1: Heroku (Free Tier Available)

1. **Create Heroku account** at [heroku.com](https://heroku.com)
2. **Install Heroku CLI**
3. **Deploy**:
   ```bash
   cd daily_briefing_generator
   heroku create your-app-name
   git subtree push --prefix=daily_briefing_generator heroku main
   ```
4. **Configure environment variables**:
   ```bash
   heroku config:set NEWS_API_KEY=your_key
   heroku config:set WEATHER_API_KEY=your_key
   heroku config:set OPENAI_API_KEY=your_key
   ```

### Option 2: Railway (Modern & Easy)

1. **Sign up** at [railway.app](https://railway.app)
2. **Connect GitHub** repository
3. **Deploy** with one click
4. **Add environment variables** in dashboard

### Option 3: Render (Free Tier)

1. **Create account** at [render.com](https://render.com)
2. **Connect GitHub** repository  
3. **Create Web Service**
4. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python web_interface/start_web_interface.py`

### Option 4: Netlify Functions

1. **Deploy to Netlify**
2. **Convert backend** to Netlify Functions
3. **Update API endpoints** in config.js

## 🔑 Environment Variables Needed

Your backend deployment needs these API keys:

```env
NEWS_API_KEY=your_news_api_key_from_newsapi.org
WEATHER_API_KEY=your_openweather_api_key  
OPENAI_API_KEY=your_openai_api_key
CORS_ORIGINS=https://YOUR_USERNAME.github.io
```

## 🌐 Custom Domain (Optional)

To use your own domain like `briefing.yourdomain.com`:

### Step 1: Add CNAME File

Create `daily_briefing_generator/web_interface/frontend/CNAME`:
```
briefing.yourdomain.com
```

### Step 2: Configure DNS

In your domain provider's DNS settings:
```
Type: CNAME
Name: briefing (or your subdomain)
Value: YOUR_USERNAME.github.io
```

### Step 3: Enable HTTPS

1. **Go to GitHub Pages settings**
2. **Check "Enforce HTTPS"**
3. **Wait for SSL certificate** (automatic)

## 🔧 Troubleshooting

### Common Issues

**1. API Connection Failed**
- ✅ Check backend is deployed and running
- ✅ Verify API URL in `config.js`
- ✅ Check CORS settings on backend

**2. Page Not Loading**
- ✅ Wait 5-10 minutes after enabling Pages
- ✅ Check GitHub Actions tab for build errors
- ✅ Ensure repository is public

**3. CORS Errors**
- ✅ Add your GitHub Pages URL to backend CORS origins
- ✅ Include both `http://` and `https://` versions

**4. Theme/History Not Working**
- ✅ Check browser console for JavaScript errors
- ✅ Ensure `config.js` is loaded before `briefing.js`

### Debug Steps

1. **Open browser Developer Tools** (F12)
2. **Check Console tab** for errors
3. **Check Network tab** for failed requests
4. **Verify config** by typing `window.BRIEFING_CONFIG` in console

## 📱 Testing Your Deployment

1. **Test on different devices**: Desktop, tablet, mobile
2. **Test both themes**: Light and dark mode
3. **Test core features**:
   - Generate briefing
   - Save to history
   - Theme toggle
   - Responsive design

## 🔄 Updating Your Site

To update your deployed site:

```bash
git add .
git commit -m "Your update message"
git push
```

GitHub Pages will automatically rebuild and deploy in a few minutes.

## 📞 Need Help?

If you encounter issues:

1. **Check the Issues tab** in your GitHub repository
2. **Review the Actions tab** for build logs
3. **Test locally first** with `python start_web_interface.py`
4. **Verify all API keys** are configured correctly

## 🎉 Success!

Once deployed, you'll have:
- ✅ Professional Daily Briefing Agent
- ✅ Accessible from anywhere
- ✅ Mobile-responsive design
- ✅ Dark/light theme support
- ✅ History management
- ✅ Free hosting on GitHub Pages

Your users can now access personalized AI briefings at your GitHub Pages URL!

---

**Remember**: Keep your API keys secure and never commit them to your repository!
