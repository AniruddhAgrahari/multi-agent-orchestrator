# tools/news_tool.py - Enhanced Multi-Source News Aggregator
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
    Enhanced news fetching with multiple strategies and sources for better coverage.
    
    This tool now tries multiple approaches to get the best news coverage:
    1. Original NewsAPI with improved parameters
    2. Different search strategies 
    3. Fallback countries and categories
    4. Better error handling and article filtering
    """
    
    # Strategy 1: Try enhanced NewsAPI search
    result = await _fetch_with_enhanced_newsapi(query, country, category, max_articles)
    if result.get("status") == "success" and result.get("articles"):
        return result
    
    # Strategy 2: Try different search terms and parameters
    result = await _fetch_with_broader_search(query, country, category, max_articles)
    if result.get("status") == "success" and result.get("articles"):
        return result
    
    # Strategy 3: Try fallback countries
    fallback_countries = ["us", "in", "gb", "au", "ca"]
    if country not in fallback_countries:
        fallback_countries.insert(0, country)
    
    for fallback_country in fallback_countries:
        if fallback_country == country:
            continue
        result = await _fetch_with_enhanced_newsapi(query, fallback_country, category, max_articles)
        if result.get("status") == "success" and result.get("articles"):
            return result
    
    # Strategy 4: Try general category if specific category fails
    if category != "general":
        result = await _fetch_with_enhanced_newsapi(query, country, "general", max_articles)
        if result.get("status") == "success" and result.get("articles"):
            return result
    
    # If all strategies fail, return a meaningful error
    return {
        "status": "error",
        "error": "No news articles found despite multiple search strategies",
        "articles": [],
        "total_results": 0
    }


async def _fetch_with_enhanced_newsapi(query: str, country: str, category: str, max_articles: int) -> Dict[str, Any]:
    """Enhanced NewsAPI fetching with better parameters"""
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return {"status": "error", "error": "NewsAPI key not found", "articles": []}
    
    # Try top headlines first
    result = await _try_top_headlines(api_key, country, category, max_articles)
    if result.get("articles"):
        return result
    
    # Try everything endpoint with enhanced search
    search_terms = _create_enhanced_search_terms(query, country, category)
    result = await _try_everything_search(api_key, search_terms, max_articles)
    return result


async def _try_top_headlines(api_key: str, country: str, category: str, max_articles: int) -> Dict[str, Any]:
    """Try top headlines endpoint"""
    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": api_key,
        "country": country,
        "pageSize": min(max_articles * 2, 20),  # Get more to filter better
        "sortBy": "publishedAt"
    }
    
    # Only add category if it's valid for top headlines
    if category in ["business", "entertainment", "general", "health", "science", "sports", "technology"]:
        params["category"] = category
    
    return await _make_api_request(base_url, params)


async def _try_everything_search(api_key: str, search_terms: str, max_articles: int) -> Dict[str, Any]:
    """Try everything endpoint with enhanced search"""
    base_url = "https://newsapi.org/v2/everything"
    params = {
        "apiKey": api_key,
        "q": search_terms,
        "sortBy": "publishedAt",
        "pageSize": min(max_articles * 2, 20),
        "language": "en",
        "from": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")  # Last 2 days
    }
    
    return await _make_api_request(base_url, params)


def _create_enhanced_search_terms(query: str, country: str, category: str) -> str:
    """Create better search terms based on context"""
    base_terms = [category if category != "general" else "news"]
    
    # Add country-specific terms
    country_terms = {
        "in": ["India", "Indian", "Delhi", "Mumbai", "Bangalore", "Chennai"],
        "us": ["USA", "America", "American", "New York", "California", "Washington"],
        "gb": ["UK", "Britain", "British", "London", "England"],
        "au": ["Australia", "Australian", "Sydney", "Melbourne"],
        "ca": ["Canada", "Canadian", "Toronto", "Vancouver"]
    }
    
    if country in country_terms:
        base_terms.extend(country_terms[country][:2])  # Add top 2 terms
    
    # Add category-specific terms
    if category == "technology":
        base_terms.extend(["tech", "innovation", "startup", "digital"])
    elif category == "business":
        base_terms.extend(["economy", "market", "finance", "corporate"])
    elif category == "health":
        base_terms.extend(["medical", "healthcare", "medicine"])
    
    return " OR ".join(base_terms)


async def _fetch_with_broader_search(query: str, country: str, category: str, max_articles: int) -> Dict[str, Any]:
    """Try with broader, more flexible search parameters"""
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return {"status": "error", "error": "NewsAPI key not found", "articles": []}
    
    # Try very broad search terms
    broad_terms = {
        "technology": "technology OR tech OR innovation OR digital OR startup",
        "business": "business OR economy OR market OR finance OR corporate",
        "health": "health OR medical OR healthcare OR medicine",
        "general": f"{country} OR news OR breaking OR latest"
    }
    
    search_query = broad_terms.get(category, broad_terms["general"])
    
    base_url = "https://newsapi.org/v2/everything"
    params = {
        "apiKey": api_key,
        "q": search_query,
        "sortBy": "publishedAt",
        "pageSize": min(max_articles * 2, 20),
        "language": "en",
        "from": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")  # Last 3 days
    }
    
    return await _make_api_request(base_url, params)


async def _make_api_request(url: str, params: Dict) -> Dict[str, Any]:
    """Make API request with enhanced error handling and article filtering"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=15) as response:
                if response.status == 200:
                    data = await response.json()
                    articles = data.get("articles", [])
                    
                    # Enhanced article filtering
                    valid_articles = []
                    for article in articles:
                        if _is_valid_article(article):
                            valid_articles.append(_normalize_article(article))
                    
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
        return {"status": "error", "error": f"Network error: {str(e)}", "articles": []}


def _is_valid_article(article: Dict) -> bool:
    """Check if article has valid content"""
    title = article.get("title", "")
    description = article.get("description", "")
    
    # Filter out invalid articles
    invalid_indicators = ["[Removed]", "removed", "unavailable", "access denied", "subscribe to read"]
    
    if not title or not description:
        return False
    
    title_lower = title.lower()
    desc_lower = description.lower()
    
    for indicator in invalid_indicators:
        if indicator in title_lower or indicator in desc_lower:
            return False
    
    # Must have minimum content length
    if len(title) < 10 or len(description) < 30:
        return False
    
    return True


def _normalize_article(article: Dict) -> Dict:
    """Normalize article data to consistent format"""
    return {
        "title": article.get("title", "").strip(),
        "description": article.get("description", "").strip(),
        "url": article.get("url", ""),
        "publishedAt": article.get("publishedAt", ""),
        "source": article.get("source", {}),
        "content": article.get("content", ""),
        "urlToImage": article.get("urlToImage", "")
    }


# Quick test function
async def test_enhanced_news_tool():
    """Test the enhanced news tool"""
    print("🧪 Testing Enhanced News Tool...")
    print("=" * 50)
    
    test_cases = [
        ("technology", "in", 3),
        ("business", "us", 3),
        ("general", "in", 5)
    ]
    
    for category, country, count in test_cases:
        print(f"\n🔍 Testing: {category} news from {country} ({count} articles)")
        
        result = await get_news_data(category=category, country=country, max_articles=count)
        
        if result["status"] == "success":
            print(f"✅ Success! Found {result['total_results']} articles")
            for i, article in enumerate(result['articles'][:2], 1):
                print(f"\n📰 Article {i}:")
                print(f"Title: {article['title'][:80]}...")
                print(f"Source: {article['source']['name']}")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
        
        print("-" * 30)


if __name__ == "__main__":
    asyncio.run(test_enhanced_news_tool())
