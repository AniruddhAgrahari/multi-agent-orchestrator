# tools/news_tool.py
import asyncio
import aiohttp
import os
from typing import Dict, List, Any
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def get_news_data(
    query: str = "technology", 
    country: str = "us", 
    category: str = "general",
    max_articles: int = 5
) -> Dict[str, Any]:
    """
    Enhanced news fetching with multiple strategies and fallbacks.
    
    This tool will be the 'eyes and ears' of your news agent,
    gathering information from the world with robust error handling.
    """
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return {"error": "NewsAPI key not found in environment variables"}
    
    # Strategy 1: Try top headlines for specific country/category
    result = await _fetch_top_headlines(api_key, country, category, max_articles)
    if result.get("status") == "success" and result.get("articles"):
        return result
    
    # Strategy 2: Try everything endpoint with broader search
    result = await _fetch_everything_search(api_key, query, country, max_articles)
    if result.get("status") == "success" and result.get("articles"):
        return result
    
    # Strategy 3: Try different country if original fails
    fallback_countries = ["us", "in", "gb", "au", "ca"]
    if country not in fallback_countries:
        fallback_countries.insert(0, country)
    
    for fallback_country in fallback_countries:
        if fallback_country == country:
            continue
        result = await _fetch_top_headlines(api_key, fallback_country, category, max_articles)
        if result.get("status") == "success" and result.get("articles"):
            return result
    
    # Strategy 4: Try general category if specific category fails
    if category != "general":
        result = await _fetch_top_headlines(api_key, country, "general", max_articles)
        if result.get("status") == "success" and result.get("articles"):
            return result
    
    # If all strategies fail, return a meaningful error
    return {
        "status": "error",
        "error": "No news articles found despite multiple search strategies",
        "articles": []
    }


async def _fetch_top_headlines(api_key: str, country: str, category: str, max_articles: int) -> Dict[str, Any]:
    """Fetch top headlines with specific country and category"""
    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": api_key,
        "country": country,
        "category": category,
        "pageSize": max_articles,
        "sortBy": "publishedAt"
    }
    
    return await _make_api_request(base_url, params)


async def _fetch_everything_search(api_key: str, query: str, country: str, max_articles: int) -> Dict[str, Any]:
    """Fetch from everything endpoint with keyword search"""
    base_url = "https://newsapi.org/v2/everything"
    
    # Create better search queries based on country
    search_terms = _get_country_specific_terms(query, country)
    
    params = {
        "apiKey": api_key,
        "q": search_terms,
        "sortBy": "publishedAt",
        "pageSize": max_articles,
        "language": "en",
        "from": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")  # Last 3 days
    }
    
    return await _make_api_request(base_url, params)


def _get_country_specific_terms(query: str, country: str) -> str:
    """Generate better search terms based on country and query"""
    country_terms = {
        "in": ["India", "Indian", "Delhi", "Mumbai", "Bangalore"],
        "us": ["America", "American", "USA", "New York", "California"],
        "gb": ["Britain", "British", "UK", "London", "England"],
        "au": ["Australia", "Australian", "Sydney", "Melbourne"],
        "ca": ["Canada", "Canadian", "Toronto", "Vancouver"]
    }
    
    base_terms = [query, "business", "technology", "latest"]
    if country in country_terms:
        base_terms.extend(country_terms[country][:2])  # Add top 2 country-specific terms
    
    return " OR ".join(base_terms)


async def _make_api_request(url: str, params: Dict) -> Dict[str, Any]:
    """Make API request with proper error handling"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    articles = data.get("articles", [])
                    # Filter out articles with missing content
                    valid_articles = [
                        article for article in articles 
                        if article.get("title") and article.get("description") and 
                        "[Removed]" not in article.get("title", "") and
                        "[Removed]" not in article.get("description", "")
                    ]
                    return {
                        "status": "success",
                        "total_results": len(valid_articles),
                        "articles": valid_articles
                    }
                elif response.status == 426:
                    return {"status": "error", "error": "API rate limit exceeded", "articles": []}
                elif response.status == 401:
                    return {"status": "error", "error": "Invalid API key", "articles": []}
                else:
                    return {"status": "error", "error": f"API request failed with status {response.status}", "articles": []}
    except asyncio.TimeoutError:
        return {"status": "error", "error": "Request timeout", "articles": []}
    except Exception as e:
        return {"error": f"Network error: {str(e)}"}

# Quick test function
async def test_news_tool():
    """Test your news tool before integrating with agent"""
    print("🧪 Testing News Tool...")
    
    result = await get_news_data(category="technology", max_articles=3)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
    else:
        print(f"✅ Success! Found {result['total_results']} articles")
        for i, article in enumerate(result['articles'][:2], 1):
            print(f"\n📰 Article {i}:")
            print(f"Title: {article['title']}")
            print(f"Source: {article['source']['name']}")

if __name__ == "__main__":
    asyncio.run(test_news_tool())
