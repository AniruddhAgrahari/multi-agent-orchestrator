import asyncio
import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()

async def test_gnews_direct():
    """Test GNews API directly"""
    api_key = os.getenv("GNEWS_API_KEY")
    if not api_key:
        print("❌ GNews API key not found")
        return
    
    print(f"🔑 GNews API Key: {api_key[:10]}...{api_key[-5:]}")
    
    try:
        async with aiohttp.ClientSession() as session:
            params = {
                "token": api_key,
                "lang": "en",
                "country": "in",
                "max": 3,
                "q": "technology"
            }
            
            print("🔍 Testing GNews API call...")
            async with session.get("https://gnews.io/api/v4/top-headlines", params=params, timeout=15) as response:
                print(f"Status: {response.status}")
                if response.status == 200:
                    data = await response.json()
                    print(f"Total results: {data.get('totalArticles', 0)}")
                    articles = data.get('articles', [])
                    print(f"Articles returned: {len(articles)}")
                    
                    for i, article in enumerate(articles[:2], 1):
                        print(f"Article {i}: {article.get('title', 'No title')}")
                else:
                    error_text = await response.text()
                    print(f"Error: {error_text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_gnews_direct())
