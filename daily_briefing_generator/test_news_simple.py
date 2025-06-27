"""
Quick test for news agent
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

from agents.news_agent import NewsAgent

async def quick_test():
    print("🧪 Quick News Agent Test")
    print("="*50)
    
    # Check environment variables
    print(f"API Key exists: {bool(os.getenv('GOOGLE_AI_API_KEY'))}")
    print(f"News Key exists: {bool(os.getenv('NEWS_API_KEY'))}")
    
    try:
        agent = NewsAgent()
        print("✅ News agent created successfully!")
        
        # Test the news tool directly first
        from tools.news_tool import get_news_data
        print("\n🔧 Testing news tool directly...")
        direct_result = await get_news_data(query="technology", category="technology", max_articles=3)
        print(f"Direct tool result: {direct_result.get('total_results', 0)} articles found")
        
        # Test a simple request
        print("\n📰 Testing agent...")
        response = await agent.get_news_briefing("Give me today's top technology news")
        print(f"\n📰 Response:\n{response}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(quick_test())
