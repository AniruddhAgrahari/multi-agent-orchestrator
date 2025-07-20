import asyncio
import sys
import os

# Add the tools directory to path
sys.path.append('daily_briefing_generator/tools')

from news_tool import get_news_data

async def test_current_system():
    print("🧪 Testing Current Multi-API News System")
    print("=" * 50)
    
    # Test with technology news from India
    result = await get_news_data(
        category='technology', 
        country='in', 
        max_articles=8
    )
    
    print(f"✅ Status: {result['status']}")
    print(f"📰 Total articles: {result.get('total_results', 0)}")
    print(f"🔗 APIs used: {result.get('apis_used', [])}")
    print(f"📡 Sources: {result.get('sources_used', [])}")
    
    print("\n📄 Articles Found:")
    print("-" * 40)
    for i, article in enumerate(result.get('articles', [])[:5], 1):
        title = article.get('title', 'No title')[:70]
        source = article.get('source', {}).get('name', 'Unknown')
        print(f"{i}. {title}...")
        print(f"   📍 Source: {source}")
        print()

if __name__ == "__main__":
    asyncio.run(test_current_system())
