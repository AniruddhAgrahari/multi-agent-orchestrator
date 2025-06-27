#!/usr/bin/env python3
"""
Daily Briefing Agent - Web Interface Launcher
=============================================

Quick start script for the Daily Briefing Agent web interface.
Handles dependency installation, environment setup, and server startup.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Print startup banner"""
    print("=" * 60)
    print("🚀 Daily Briefing Agent - Web Interface")
    print("=" * 60)
    print("Professional Intelligence Platform")
    print("Multi-agent system with weather, news, and synthesis")
    print("=" * 60)

def check_python_version():
    """Check Python version compatibility"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    backend_dir = Path(__file__).parent / "backend"
    requirements_file = backend_dir / "requirements.txt"
    
    if not requirements_file.exists():
        print(f"❌ Requirements file not found: {requirements_file}")
        sys.exit(1)
    
    try:
        # Install web interface dependencies
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ], check=True, cwd=backend_dir)
        
        # Install core agent dependencies
        core_requirements = Path(__file__).parent.parent / "requirements.txt"
        if core_requirements.exists():
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(core_requirements)
            ], check=True)
        
        print("✅ Dependencies installed successfully")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("Try running manually: pip install -r backend/requirements.txt")
        sys.exit(1)

def check_environment():
    """Check environment configuration"""
    print("\n🔍 Checking environment...")
    
    # Check for .env file
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        print("✅ Environment file found")
    else:
        print("⚠️  No .env file found - using defaults")
    
    # Check for required environment variables
    required_vars = ["GOOGLE_AI_API_KEY", "OPENWEATHER_API_KEY", "NEWS_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print("The system may have limited functionality")
    else:
        print("✅ All required environment variables found")

def start_server():
    """Start the web server"""
    print("\n🌐 Starting web server...")
    
    backend_dir = Path(__file__).parent / "backend"
    
    # Set environment for the server
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).parent.parent)
    
    try:
        # Change to backend directory and start server
        os.chdir(backend_dir)
        
        print("📍 Server will be available at:")
        print("   • Main Interface: http://localhost:8000")
        print("   • API Documentation: http://localhost:8000/docs")
        print("   • Health Check: http://localhost:8000/api/v1/health")
        print("\n🔄 Starting server... (Ctrl+C to stop)")
        
        # Start uvicorn server
        subprocess.run([
            sys.executable, "-m", "uvicorn", "app:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload",
            "--log-level", "info"
        ], env=env)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Failed to start server: {e}")
        sys.exit(1)

def main():
    """Main startup function"""
    print_banner()
    
    check_python_version()
    
    # Check if we should install dependencies
    if "--install" in sys.argv or not Path("backend/requirements.txt").exists():
        install_dependencies()
    
    check_environment()
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()
