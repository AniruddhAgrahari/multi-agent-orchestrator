# Daily Briefing Agent - Web Interface

## 🌐 Professional Web Interface for Multi-Agent Daily Briefing System

A modern, responsive web interface for the Daily Briefing Agent that provides:
- **Professional Dashboard** for briefing requests
- **Real-time Status Monitoring** of agent health
- **Interactive API** with comprehensive documentation
- **Quick Briefing Templates** for common requests
- **Error Recovery & Monitoring** with graceful degradation

## 📁 Project Structure

```
web_interface/
├── backend/                    # FastAPI server
│   ├── app.py                 # Main application server
│   ├── routes/
│   │   ├── briefing.py        # Briefing API endpoints
│   │   └── health.py          # Health monitoring endpoints
│   └── requirements.txt       # Web dependencies
├── frontend/                   # Modern web interface
│   ├── index.html            # Main briefing interface
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css    # Professional styling
│   │   └── js/
│   │       └── briefing.js   # Interactive functionality
│   └── templates/
│       └── base.html         # Template base
├── config/
│   └── web_config.py         # Web-specific configuration
└── start_web_interface.py    # Quick start launcher
```

## 🚀 Quick Start

### Option 1: Quick Launcher (Recommended)
```bash
cd web_interface
python start_web_interface.py
```

### Option 2: Manual Setup
```bash
# Install dependencies
cd web_interface/backend
pip install -r requirements.txt

# Start server
python app.py
```

### Option 3: Direct Uvicorn
```bash
cd web_interface/backend
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

## 🔗 Access Points

Once running, access the interface at:

- **🏠 Main Interface**: http://localhost:8000
- **📚 API Documentation**: http://localhost:8000/docs
- **📖 API Reference**: http://localhost:8000/redoc
- **💓 Health Check**: http://localhost:8000/api/v1/health

## ✨ Features

### **Professional Dashboard**
- Clean, modern interface with professional styling
- Quick action buttons for common briefing types
- Custom briefing form with advanced options
- Real-time loading indicators with progress steps

### **API Endpoints**

#### Briefing Endpoints
- `POST /api/v1/briefing` - Generate custom briefings
- `GET /api/v1/briefing/quick/{type}` - Quick briefing templates
- `GET /api/v1/briefing/templates` - Available templates and options

#### Health Monitoring
- `GET /api/v1/health` - Basic health check
- `GET /api/v1/health/detailed` - Comprehensive system status
- `GET /api/v1/health/agents` - Individual agent health
- `GET /api/v1/health/ready` - Kubernetes readiness probe
- `GET /api/v1/health/live` - Kubernetes liveness probe

### **Quick Briefing Types**
- **Weather Focus**: Location-based weather briefings
- **News Digest**: Category-filtered news updates
- **Business Updates**: Business and market news
- **Tech News**: Technology sector briefings
- **Complete Briefing**: Comprehensive weather + news synthesis

### **Advanced Features**
- **Error Recovery**: Toggle-able error recovery for robust operation
- **System Monitoring**: Real-time health status and performance metrics
- **Professional Formatting**: Markdown-style content with proper typography
- **Copy/Download**: Easy sharing and export of briefings
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## 🛠️ Configuration

### Environment Variables
```bash
# Web Server Configuration
WEB_HOST=0.0.0.0
WEB_PORT=8000
WEB_DEBUG=False
WEB_RELOAD=True

# API Configuration
RATE_LIMIT_BRIEFING=10
RATE_LIMIT_HEALTH=60
REQUEST_TIMEOUT=60

# Security (Production)
SECRET_KEY=your-secret-key-here
ENVIRONMENT=production

# Core Agent APIs (inherited from main system)
GOOGLE_AI_API_KEY=your-gemini-key
OPENWEATHER_API_KEY=your-weather-key
NEWS_API_KEY=your-news-key
```

### Production Deployment
```bash
# Set production environment
export ENVIRONMENT=production
export WEB_DEBUG=False
export WEB_RELOAD=False

# Start with production settings
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📱 API Usage Examples

### Generate Custom Briefing
```bash
curl -X POST "http://localhost:8000/api/v1/briefing" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "Morning briefing for London with technology news",
       "location": "London",
       "categories": ["technology"],
       "use_recovery": true
     }'
```

### Quick Weather Briefing
```bash
curl "http://localhost:8000/api/v1/briefing/quick/weather?location=Tokyo"
```

### System Health Check
```bash
curl "http://localhost:8000/api/v1/health/detailed"
```

## 🎨 UI Components

### **Professional Styling**
- Modern Inter font family
- Consistent color scheme with CSS variables
- Responsive grid layouts
- Smooth animations and transitions
- Professional iconography with Font Awesome

### **Interactive Elements**
- Real-time form validation
- Progress indicators for long operations
- Toast notifications for user feedback
- Modal dialogs for detailed information
- Keyboard shortcuts (Ctrl+Enter to submit)

### **Status Monitoring**
- Color-coded health indicators
- System metrics display (CPU, memory, disk)
- Agent status tracking
- Performance monitoring
- Error logging and display

## 🔧 Development

### **Adding New Features**
1. **Backend**: Add routes in `backend/routes/`
2. **Frontend**: Update `frontend/static/js/briefing.js`
3. **Styling**: Modify `frontend/static/css/styles.css`
4. **Configuration**: Update `config/web_config.py`

### **Testing**
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest backend/tests/
```

### **Docker Deployment**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🚨 Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Kill existing process
lsof -ti:8000 | xargs kill -9
# Or use different port
uvicorn app:app --port 8001
```

**Missing dependencies:**
```bash
# Install all dependencies
pip install -r backend/requirements.txt
pip install -r ../requirements.txt
```

**API connection errors:**
- Check that core agents are properly configured
- Verify environment variables are set
- Check network connectivity for external APIs

### **Logs and Monitoring**
- Server logs: Check console output
- Agent logs: Check main system logs
- Error tracking: Check browser console for frontend issues
- Health status: Visit `/api/v1/health/detailed`

## 📈 Performance

### **Optimization Features**
- Async/await throughout for non-blocking operations
- Request timeouts to prevent hanging
- Connection pooling for external APIs
- Graceful error handling and recovery
- Efficient static file serving

### **Scaling Considerations**
- Use multiple workers for production: `--workers 4`
- Implement caching for frequently requested briefings
- Add load balancing for high availability
- Monitor resource usage with system health endpoints

## 🔒 Security

### **Built-in Security**
- CORS configuration for cross-origin requests
- Request validation with Pydantic models
- Rate limiting (configurable)
- Input sanitization
- Error message sanitization to prevent information leakage

### **Production Security**
- Use HTTPS in production
- Set secure SECRET_KEY
- Configure appropriate CORS origins
- Implement authentication if needed
- Regular dependency updates

---

**🎯 Ready to use!** The web interface provides a professional, feature-rich platform for interacting with your Daily Briefing Agent system.
