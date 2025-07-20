import asyncio
import sys
import os
sys.path.append('tools')
from news_tool import get_news_data

async def test():
    print("🧪 Testing Integrated Multi-API News System")
    print("=" * 50)
    
    result = await get_news_data(category='technology', country='in', max_articles=5)
    
    print(f"Status: {result['status']}")
    print(f"Total articles: {result.get('total_results', 0)}")
    print(f"APIs used: {result.get('apis_used', [])}")
    print(f"Sources: {result.get('sources_used', [])}")
    
    print("\nTop Articles:")
    for i, article in enumerate(result.get('articles', [])[:3], 1):
        print(f"{i}. {article['title'][:80]}...")
        print(f"   Source: {article.get('source', {}).get('name', 'Unknown')}")

if __name__ == "__main__":
    asyncio.run(test())
