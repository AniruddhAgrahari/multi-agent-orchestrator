"""
Test script for the weather tool
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.weather_tool import get_weather_data

async def test_weather():
    """Test the weather tool with a sample city."""
    print("🌤️ Testing Weather Tool...")
    print("-" * 40)
    
    try:
        # Test with London, UK
        weather_data = await get_weather_data("London", "GB")
        
        if "error" in weather_data:
            print(f"❌ Error: {weather_data['error']}")
        else:
            print("✅ Weather data retrieved successfully!")
            print(f"📍 Location: {weather_data.get('name', 'Unknown')}")
            print(f"🌡️ Temperature: {weather_data.get('main', {}).get('temp', 'N/A')}°C")
            print(f"☁️ Weather: {weather_data.get('weather', [{}])[0].get('description', 'N/A')}")
            print(f"💧 Humidity: {weather_data.get('main', {}).get('humidity', 'N/A')}%")
            
    except Exception as e:
        print(f"❌ Exception occurred: {e}")

if __name__ == "__main__":
    asyncio.run(test_weather())
