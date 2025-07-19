# tools/enhanced_news_tool.py
import asyncio
import aiohttp
import feedparser
import os
from typing import Dict, List, Any
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MultiSourceNewsAggregator:
    def __init__(self):
        """Enhanced news aggregator using multiple sources for better coverage"""
        self.news_api_key = os.getenv("NEWS_API_KEY")
        self.newsdata_api_key = os.getenv("NEWSDATA_API_KEY")  # Optional: sign up at newsdata.io
        
        # RSS feeds for different categories and regions
        self.rss_feeds = {
            "general": {
                "global": [
                    "https://feeds.bbci.co.uk/news/rss.xml",
                    "https://rss.cnn.com/rss/edition.rss",
                    "https://feeds.reuters.com/reuters/topNews",
                    "https://feeds.nbcnews.com/nbcnews/public/news"
                ],
                "india": [
                    "https://feeds.feedburner.com/ndtvnews-top-stories",
                    "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
                    "https://www.thehindu.com/news/national/?service=rss",
                    "https://indianexpress.com/feed/"
                ],
                "us": [
                    "https://feeds.washingtonpost.com/rss/national",
                    "https://rss.nytimes.com/services/xml/rss/nyt/US.xml"
                ]
            },
            "technology": {
                "global": [
                    "https://feeds.feedburner.com/TechCrunch",
                    "https://feeds.arstechnica.com/arstechnica/index",
                    "https://www.wired.com/feed/rss",
                    "https://feeds.reuters.com/reuters/technologyNews"
                ],
                "india": [
                    "https://economictimes.indiatimes.com/tech/rssfeeds/13357270.cms"
                ]
            },
            "business": {
                "global": [
                    "https://feeds.reuters.com/reuters/businessNews",
                    "https://feeds.bloomberg.com/markets/news.rss",
                    "https://feeds.cnbc.com/cnbc/news"
                ],
                "india": [
                    "https://economictimes.indiatimes.com/rssfeedstopstories.cms",
                    "https://www.business-standard.com/rss/home_page_top_stories.rss"
                ]
            }
        }
    
    async def get_comprehensive_news(self, 
                                   category: str = "general",
                                   region: str = "global",
                                   max_articles: int = 10) -> Dict[str, Any]:
        """
        Get news from multiple sources with comprehensive coverage
        """
        all_articles = []
        sources_tried = []
        
        # Strategy 1: Try RSS feeds first (most reliable)
        rss_articles = await self._fetch_from_rss(category, region, max_articles)
        if rss_articles:
            all_articles.extend(rss_articles)
            sources_tried.append("RSS")
        
        # Strategy 2: Try original News API if we need more articles
        if len(all_articles) < max_articles and self.news_api_key:
            api_articles = await self._fetch_from_newsapi(category, region, max_articles - len(all_articles))
            if api_articles:
                all_articles.extend(api_articles)
                sources_tried.append("NewsAPI")
        
        # Strategy 3: Try NewsData.io if available
        if len(all_articles) < max_articles and self.newsdata_api_key:
            newsdata_articles = await self._fetch_from_newsdata(category, region, max_articles - len(all_articles))
            if newsdata_articles:
                all_articles.extend(newsdata_articles)
                sources_tried.append("NewsData")
        
        # Remove duplicates and sort by publish date
        unique_articles = self._remove_duplicates(all_articles)
        sorted_articles = sorted(unique_articles, key=lambda x: x.get('published_at', ''), reverse=True)
        
        return {
            "status": "success",
            "total_results": len(sorted_articles),
            "articles": sorted_articles[:max_articles],
            "sources_used": sources_tried,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _fetch_from_rss(self, category: str, region: str, max_articles: int) -> List[Dict]:
        """Fetch news from RSS feeds"""
        articles = []
        
        # Get appropriate RSS feeds
        feeds = []
        if category in self.rss_feeds:
            if region in self.rss_feeds[category]:
                feeds.extend(self.rss_feeds[category][region])
            elif region == "india" and "global" in self.rss_feeds[category]:
                feeds.extend(self.rss_feeds[category]["global"])  # Fallback to global
        
        if not feeds and "general" in self.rss_feeds:
            # Fallback to general category
            if region in self.rss_feeds["general"]:
                feeds.extend(self.rss_feeds["general"][region])
            else:
                feeds.extend(self.rss_feeds["general"]["global"])
        
        # Fetch from each RSS feed
        for feed_url in feeds[:3]:  # Limit to 3 feeds to avoid too many requests
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(feed_url, timeout=10) as response:
                        if response.status == 200:
                            content = await response.text()
                            feed = feedparser.parse(content)
                            
                            for entry in feed.entries[:max_articles]:
                                articles.append({
                                    "title": entry.get("title", ""),
                                    "description": entry.get("summary", entry.get("description", "")),
                                    "url": entry.get("link", ""),
                                    "published_at": entry.get("published", ""),
                                    "source": {"name": feed.feed.get("title", "RSS Source")},
                                    "content": entry.get("content", [{}])[0].get("value", "") if entry.get("content") else ""
                                })
            except Exception as e:
                print(f"RSS feed error for {feed_url}: {e}")
                continue
        
        return articles
    
    async def _fetch_from_newsapi(self, category: str, region: str, max_articles: int) -> List[Dict]:
        """Fetch from original News API with improved parameters"""
        try:
            country_code = self._get_country_code(region)
            
            async with aiohttp.ClientSession() as session:
                # Try top headlines first
                params = {
                    "apiKey": self.news_api_key,
                    "country": country_code,
                    "category": category if category != "general" else None,
                    "pageSize": max_articles
                }
                params = {k: v for k, v in params.items() if v is not None}
                
                async with session.get("https://newsapi.org/v2/top-headlines", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        articles = []
                        for article in data.get("articles", []):
                            if article.get("title") and "[Removed]" not in article.get("title", ""):
                                articles.append({
                                    "title": article["title"],
                                    "description": article.get("description", ""),
                                    "url": article.get("url", ""),
                                    "published_at": article.get("publishedAt", ""),
                                    "source": article.get("source", {}),
                                    "content": article.get("content", "")
                                })
                        return articles
        except Exception as e:
            print(f"NewsAPI error: {e}")
        
        return []
    
    async def _fetch_from_newsdata(self, category: str, region: str, max_articles: int) -> List[Dict]:
        """Fetch from NewsData.io API"""
        if not self.newsdata_api_key:
            return []
        
        try:
            country_code = self._get_country_code(region)
            
            async with aiohttp.ClientSession() as session:
                params = {
                    "apikey": self.newsdata_api_key,
                    "country": country_code,
                    "category": category,
                    "language": "en",
                    "size": max_articles
                }
                
                async with session.get("https://newsdata.io/api/1/news", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        articles = []
                        for article in data.get("results", []):
                            articles.append({
                                "title": article.get("title", ""),
                                "description": article.get("description", ""),
                                "url": article.get("link", ""),
                                "published_at": article.get("pubDate", ""),
                                "source": {"name": article.get("source_id", "NewsData")},
                                "content": article.get("content", "")
                            })
                        return articles
        except Exception as e:
            print(f"NewsData error: {e}")
        
        return []
    
    def _get_country_code(self, region: str) -> str:
        """Convert region to appropriate country code"""
        region_map = {
            "india": "in",
            "us": "us",
            "uk": "gb",
            "global": "us"  # Default to US for global
        }
        return region_map.get(region.lower(), "us")
    
    def _remove_duplicates(self, articles: List[Dict]) -> List[Dict]:
        """Remove duplicate articles based on title similarity"""
        seen_titles = set()
        unique_articles = []
        
        for article in articles:
            title = article.get("title", "").lower().strip()
            # Simple duplicate detection
            title_words = set(title.split())
            is_duplicate = False
            
            for seen_title in seen_titles:
                seen_words = set(seen_title.split())
                # If 70% of words match, consider it a duplicate
                if len(title_words & seen_words) / max(len(title_words), len(seen_words)) > 0.7:
                    is_duplicate = True
                    break
            
            if not is_duplicate and title:
                seen_titles.add(title)
                unique_articles.append(article)
        
        return unique_articles


# Enhanced wrapper function to maintain compatibility
async def get_news_data(
    query: str = "technology", 
    country: str = "us", 
    category: str = "general",
    max_articles: int = 5
) -> Dict[str, Any]:
    """
    Enhanced news fetching using multiple sources for better coverage
    """
    aggregator = MultiSourceNewsAggregator()
    
    # Map country codes to regions
    region_map = {
        "in": "india",
        "us": "us", 
        "gb": "uk",
        "uk": "uk"
    }
    region = region_map.get(country, "global")
    
    result = await aggregator.get_comprehensive_news(category, region, max_articles)
    
    # Convert to expected format
    return {
        "status": result["status"],
        "total_results": result["total_results"],
        "articles": result["articles"],
        "sources_used": result.get("sources_used", [])
    }


# Test function
async def test_enhanced_news():
    """Test the enhanced news system"""
    print("🧪 Testing Enhanced Multi-Source News System")
    print("=" * 60)
    
    test_cases = [
        ("technology", "india", 3),
        ("business", "us", 3), 
        ("general", "india", 5)
    ]
    
    for category, region, count in test_cases:
        print(f"\n🔍 Testing: {category} news from {region} ({count} articles)")
        country_code = {"india": "in", "us": "us"}.get(region, "us")
        
        result = await get_news_data(category=category, country=country_code, max_articles=count)
        
        print(f"✅ Status: {result['status']}")
        print(f"📰 Found: {result['total_results']} articles")
        if 'sources_used' in result:
            print(f"🔗 Sources: {', '.join(result['sources_used'])}")
        
        for i, article in enumerate(result.get('articles', [])[:2], 1):
            print(f"\nArticle {i}: {article.get('title', 'No title')[:80]}...")
            print(f"Source: {article.get('source', {}).get('name', 'Unknown')}")
        
        print("-" * 40)


if __name__ == "__main__":
    asyncio.run(test_enhanced_news())
