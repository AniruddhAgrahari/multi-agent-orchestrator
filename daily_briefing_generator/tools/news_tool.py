# tools/news_tool.py
import asyncio
import aiohttp
import os
from typing import Dict, List, Any
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def get_news_data(
    query: str = "technology", 
    country: str = "us", 
    category: str = "general",
    max_articles: int = 5
) -> Dict[str, Any]:
    """
    Fetch current news articles for your daily briefing.
    
    This tool will be the 'eyes and ears' of your news agent,
    gathering information from the world.
    """
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return {"error": "NewsAPI key not found in environment variables"}
    
    # Build the API URL - using top headlines for daily briefing
    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": api_key,
        "country": country,
        "category": category,
        "pageSize": max_articles,
        "sortBy": "publishedAt"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "status": "success",
                        "total_results": data.get("totalResults", 0),
                        "articles": data.get("articles", [])
                    }
                else:
                    return {"error": f"News API request failed with status {response.status}"}
    except Exception as e:
        return {"error": f"Network error: {str(e)}"}

# Quick test function
async def test_news_tool():
    """Test your news tool before integrating with agent"""
    print("🧪 Testing News Tool...")
    
    result = await get_news_data(category="technology", max_articles=3)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
    else:
        print(f"✅ Success! Found {result['total_results']} articles")
        for i, article in enumerate(result['articles'][:2], 1):
            print(f"\n📰 Article {i}:")
            print(f"Title: {article['title']}")
            print(f"Source: {article['source']['name']}")

if __name__ == "__main__":
    asyncio.run(test_news_tool())
