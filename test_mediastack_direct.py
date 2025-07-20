import asyncio
import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()

async def test_mediastack_direct():
    """Test MediaStack API directly"""
    api_key = os.getenv("MEDIASTACK_API_KEY")
    if not api_key:
        print("❌ MediaStack API key not found")
        return
    
    print(f"🔑 MediaStack API Key: {api_key[:10]}...{api_key[-5:]}")
    
    try:
        async with aiohttp.ClientSession() as session:
            params = {
                "access_key": api_key,
                "countries": "in",
                "limit": 3,
                "languages": "en",
                "sort": "published_desc"
            }
            
            print("🔍 Testing MediaStack API call...")
            async with session.get("http://api.mediastack.com/v1/news", params=params, timeout=15) as response:
                print(f"Status: {response.status}")
                if response.status == 200:
                    data = await response.json()
                    articles = data.get('data', [])
                    print(f"Articles returned: {len(articles)}")
                    
                    for i, article in enumerate(articles[:2], 1):
                        print(f"Article {i}: {article.get('title', 'No title')}")
                        print(f"   Source: {article.get('source', 'Unknown')}")
                else:
                    error_text = await response.text()
                    print(f"Error: {error_text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_mediastack_direct())
