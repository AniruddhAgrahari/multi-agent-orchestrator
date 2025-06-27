# tools/weather_tool.py
import asyncio
import aiohttp
import os
from typing import Dict, Any

async def get_weather_data(city: str, country_code: str = "US") -> Dict[str, Any]:
    """
    Fetch current weather data for a specified city.
    
    This is your agent's 'hand' to reach into the real world and grab weather data.
    """
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        raise ValueError("OpenWeatherMap API key not found in environment variables")
    
    # Build the API URL
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": f"{city},{country_code}",
        "appid": api_key,
        "units": "metric"  # Celsius temperatures
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {"error": f"API request failed with status {response.status}"}
    except Exception as e:
        return {"error": f"Network error: {str(e)}"}
