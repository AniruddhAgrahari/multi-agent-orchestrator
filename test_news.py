import asyncio
from news_tool import get_news_data

async def test():
    result = await get_news_data(query='technology', country='in', category='technology', max_articles=3)
    print(f'Status: {result["status"]}')
    print(f'Articles found: {result.get("total_results", 0)}')
    for article in result.get('articles', [])[:3]:
        print(f'- {article["title"][:60]}...')

if __name__ == "__main__":
    asyncio.run(test())
