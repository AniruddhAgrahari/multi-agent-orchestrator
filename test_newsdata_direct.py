import asyncio
import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()

async def test_newsdata_direct():
    """Test NewsData API directly"""
    api_key = os.getenv("NEWSDATA_API_KEY")
    if not api_key:
        print("❌ NewsData API key not found")
        return
    
    print(f"🔑 NewsData API Key: {api_key[:10]}...{api_key[-5:]}")
    
    try:
        async with aiohttp.ClientSession() as session:
            params = {
                "apikey": api_key,
                "country": "in",
                "category": "technology",
                "language": "en",
                "size": 3
            }
            
            print("🔍 Testing NewsData API call...")
            async with session.get("https://newsdata.io/api/1/news", params=params, timeout=15) as response:
                print(f"Status: {response.status}")
                if response.status == 200:
                    data = await response.json()
                    print(f"Status from API: {data.get('status')}")
                    articles = data.get('results', [])
                    print(f"Articles returned: {len(articles)}")
                    
                    for i, article in enumerate(articles[:2], 1):
                        print(f"Article {i}: {article.get('title', 'No title')}")
                else:
                    error_text = await response.text()
                    print(f"Error: {error_text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_newsdata_direct())
