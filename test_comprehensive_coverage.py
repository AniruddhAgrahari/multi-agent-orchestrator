import asyncio
import sys
import os

# Add the tools directory to path
sys.path.append('daily_briefing_generator/tools')

from news_tool import get_news_data

async def test_comprehensive_categories():
    print("🧪 Testing Comprehensive Multi-API News Coverage")
    print("=" * 60)
    
    test_cases = [
        ("technology", "in", "Technology News from India"),
        ("business", "us", "Business News from US"),
        ("general", "in", "General News from India"),
        ("health", "in", "Health News from India")
    ]
    
    for category, country, description in test_cases:
        print(f"\n🔍 {description}")
        print("-" * 40)
        
        result = await get_news_data(
            category=category, 
            country=country, 
            max_articles=6
        )
        
        print(f"✅ Status: {result['status']}")
        print(f"📰 Articles: {result.get('total_results', 0)}")
        print(f"🔗 APIs: {result.get('apis_used', [])}")
        print(f"📡 Sources: {result.get('sources_used', [])}")
        
        # Show top 3 articles
        for i, article in enumerate(result.get('articles', [])[:3], 1):
            title = article.get('title', 'No title')[:60]
            source = article.get('source', {}).get('name', 'Unknown')
            print(f"  {i}. {title}... [{source}]")
        
        print()

if __name__ == "__main__":
    asyncio.run(test_comprehensive_categories())
