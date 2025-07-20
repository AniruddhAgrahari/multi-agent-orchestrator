import asyncio
import os
import aiohttp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_world_news_api_fixed():
    """Test World News API with correct parameters"""
    print("🔍 Testing World News API (Fixed)")
    print("=" * 40)
    
    worldnews_key = os.getenv('WORLD_NEWS_API_KEY')
    
    if not worldnews_key:
        print("❌ WORLD_NEWS_API_KEY not found")
        return
    
    print(f"🔑 Found WORLD_NEWS_API_KEY: {worldnews_key[:10]}...{worldnews_key[-5:]}")
    
    try:
        async with aiohttp.ClientSession() as session:
            # Try without location filter first
            params = {
                "api-key": worldnews_key,
                "number": 3,
                "language": "en",
                "sort": "publish-time",
                "sort-direction": "DESC",
                "text": "technology India"  # Include India in search terms instead
            }
            
            print("🔍 Testing World News API call (global search)...")
            async with session.get("https://api.worldnewsapi.com/search-news", params=params, timeout=15) as response:
                print(f"Status: {response.status}")
                if response.status == 200:
                    data = await response.json()
                    news = data.get('news', [])
                    print(f"✅ Working: {len(news)} articles found")
                    
                    for i, article in enumerate(news[:3], 1):
                        title = article.get('title', 'No title')[:70]
                        source = article.get('source_country', 'Unknown')
                        print(f"Article {i}: {title}...")
                        print(f"   Source: {source}")
                elif response.status == 401:
                    print("❌ Unauthorized - API key might be invalid")
                elif response.status == 402:
                    print("❌ Payment required - free tier limit exceeded")
                else:
                    error_text = await response.text()
                    print(f"❌ Error {response.status}: {error_text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_world_news_api_fixed())
