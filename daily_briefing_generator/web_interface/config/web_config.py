"""
Web Interface Configuration
==========================

Configuration settings for the Daily Briefing Agent web interface.
Handles environment-specific settings, API configurations, and web server options.
"""

import os
from typing import Optional

class WebConfig:
    """Web interface configuration"""
    
    # Server Configuration
    HOST: str = os.getenv("WEB_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("WEB_PORT", "8000"))
    DEBUG: bool = os.getenv("WEB_DEBUG", "False").lower() == "true"
    RELOAD: bool = os.getenv("WEB_RELOAD", "True").lower() == "true"
    
    # API Configuration
    API_VERSION: str = "v1"
    API_PREFIX: str = f"/api/{API_VERSION}"
    
    # CORS Configuration
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        # Add production domains here
    ]
    
    # Static Files
    STATIC_DIR: str = "frontend/static"
    TEMPLATES_DIR: str = "frontend/templates"
    
    # Security Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "daily-briefing-agent-secret-key-change-in-production")
    
    # Rate Limiting (requests per minute)
    RATE_LIMIT_BRIEFING: int = int(os.getenv("RATE_LIMIT_BRIEFING", "10"))
    RATE_LIMIT_HEALTH: int = int(os.getenv("RATE_LIMIT_HEALTH", "60"))
    
    # Request Timeouts (seconds)
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "60"))
    AGENT_TIMEOUT: int = int(os.getenv("AGENT_TIMEOUT", "30"))
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Health Check Configuration
    HEALTH_CHECK_INTERVAL: int = int(os.getenv("HEALTH_CHECK_INTERVAL", "30"))
    
    # Cache Configuration (for future use)
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "300"))  # 5 minutes
    ENABLE_CACHE: bool = os.getenv("ENABLE_CACHE", "False").lower() == "true"
    
    # Database Configuration (for future use)
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    
    # External API Configuration
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY: int = int(os.getenv("RETRY_DELAY", "1"))
    
    # UI Configuration
    MAX_BRIEFING_LENGTH: int = int(os.getenv("MAX_BRIEFING_LENGTH", "10000"))
    DEFAULT_LOCATION: str = os.getenv("DEFAULT_LOCATION", "London")
    
    @classmethod
    def get_uvicorn_config(cls) -> dict:
        """Get uvicorn server configuration"""
        return {
            "host": cls.HOST,
            "port": cls.PORT,
            "reload": cls.RELOAD,
            "log_level": cls.LOG_LEVEL.lower(),
            "access_log": True,
            "loop": "asyncio"
        }
    
    @classmethod
    def get_cors_config(cls) -> dict:
        """Get CORS middleware configuration"""
        return {
            "allow_origins": cls.CORS_ORIGINS,
            "allow_credentials": True,
            "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["*"],
        }
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment"""
        return os.getenv("ENVIRONMENT", "development").lower() == "production"
    
    @classmethod
    def get_logging_config(cls) -> dict:
        """Get logging configuration"""
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": cls.LOG_FORMAT,
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "default": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                },
                "file": {
                    "formatter": "default",
                    "class": "logging.FileHandler",
                    "filename": "logs/web_interface.log",
                    "mode": "a",
                },
            },
            "root": {
                "level": cls.LOG_LEVEL,
                "handlers": ["default"] + (["file"] if cls.is_production() else []),
            },
        }

# Environment-specific configurations
class DevelopmentConfig(WebConfig):
    """Development environment configuration"""
    DEBUG = True
    RELOAD = True
    LOG_LEVEL = "DEBUG"

class ProductionConfig(WebConfig):
    """Production environment configuration"""
    DEBUG = False
    RELOAD = False
    LOG_LEVEL = "INFO"
    
    # Production security settings
    CORS_ORIGINS = [
        # Add your production domains here
        "https://yourdomain.com",
        "https://www.yourdomain.com"
    ]

class TestingConfig(WebConfig):
    """Testing environment configuration"""
    DEBUG = True
    TESTING = True
    LOG_LEVEL = "DEBUG"
    
    # Use different port for testing
    PORT = 8001

# Configuration factory
def get_config():
    """Get configuration based on environment"""
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    if env == "production":
        return ProductionConfig()
    elif env == "testing":
        return TestingConfig()
    else:
        return DevelopmentConfig()

# Global configuration instance
config = get_config()

# Export commonly used settings
__all__ = [
    "WebConfig",
    "DevelopmentConfig", 
    "ProductionConfig",
    "TestingConfig",
    "get_config",
    "config"
]
