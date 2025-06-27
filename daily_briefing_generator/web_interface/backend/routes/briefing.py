"""
Daily Briefing API Routes
========================

REST API endpoints for the Daily Briefing Agent system.
Provides weather, news, and comprehensive briefing services.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
import asyncio
import logging

# Configure logging
logger = logging.getLogger(__name__)

briefing_router = APIRouter(tags=["briefing"])

# Request/Response models
class BriefingRequest(BaseModel):
    query: str
    location: Optional[str] = None
    categories: Optional[List[str]] = None
    use_recovery: Optional[bool] = True

class BriefingResponse(BaseModel):
    success: bool
    content: str
    metadata: dict

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None

@briefing_router.post("/briefing", response_model=BriefingResponse)
async def create_briefing(request: BriefingRequest):
    """
    Generate a comprehensive daily briefing
    
    - **query**: Natural language request for briefing
    - **location**: Optional specific location for weather
    - **categories**: Optional news categories filter
    - **use_recovery**: Enable error recovery (default: True)
    """
    try:
        # Import here to avoid circular imports
        from app import get_master_agent
        
        master_agent = get_master_agent()
        
        # Build query with optional parameters
        enhanced_query = request.query
        if request.location:
            enhanced_query += f" for {request.location}"
        if request.categories:
            enhanced_query += f" with {', '.join(request.categories)} news"
        
        logger.info(f"Processing briefing request: {enhanced_query}")
        
        # Generate briefing with or without recovery
        if request.use_recovery:
            content = await master_agent.run_with_recovery(enhanced_query)
        else:
            content = await master_agent.process_request(enhanced_query)
        
        return BriefingResponse(
            success=True,
            content=content,
            metadata={
                "query": enhanced_query,
                "location": request.location,
                "categories": request.categories,
                "recovery_enabled": request.use_recovery
            }
        )
        
    except Exception as e:
        logger.error(f"Briefing generation failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate briefing: {str(e)}"
        )

@briefing_router.get("/briefing/quick/{briefing_type}")
async def quick_briefing(briefing_type: str, location: Optional[str] = None):
    """
    Generate quick briefings for common requests
    
    - **briefing_type**: weather, news, business, technology, or complete
    - **location**: Optional location for weather briefings
    """
    try:
        from app import get_master_agent
        
        master_agent = get_master_agent()
        
        # Define quick briefing templates
        templates = {
            "weather": f"Weather for {location or 'default location'}",
            "news": "Today's top news",
            "business": "Business news updates",
            "technology": "Technology news briefing",
            "complete": f"Complete daily briefing for {location or 'default location'}"
        }
        
        if briefing_type not in templates:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid briefing type. Available: {list(templates.keys())}"
            )
        
        query = templates[briefing_type]
        logger.info(f"Processing quick briefing: {query}")
        
        content = await master_agent.run_with_recovery(query)
        
        return BriefingResponse(
            success=True,
            content=content,
            metadata={
                "briefing_type": briefing_type,
                "location": location,
                "query": query
            }
        )
        
    except Exception as e:
        logger.error(f"Quick briefing failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate quick briefing: {str(e)}"
        )

@briefing_router.post("/briefing/stream")
async def stream_briefing(request: BriefingRequest):
    """
    Generate briefing with streaming response (future implementation)
    """
    # Placeholder for streaming implementation
    raise HTTPException(
        status_code=501,
        detail="Streaming briefings not yet implemented"
    )

@briefing_router.get("/briefing/templates")
async def get_briefing_templates():
    """Get available briefing templates"""
    return {
        "templates": [
            {
                "id": "morning",
                "name": "Morning Briefing",
                "description": "Complete morning briefing with weather and news",
                "example": "Morning briefing for London with technology news"
            },
            {
                "id": "weather_only",
                "name": "Weather Focus",
                "description": "Weather-focused briefing for planning",
                "example": "Weather conditions for Tokyo for business travel"
            },
            {
                "id": "news_only",
                "name": "News Digest",
                "description": "News-only briefing for specific categories",
                "example": "Business and technology news updates"
            },
            {
                "id": "executive",
                "name": "Executive Briefing",
                "description": "High-level executive briefing with insights",
                "example": "Executive briefing for New York with market analysis"
            }
        ],
        "categories": [
            "technology", "business", "health", "sports", "general"
        ],
        "common_locations": [
            "London", "New York", "Tokyo", "Mumbai", "Paris", "Singapore"
        ]
    }
