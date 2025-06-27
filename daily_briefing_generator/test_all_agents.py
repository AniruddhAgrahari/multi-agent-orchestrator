"""
Test all agents with the new API key
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_all_agents():
    print("🔑 TESTING ALL AGENTS WITH NEW API KEY")
    print("=" * 50)
    
    # Check API key loading
    api_key = os.getenv('GOOGLE_AI_API_KEY')
    print(f"✅ API Key loaded: {api_key[:20]}..." if api_key else "❌ No API key found")
    print()
    
    try:
        # Test Weather Agent
        print("🌤️ TESTING WEATHER AGENT")
        print("-" * 30)
        from agents.weather_agent import WeatherAgent
        weather_agent = WeatherAgent()
        weather_result = await weather_agent.get_weather_briefing("What's the weather in Tokyo?")
        print(f"✅ Weather Agent Response:")
        print(f"{weather_result[:200]}...")
        print()
        
        # Test News Agent
        print("📰 TESTING NEWS AGENT")
        print("-" * 30)
        from agents.news_agent import NewsAgent
        news_agent = NewsAgent()
        news_result = await news_agent.get_news_briefing("Give me technology news")
        print(f"✅ News Agent Response:")
        print(f"{news_result[:200]}...")
        print()
        
        # Test Master Agent
        print("🎯 TESTING MASTER AGENT")
        print("-" * 30)
        from orchestrator.master_agent import MasterAgent
        master_agent = MasterAgent()
        master_result = await master_agent.run("Give me a brief weather update for London")
        print(f"✅ Master Agent Response:")
        print(f"{master_result[:200]}...")
        print()
        
        print("🎉 ALL AGENTS WORKING SUCCESSFULLY WITH NEW API KEY!")
        
    except Exception as e:
        print(f"❌ Error testing agents: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_all_agents())
