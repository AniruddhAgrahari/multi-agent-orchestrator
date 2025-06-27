# Daily Briefing Agent - Frontend

A modern, professional web interface for the AI-powered Daily Briefing Agent. Get comprehensive, personalized daily briefings with weather, news, and AI insights.

## 🌟 Features

- **Ultra-Minimal Design**: Clean, professional interface with dark/light mode
- **Three-Section Output**: Weather & Environment, News & Updates, Insights & Analysis  
- **Dynamic Loading**: Animated progress indicators with step-by-step feedback
- **History Management**: Save, search, and organize your briefings
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile
- **Theme Persistence**: Your preferred theme is saved across sessions

## 🚀 Live Demo

Visit the live application: [Your GitHub Pages URL]

## 🛠️ Deployment on GitHub Pages

### Prerequisites

1. A GitHub account
2. A backend API deployed (see [Backend Setup](#backend-setup))

### Step 1: Fork or Clone This Repository

```bash
git clone https://github.com/your-username/daily-briefing-agent.git
cd daily-briefing-agent
```

### Step 2: Configure Your API Endpoint

Edit `config.js` and update the production API URL:

```javascript
production: {
    baseUrl: 'https://your-api-domain.com',  // Change this to your API URL
    apiBase: '/api/v1'
}
```

### Step 3: Deploy to GitHub Pages

1. Push your changes to GitHub:
   ```bash
   git add .
   git commit -m "Configure for production deployment"
   git push origin main
   ```

2. Enable GitHub Pages:
   - Go to your repository on GitHub
   - Click **Settings** → **Pages**
   - Under **Source**, select **Deploy from a branch**
   - Choose **main branch** and **/ (root)**
   - Click **Save**

3. Your site will be available at: `https://your-username.github.io/daily-briefing-agent/daily_briefing_generator/web_interface/frontend/`

### Step 4: Custom Domain (Optional)

To use a custom domain like `briefing.yourdomain.com`:

1. Add a `CNAME` file in the `frontend` folder with your domain
2. Configure your DNS provider to point to `your-username.github.io`
3. Enable **Enforce HTTPS** in GitHub Pages settings

## 🔧 Backend Setup

The frontend requires a backend API. Here are your deployment options:

### Option 1: Heroku (Recommended)

1. Create a Heroku account
2. Install Heroku CLI
3. Deploy the backend:
   ```bash
   cd daily_briefing_generator
   heroku create your-app-name
   git push heroku main
   ```

### Option 2: Railway

1. Connect your GitHub repo to Railway
2. Deploy with one click
3. Configure environment variables

### Option 3: Render

1. Connect your GitHub repo to Render
2. Create a new Web Service
3. Set build and start commands

### Option 4: Serverless Functions

- **Netlify Functions**: Deploy as serverless functions
- **Vercel API Routes**: Use Vercel's API routing
- **AWS Lambda**: Deploy using AWS SAM or Serverless Framework

## 🔑 Environment Variables

Configure these in your backend deployment:

```env
NEWS_API_KEY=your_news_api_key
WEATHER_API_KEY=your_openweather_api_key  
OPENAI_API_KEY=your_openai_api_key
CORS_ORIGINS=https://your-frontend-domain.com
```

## 📁 Project Structure

```
frontend/
├── index.html              # Main application
├── config.js              # Environment configuration
├── static/
│   ├── css/
│   │   └── styles.css     # Additional styles (mostly inline)
│   └── js/
│       └── briefing.js    # Main application logic
└── templates/             # Template files
```

## 🎨 Customization

### Themes

The application supports both light and dark themes with CSS variables. Customize colors in `index.html`:

```css
:root {
    --primary-color: #2563eb;
    --bg-primary: #ffffff;
    --text-primary: #0f172a;
    /* ... */
}
```

### Branding

Update the logo and branding in `index.html`:

```html
<div class="logo">
    <div class="logo-icon">🤖</div>
    <div class="logo-text">Your Brand</div>
</div>
```

## 🔒 CORS Configuration

Make sure your backend API allows requests from your frontend domain:

```python
# In your Flask app
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['https://your-username.github.io'])
```

## 📱 Mobile Support

The interface is fully responsive and includes:
- Touch-friendly interactions
- Optimized typography for mobile
- Collapsible sidebar for small screens
- Swipe gestures for navigation

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Failed**: Check your backend URL in `config.js`
2. **CORS Errors**: Ensure your backend allows your frontend domain
3. **Theme Not Saving**: Check localStorage availability
4. **Mobile Layout Issues**: Verify viewport meta tag

### Debug Mode

Enable debug mode by running locally (`localhost`). This provides:
- Detailed console logging
- API request/response information
- Performance metrics

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For support and questions:
- Open an issue on GitHub
- Check the [Wiki](link-to-wiki) for documentation
- Join our community Discord (if applicable)

---

Built with ❤️ for the AI community
