"""
Health Check API Routes
======================

System health and status monitoring endpoints.
"""

from fastapi import APIRouter
from pydantic import BaseModel
import asyncio
import time
from datetime import datetime
import psutil
import os

health_router = APIRouter(tags=["health"])

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    uptime: float
    version: str

class SystemStatus(BaseModel):
    status: str
    agents: dict
    system: dict
    performance: dict

# Track service start time
start_time = time.time()

@health_router.get("/health", response_model=HealthResponse)
async def health_check():
    """Basic health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        uptime=time.time() - start_time,
        version="1.0.0"
    )

@health_router.get("/health/detailed", response_model=SystemStatus)
async def detailed_health_check():
    """Detailed system health check"""
    try:
        # Import here to avoid circular imports
        from app import get_master_agent
        
        # Test master agent
        try:
            master_agent = get_master_agent()
            master_status = "healthy"
            
            # Test basic functionality
            test_response = await asyncio.wait_for(
                master_agent.process_request("Health check test"),
                timeout=5.0
            )
            agent_test_status = "passed" if test_response else "failed"
            
        except Exception as e:
            master_status = f"error: {str(e)}"
            agent_test_status = "failed"
        
        # Test individual agents
        agents_status = {
            "master_agent": master_status,
            "weather_agent": "healthy",  # Could add specific tests
            "news_agent": "healthy",     # Could add specific tests
            "test_status": agent_test_status
        }
        
        # System metrics
        system_info = {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:').percent,
            "process_count": len(psutil.pids())
        }
        
        # Performance metrics
        performance_info = {
            "uptime_seconds": time.time() - start_time,
            "uptime_formatted": f"{(time.time() - start_time) / 3600:.2f} hours",
            "response_time_ms": 0  # Could implement actual response time tracking
        }
        
        overall_status = "healthy" if master_status == "healthy" else "degraded"
        
        return SystemStatus(
            status=overall_status,
            agents=agents_status,
            system=system_info,
            performance=performance_info
        )
        
    except Exception as e:
        return SystemStatus(
            status="error",
            agents={"error": str(e)},
            system={},
            performance={}
        )

@health_router.get("/health/agents")
async def agents_health_check():
    """Check health of individual agents"""
    try:
        from app import get_master_agent
        
        master_agent = get_master_agent()
        
        # Test each agent individually
        results = {}
        
        # Test weather agent
        try:
            weather_response = await asyncio.wait_for(
                master_agent.weather_agent.get_weather_briefing("Health check test"),
                timeout=10.0
            )
            results["weather_agent"] = {
                "status": "healthy" if weather_response else "error",
                "response_length": len(weather_response) if weather_response else 0
            }
        except Exception as e:
            results["weather_agent"] = {"status": "error", "error": str(e)}
        
        # Test news agent
        try:
            news_response = await asyncio.wait_for(
                master_agent.news_agent.get_news_briefing("Health check test"),
                timeout=10.0
            )
            results["news_agent"] = {
                "status": "healthy" if news_response else "error",
                "response_length": len(news_response) if news_response else 0
            }
        except Exception as e:
            results["news_agent"] = {"status": "error", "error": str(e)}
        
        return {
            "timestamp": datetime.now().isoformat(),
            "agents": results
        }
        
    except Exception as e:
        return {
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "agents": {}
        }

@health_router.get("/health/ready")
async def readiness_check():
    """Kubernetes-style readiness check"""
    try:
        from app import get_master_agent
        master_agent = get_master_agent()
        
        # Quick test of core functionality
        test_response = await asyncio.wait_for(
            master_agent.process_request("Ready check"),
            timeout=3.0
        )
        
        return {"status": "ready", "timestamp": datetime.now().isoformat()}
        
    except Exception as e:
        return {"status": "not_ready", "error": str(e), "timestamp": datetime.now().isoformat()}

@health_router.get("/health/live")
async def liveness_check():
    """Kubernetes-style liveness check"""
    return {
        "status": "alive",
        "timestamp": datetime.now().isoformat(),
        "uptime": time.time() - start_time
    }
