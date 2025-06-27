"""
Daily Briefing Agent - FastAPI Web Server
=========================================

Professional web interface for the multi-agent daily briefing system.
Provides REST API endpoints for weather, news, and comprehensive briefings.
"""

import sys
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager

# Add parent directories to path for agent imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from orchestrator.master_agent import MasterAgent
from routes.briefing import briefing_router
from routes.health import health_router

# Global master agent instance
master_agent = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    global master_agent
    print("🚀 Initializing Daily Briefing Agent...")
    try:
        master_agent = MasterAgent()
        print("✅ Master Agent initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize Master Agent: {e}")
        raise
    
    yield
    
    print("🔄 Shutting down Daily Briefing Agent...")

# Create FastAPI application
app = FastAPI(
    title="Daily Briefing Agent",
    description="Professional multi-agent daily briefing system with weather, news, and synthesis capabilities",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")

# Configure templates (for future use)
templates = Jinja2Templates(directory="../frontend/templates")

# Include API routes
app.include_router(briefing_router, prefix="/api/v1")
app.include_router(health_router, prefix="/api/v1")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main briefing interface"""
    try:
        with open("../frontend/index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Daily Briefing Agent</h1><p>Frontend file not found</p>", status_code=404)

@app.get("/briefing", response_class=HTMLResponse) 
async def briefing_interface(request: Request):
    """Serve the briefing interface"""
    with open("../frontend/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Global HTTP exception handler"""
    return {"error": exc.detail, "status_code": exc.status_code}

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    return {"error": "Internal server error", "details": str(exc)}

def get_master_agent():
    """Get the global master agent instance"""
    global master_agent
    if master_agent is None:
        raise HTTPException(status_code=503, detail="Master agent not initialized")
    return master_agent

if __name__ == "__main__":
    print("🌐 Starting Daily Briefing Agent Web Interface...")
    print("📍 Access the interface at: http://localhost:8000")
    print("📚 API Documentation at: http://localhost:8000/docs")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
