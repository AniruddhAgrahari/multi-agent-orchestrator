# agents/weather_agent.py
import asyncio
import os
import sys
from typing import Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.weather_tool import get_weather_data

load_dotenv()

class WeatherAgent:
    def __init__(self):
        """
        Your first intelligent agent, Master Aniruddh!
        This agent combines AI reasoning with real-world weather data.
        """
        # Configure Google AI Studio
        api_key = os.getenv("GOOGLE_AI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Google AI API key not found. Please set GOOGLE_AI_API_KEY in your .env file")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-flash-lite-latest')
        
    async def get_weather_briefing(self, user_request: str) -> str:
        """
        This is where your agent becomes intelligent!
        It analyzes the user's request and decides how to respond.
        """
        # First, let the AI understand what the user wants
        analysis_prompt = f"""
        Analyze this weather request: "{user_request}"
        
        Extract:
        1. City name
        2. Country (if mentioned, otherwise assume US)
        3. What specific weather info they want
        
        Respond in this exact format:
        CITY: [city name]
        COUNTRY: [country code]
        REQUEST_TYPE: [brief description]
        """
        
        try:
            # Get AI analysis
            response = await self.model.generate_content_async(analysis_prompt)
            analysis = response.text
            
            # Parse the AI's analysis
            city = self._extract_value(analysis, "CITY:")
            country = self._extract_value(analysis, "COUNTRY:")
            
            if not city:
                return "I couldn't identify which city you're asking about. Could you please specify?"
            
            # Fetch real weather data using your tool
            weather_data = await get_weather_data(city, country or "US")
            
            if "error" in weather_data:
                return f"Sorry, I couldn't get weather data: {weather_data['error']}"
            
            # Let AI create a natural response
            briefing_prompt = f"""
            Create a natural, conversational weather briefing based on this data:
            
            City: {weather_data['name']}, {weather_data['sys']['country']}
            Temperature: {weather_data['main']['temp']}°C
            Feels like: {weather_data['main']['feels_like']}°C
            Weather: {weather_data['weather'][0]['description']}
            Humidity: {weather_data['main']['humidity']}%
            Wind: {weather_data['wind']['speed']} m/s
            
            User's original request: "{user_request}"
            
            Make it conversational and helpful, addressing their specific request.
            """
            
            final_response = await self.model.generate_content_async(briefing_prompt)
            return final_response.text
            
        except Exception as e:
            return f"I encountered an error processing your request: {str(e)}"
    
    def _extract_value(self, text: str, key: str) -> str:
        """Helper method to parse AI responses"""
        lines = text.split('\n')
        for line in lines:
            if line.strip().startswith(key):
                return line.split(':', 1)[1].strip()
        return ""

# Test function
async def test_weather_agent():
    """Test your first intelligent agent!"""
    agent = WeatherAgent()
    
    test_requests = [
        "What's the weather like in New York?",
        "Is it raining in London?",
        "How hot is it in Mumbai today?"
    ]
    
    for request in test_requests:
        print(f"\n🤖 User: {request}")
        response = await agent.get_weather_briefing(request)
        print(f"🌤️  Agent: {response}")
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(test_weather_agent())
