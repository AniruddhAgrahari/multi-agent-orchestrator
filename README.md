# 🧠 Daily Briefing Agent

> # Synoptic AI: Multi-Agent Orchestrator

🤖 **Professional AI-powered briefing generation system** that orchestrates multiple intelligent agents to provide comprehensive daily briefings with weather data, news updates, and actionable insights.

**Live Demo:** [https://AniruddhAgrahari.github.io/multi-agent-orchestrator/](https://AniruddhAgrahari.github.io/multi-agent-orchestrator/)

[![Deploy to GitHub Pages](https://img.shields.io/badge/Deploy-GitHub%20Pages-blue?style=for-the-badge&logo=github)](https://github.com/your-username/daily-briefing-agent)
[![API Documentation](https://img.shields.io/badge/API-Documentation-green?style=for-the-badge&logo=swagger)](https://your-api-domain.com/docs)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)

## 🌟 Features

### 🎨 **Modern Web Interface**
- **Ultra-minimal design** with professional aesthetics
- **Dark/Light mode** with persistent theme preference
- **Fully responsive** - works on desktop, tablet, and mobile
- **Dynamic loading animations** with step-by-step progress
- **History management** - save, search, and organize briefings

### 🤖 **AI-Powered Intelligence**
- **Multi-agent orchestration** for comprehensive analysis
- **Three-section output**: Weather & Environment, News & Updates, Insights & Analysis
- **Personalized content** based on your requests
- **Real-time data integration** from multiple sources

### 🛡️ **Production Ready**
- **GitHub Pages deployment** with automatic CI/CD
- **Environment configuration** for local and production
- **Error handling and recovery** with user-friendly messages
- **API health monitoring** and status checks

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
setup.bat
```

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/daily-briefing-agent.git
   cd daily-briefing-agent
   ```

2. **Deploy to GitHub Pages:**
   - Follow the [detailed deployment guide](GITHUB_PAGES_DEPLOYMENT.md)

3. **Configure your API endpoint:**
   - Edit `daily_briefing_generator/web_interface/frontend/config.js`
   - Update the production `baseUrl` with your API endpoint

## 🌐 Live Demo

**Frontend**: [View Demo](https://your-username.github.io/daily-briefing-agent/)  
**API Docs**: [API Documentation](https://your-api-domain.com/docs)

## 📁 Project Structure

```
daily-briefing-agent/
├── 📄 README.md                          # This file
├── 📄 GITHUB_PAGES_DEPLOYMENT.md         # Deployment guide
├── 📄 setup.sh / setup.bat               # Quick setup scripts
├── 📁 daily_briefing_generator/
│   ├── 📁 agents/                        # AI agent implementations
│   ├── 📁 orchestrator/                  # Multi-agent orchestrator
│   ├── 📁 web_interface/
│   │   ├── 📁 backend/                   # Flask API server
│   │   └── 📁 frontend/                  # Static web interface
│   │       ├── 📄 index.html             # Main application
│   │       ├── 📄 config.js              # Environment configuration
│   │       └── 📁 static/
│   │           ├── 📁 css/               # Stylesheets
│   │           └── 📁 js/                # JavaScript application
│   └── 📄 requirements.txt               # Python dependencies
└── 📁 .github/workflows/                 # GitHub Actions for deployment
```

## 🔧 Backend Deployment Options

The frontend requires a backend API. Choose one:

### 🌟 **Recommended: Railway**
- ✅ Easy one-click deployment
- ✅ Automatic HTTPS
- ✅ Free tier available
- ✅ Great for beginners

[Deploy to Railway](https://railway.app) → Connect GitHub → Deploy

### 🎯 **Popular: Heroku**
```bash
cd daily_briefing_generator
heroku create your-app-name
git subtree push --prefix=daily_briefing_generator heroku main
```

### ⚡ **Modern: Render**
- Connect GitHub repository
- Set build command: `pip install -r requirements.txt`
- Set start command: `python web_interface/start_web_interface.py`

### 🔥 **Serverless: Netlify/Vercel**
- Convert to serverless functions
- Deploy with automatic scaling

## 🔑 Required API Keys

Get these free API keys for full functionality:

| Service | Purpose | Get Key | Cost |
|---------|---------|---------|------|
| **News API** | Latest news | [newsapi.org](https://newsapi.org/register) | Free tier |
| **OpenWeather** | Weather data | [openweathermap.org](https://openweathermap.org/api) | Free tier |
| **OpenAI** | AI analysis | [platform.openai.com](https://platform.openai.com/api-keys) | Pay per use |

## ⚙️ Configuration

### Environment Variables (Backend)
```env
NEWS_API_KEY=your_news_api_key
WEATHER_API_KEY=your_openweather_api_key  
OPENAI_API_KEY=your_openai_api_key
CORS_ORIGINS=https://your-frontend-domain.com
```

### Frontend Configuration
Edit `daily_briefing_generator/web_interface/frontend/config.js`:
```javascript
production: {
    baseUrl: 'https://your-api-domain.com',  // Your deployed backend
    apiBase: '/api/v1'
}
```

## 🎨 Customization

### 🌈 **Themes**
Customize colors in `index.html`:
```css
:root {
    --primary-color: #2563eb;
    --bg-primary: #ffffff;
    --text-primary: #0f172a;
}
```

### 🏷️ **Branding**
Update logo and title:
```html
<div class="logo">🤖</div>
<h1>Your Brand Name</h1>
```

### ⚡ **Features**
Toggle features in `config.js`:
```javascript
ENABLE_HISTORY: true,
ENABLE_DARK_MODE: true,
ENABLE_API_DOCS: true
```

## 📱 Mobile Support

- ✅ **Touch-friendly** interface
- ✅ **Responsive design** adapts to all screen sizes
- ✅ **Optimized typography** for mobile reading
- ✅ **Swipe gestures** for navigation
- ✅ **Progressive Web App** ready

## 🔒 Security & Privacy

- 🛡️ **No data storage** on the frontend
- 🔐 **HTTPS enforcement** on GitHub Pages
- 🚫 **No tracking** or analytics by default
- 🔑 **API keys** are server-side only
- 🌐 **CORS protection** configured

## 🧪 Testing

### Local Development
```bash
cd daily_briefing_generator
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python web_interface/start_web_interface.py
```

### Production Testing
- ✅ Test on multiple devices
- ✅ Verify API connectivity
- ✅ Check theme persistence
- ✅ Validate responsive design

## 🐛 Troubleshooting

### Common Issues

**API Connection Failed**
```bash
# Check your config.js API endpoint
# Verify backend is deployed and running
# Check CORS settings
```

**Theme Not Saving**
```bash
# Check localStorage availability
# Verify JavaScript console for errors
```

**Mobile Issues**
```bash
# Check viewport meta tag
# Test touch interactions
# Verify responsive breakpoints
```

### Debug Mode

Run locally for detailed logging:
```javascript
// In browser console
window.BRIEFING_CONFIG.DEBUG_MODE = true;
```

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Development Guidelines
- ✅ Follow existing code style
- ✅ Add comments for complex logic
- ✅ Test on multiple browsers
- ✅ Update documentation

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for GPT integration
- **News API** for news data
- **OpenWeather** for weather information
- **GitHub Pages** for free hosting
- **Inter Font** for beautiful typography

## 📞 Support

- 🐛 **Bug Reports**: [Open an issue](https://github.com/your-username/daily-briefing-agent/issues)
- 💡 **Feature Requests**: [Discussions](https://github.com/your-username/daily-briefing-agent/discussions)
- 📧 **Contact**: agraharianiruddha@gmail.com

## 🗺️ Roadmap

- [ ] **Multi-language support** 🌍
- [ ] **Voice interface** 🎤
- [ ] **Email delivery** 📧
- [ ] **Calendar integration** 📅
- [ ] **Custom agent creation** 🔧
- [ ] **Slack/Teams bots** 💬

---

<div align="center">

**Made with ❤️ for the AI community**

[⭐ Star this repo](https://github.com/your-username/daily-briefing-agent) • [🐛 Report Bug](https://github.com/your-username/daily-briefing-agent/issues) • [💡 Request Feature](https://github.com/your-username/daily-briefing-agent/discussions)

</div>
