import asyncio
import os
import aiohttp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_all_new_apis():
    """Test all configured APIs directly"""
    print("🔍 Testing All Configured APIs")
    print("=" * 50)
    
    # Test GNews (previously working)
    print("\n1. 🧪 Testing GNews API:")
    gnews_key = os.getenv("GNEWS_API_KEY")
    if gnews_key:
        try:
            async with aiohttp.ClientSession() as session:
                params = {
                    "token": gnews_key,
                    "lang": "en",
                    "country": "in",
                    "max": 2,
                    "q": "technology"
                }
                async with session.get("https://gnews.io/api/v4/top-headlines", params=params, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"   ✅ Working: {len(data.get('articles', []))} articles")
                    else:
                        print(f"   ❌ Error: Status {response.status}")
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    else:
        print("   ❌ Key not found")
    
    # Test NewsData (previously working)
    print("\n2. 🧪 Testing NewsData API:")
    newsdata_key = os.getenv("NEWSDATA_API_KEY")
    if newsdata_key:
        try:
            async with aiohttp.ClientSession() as session:
                params = {
                    "apikey": newsdata_key,
                    "country": "in",
                    "category": "technology",
                    "language": "en",
                    "size": 2
                }
                async with session.get("https://newsdata.io/api/1/news", params=params, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"   ✅ Working: {len(data.get('results', []))} articles")
                    else:
                        print(f"   ❌ Error: Status {response.status}")
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    else:
        print("   ❌ Key not found")
    
    # Test MediaStack
    print("\n3. 🧪 Testing MediaStack API:")
    mediastack_key = os.getenv("MEDIASTACK_API_KEY")
    if mediastack_key:
        try:
            async with aiohttp.ClientSession() as session:
                params = {
                    "access_key": mediastack_key,
                    "countries": "in",
                    "limit": 2,
                    "languages": "en",
                    "sort": "published_desc"
                }
                async with session.get("http://api.mediastack.com/v1/news", params=params, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"   ✅ Working: {len(data.get('data', []))} articles")
                    else:
                        error_text = await response.text()
                        print(f"   ❌ Error: {error_text}")
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    else:
        print("   ❌ Key not found")
    
    # Test the 4th API that was added
    print("\n4. 🧪 Testing Additional APIs:")
    additional_apis = [
        ("Currents", "CURRENTS_API_KEY"),
        ("WorldNews", "WORLDNEWS_API_KEY"), 
        ("NewsCatcher", "NEWSCATCHER_API_KEY")
    ]
    
    for name, env_var in additional_apis:
        key = os.getenv(env_var)
        if key:
            print(f"   🔑 {name}: Found key {key[:10]}...{key[-5:]}")
        else:
            print(f"   ❌ {name}: Not configured")

if __name__ == "__main__":
    asyncio.run(test_all_new_apis())
