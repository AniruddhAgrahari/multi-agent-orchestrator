import asyncio
import sys
import os
sys.path.append('daily_briefing_generator/tools')
from enhanced_news_tool import MultiSourceNewsAggregator

async def test_individual_apis():
    print("🔍 Testing Individual APIs")
    print("=" * 40)
    
    aggregator = MultiSourceNewsAggregator()
    
    # Test GNews API specifically
    print("\n🧪 Testing GNews API:")
    try:
        result = await aggregator._fetch_from_gnews("technology", "india", 3)
        print(f"   Articles found: {len(result.get('articles', []))}")
        for article in result.get('articles', [])[:2]:
            print(f"   - {article.get('title', 'No title')[:50]}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test NewsData API
    print("\n🧪 Testing NewsData API:")
    try:
        result = await aggregator._fetch_from_newsdata("technology", "india", 3)
        print(f"   Articles found: {len(result.get('articles', []))}")
        for article in result.get('articles', [])[:2]:
            print(f"   - {article.get('title', 'No title')[:50]}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test NewsAPI
    print("\n🧪 Testing NewsAPI:")
    try:
        result = await aggregator._fetch_from_newsapi("technology", "india", 3)
        print(f"   Articles found: {len(result)}")
        for article in result[:2]:
            print(f"   - {article.get('title', 'No title')[:50]}...")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_individual_apis())
