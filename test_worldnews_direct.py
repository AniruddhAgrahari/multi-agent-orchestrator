import asyncio
import os
import aiohttp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_worldnews_api():
    """Test WorldNews API specifically"""
    print("🔍 Testing WorldNews API")
    print("=" * 40)
    
    # Check for different possible variable names
    possible_keys = [
        'WORLDNEWS_API_KEY',
        'WORLD_NEWS_API_KEY', 
        'WORLDNEWSAPI_KEY',
        'WORLD_NEWS_KEY'
    ]
    
    worldnews_key = None
    key_name = None
    
    for key_var in possible_keys:
        key = os.getenv(key_var)
        if key:
            worldnews_key = key
            key_name = key_var
            break
    
    if not worldnews_key:
        print("❌ WorldNews API key not found")
        print("   Checked variables:", possible_keys)
        return
    
    print(f"🔑 Found {key_name}: {worldnews_key[:10]}...{worldnews_key[-5:]}")
    
    try:
        async with aiohttp.ClientSession() as session:
            params = {
                "api-key": worldnews_key,
                "number": 3,
                "language": "en",
                "sort": "publish-time",
                "sort-direction": "DESC",
                "location-filter": "IN",  # India
                "text": "technology"
            }
            
            print("🔍 Testing WorldNews API call...")
            async with session.get("https://api.worldnewsapi.com/search-news", params=params, timeout=15) as response:
                print(f"Status: {response.status}")
                if response.status == 200:
                    data = await response.json()
                    news = data.get('news', [])
                    print(f"✅ Working: {len(news)} articles found")
                    
                    for i, article in enumerate(news[:2], 1):
                        print(f"Article {i}: {article.get('title', 'No title')}")
                        print(f"   Source: {article.get('source_country', 'Unknown')}")
                else:
                    error_text = await response.text()
                    print(f"❌ Error: {error_text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_worldnews_api())
