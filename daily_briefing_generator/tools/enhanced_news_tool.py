# tools/enhanced_news_tool.py - Comprehensive Multi-API News System
import asyncio
import aiohttp
import feedparser
import os
import json
from typing import Dict, List, Any
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MultiSourceNewsAggregator:
    def __init__(self):
        """Enhanced news aggregator using multiple APIs and sources for maximum coverage"""
        # Multiple News APIs
        self.news_api_key = os.getenv("NEWS_API_KEY")  # newsapi.org
        self.newsdata_api_key = os.getenv("NEWSDATA_API_KEY")  # newsdata.io
        self.gnews_api_key = os.getenv("GNEWS_API_KEY")  # gnews.io
        self.mediastack_api_key = os.getenv("MEDIASTACK_API_KEY")  # mediastack.com
        self.currents_api_key = os.getenv("CURRENTS_API_KEY")  # currentsapi.services
        self.worldnews_api_key = os.getenv("WORLDNEWS_API_KEY") or os.getenv("WORLD_NEWS_API_KEY")  # worldnewsapi.com
        self.newscatcher_api_key = os.getenv("NEWSCATCHER_API_KEY")  # newscatcherapi.com
        
        # Enhanced RSS feeds for different categories and regions
        self.rss_feeds = {
            "general": {
                "global": [
                    "https://feeds.bbci.co.uk/news/rss.xml",
                    "https://rss.cnn.com/rss/edition.rss", 
                    "https://feeds.reuters.com/reuters/topNews",
                    "https://feeds.nbcnews.com/nbcnews/public/news",
                    "https://feeds.skynews.com/feeds/rss/world.xml",
                    "https://feeds.feedburner.com/time/world",
                    "https://feeds.washingtonpost.com/rss/world"
                ],
                "india": [
                    "https://feeds.feedburner.com/ndtvnews-top-stories",
                    "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
                    "https://www.thehindu.com/news/national/?service=rss",
                    "https://indianexpress.com/feed/",
                    "https://www.hindustantimes.com/feeds/rss/india-news/index.xml",
                    "https://www.business-standard.com/rss/latest.rss"
                ],
                "us": [
                    "https://feeds.washingtonpost.com/rss/national",
                    "https://rss.nytimes.com/services/xml/rss/nyt/US.xml",
                    "https://feeds.usatoday.com/usatoday-NewsTopStories",
                    "https://feeds.foxnews.com/foxnews/politics"
                ],
                "uk": [
                    "https://feeds.bbci.co.uk/news/uk/rss.xml",
                    "https://www.theguardian.com/uk/rss",
                    "https://feeds.skynews.com/feeds/rss/uk.xml"
                ]
            },
            "technology": {
                "global": [
                    "https://feeds.feedburner.com/TechCrunch",
                    "https://feeds.arstechnica.com/arstechnica/index",
                    "https://www.wired.com/feed/rss",
                    "https://feeds.reuters.com/reuters/technologyNews",
                    "https://feeds.feedburner.com/venturebeat/SZYF",
                    "https://www.theverge.com/rss/index.xml",
                    "https://feeds.mashable.com/Mashable",
                    "https://techcrunch.com/feed/"
                ],
                "india": [
                    "https://economictimes.indiatimes.com/tech/rssfeeds/13357270.cms",
                    "https://www.financialexpress.com/industry/technology/feed/"
                ]
            },
            "business": {
                "global": [
                    "https://feeds.reuters.com/reuters/businessNews",
                    "https://feeds.bloomberg.com/markets/news.rss",
                    "https://feeds.cnbc.com/cnbc/news",
                    "https://feeds.fortune.com/fortune/feed",
                    "https://feeds.feedburner.com/entrepreneur/latest",
                    "https://feeds.forbes.com/forbesbusiness/feed2.xml"
                ],
                "india": [
                    "https://economictimes.indiatimes.com/rssfeedstopstories.cms",
                    "https://www.business-standard.com/rss/home_page_top_stories.rss",
                    "https://www.financialexpress.com/market/feed/"
                ]
            },
            "health": {
                "global": [
                    "https://feeds.reuters.com/reuters/health",
                    "https://www.who.int/rss-feeds/news-english.xml",
                    "https://feeds.webmd.com/rss/rss.aspx?RSSSource=RSS_PUBLIC"
                ]
            },
            "sports": {
                "global": [
                    "https://feeds.bbci.co.uk/sport/rss.xml",
                    "https://feeds.reuters.com/reuters/sportsNews",
                    "http://rss.espn.com/rss/news"
                ]
            }
        }
    
    async def get_comprehensive_news(self, 
                                   category: str = "general",
                                   region: str = "global",
                                   max_articles: int = 10) -> Dict[str, Any]:
        """
        Get news from multiple sources with comprehensive coverage
        Uses multiple APIs and RSS feeds for maximum reliability
        """
        all_articles = []
        sources_tried = []
        apis_used = []
        
        # Strategy 1: Try multiple news APIs in parallel
        api_tasks = []
        
        # GNews API (usually most reliable)
        if self.gnews_api_key:
            api_tasks.append(self._fetch_from_gnews(category, region, max_articles // 2))
        
        # NewsAPI.org
        if self.news_api_key:
            api_tasks.append(self._fetch_from_newsapi(category, region, max_articles // 2))
        
        # NewsData.io
        if self.newsdata_api_key:
            api_tasks.append(self._fetch_from_newsdata(category, region, max_articles // 2))
        
        # MediaStack
        if self.mediastack_api_key:
            api_tasks.append(self._fetch_from_mediastack(category, region, max_articles // 2))
        
        # Currents API
        if self.currents_api_key:
            api_tasks.append(self._fetch_from_currents(category, region, max_articles // 2))
        
        # WorldNews API
        if self.worldnews_api_key:
            api_tasks.append(self._fetch_from_worldnews(category, region, max_articles // 2))
        
        # NewsCatcher API
        if self.newscatcher_api_key:
            api_tasks.append(self._fetch_from_newscatcher(category, region, max_articles // 2))
        
        # Execute API calls in parallel
        if api_tasks:
            try:
                api_results = await asyncio.gather(*api_tasks, return_exceptions=True)
                for i, result in enumerate(api_results):
                    if isinstance(result, dict) and result.get('articles'):
                        all_articles.extend(result['articles'])
                        if i == 0 and self.gnews_api_key: apis_used.append("GNews")
                        elif i == 1 and self.news_api_key: apis_used.append("NewsAPI") 
                        elif i == 2 and self.newsdata_api_key: apis_used.append("NewsData")
                        elif i == 3 and self.mediastack_api_key: apis_used.append("MediaStack")
                        elif i == 4 and self.currents_api_key: apis_used.append("Currents")
                        elif i == 5 and self.worldnews_api_key: apis_used.append("WorldNews")
                        elif i == 6 and self.newscatcher_api_key: apis_used.append("NewsCatcher")
            except Exception as e:
                print(f"Error in parallel API calls: {e}")
        
        # Strategy 2: RSS feeds (very reliable fallback)
        if len(all_articles) < max_articles:
            rss_articles = await self._fetch_from_rss(category, region, max_articles - len(all_articles))
            if rss_articles:
                all_articles.extend(rss_articles)
                sources_tried.append("RSS")
        
        # Strategy 3: Try alternative regions if needed
        if len(all_articles) < max_articles // 2:
            fallback_regions = ["global", "us", "india", "uk"]
            for fallback_region in fallback_regions:
                if fallback_region != region:
                    fallback_articles = await self._fetch_from_rss(category, fallback_region, max_articles - len(all_articles))
                    if fallback_articles:
                        all_articles.extend(fallback_articles)
                        sources_tried.append(f"RSS-{fallback_region}")
                        break
        
        # Remove duplicates and sort by publish date
        unique_articles = self._remove_duplicates(all_articles)
        sorted_articles = sorted(unique_articles, key=lambda x: x.get('published_at', ''), reverse=True)
        
        return {
            "status": "success",
            "total_results": len(sorted_articles),
            "articles": sorted_articles[:max_articles],
            "apis_used": apis_used,
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
    
    async def _fetch_from_gnews(self, category: str, region: str, max_articles: int) -> Dict[str, Any]:
        """Fetch from GNews API - usually most reliable"""
        if not self.gnews_api_key:
            return {"articles": []}
        
        try:
            country_code = self._get_country_code(region)
            
            async with aiohttp.ClientSession() as session:
                params = {
                    "token": self.gnews_api_key,
                    "lang": "en",
                    "country": country_code,
                    "max": min(max_articles, 10),
                    "q": category if category != "general" else "",
                }
                params = {k: v for k, v in params.items() if v}  # Remove empty values
                
                async with session.get("https://gnews.io/api/v4/top-headlines", params=params, timeout=15) as response:
                    if response.status == 200:
                        data = await response.json()
                        articles = []
                        for article in data.get("articles", []):
                            articles.append({
                                "title": article.get("title", ""),
                                "description": article.get("description", ""),
                                "url": article.get("url", ""),
                                "published_at": article.get("publishedAt", ""),
                                "source": {"name": article.get("source", {}).get("name", "GNews")},
                                "content": article.get("content", "")
                            })
                        return {"articles": articles}
        except Exception as e:
            print(f"GNews API error: {e}")
        
        return {"articles": []}
    
    async def _fetch_from_mediastack(self, category: str, region: str, max_articles: int) -> Dict[str, Any]:
        """Fetch from MediaStack API"""
        if not self.mediastack_api_key:
            return {"articles": []}
        
        try:
            countries = self._get_mediastack_countries(region)
            
            async with aiohttp.ClientSession() as session:
                params = {
                    "access_key": self.mediastack_api_key,
                    "countries": countries,
                    "limit": min(max_articles, 25),
                    "languages": "en",
                    "sort": "published_desc"
                }
                if category != "general":
                    params["categories"] = category
                
                async with session.get("http://api.mediastack.com/v1/news", params=params, timeout=15) as response:
                    if response.status == 200:
                        data = await response.json()
                        articles = []
                        for article in data.get("data", []):
                            articles.append({
                                "title": article.get("title", ""),
                                "description": article.get("description", ""),
                                "url": article.get("url", ""),
                                "published_at": article.get("published_at", ""),
                                "source": {"name": article.get("source", "MediaStack")},
                                "content": article.get("description", "")  # MediaStack doesn't provide full content
                            })
                        return {"articles": articles}
        except Exception as e:
            print(f"MediaStack API error: {e}")
        
        return {"articles": []}
    
    async def _fetch_from_currents(self, category: str, region: str, max_articles: int) -> Dict[str, Any]:
        """Fetch from Currents API"""
        if not self.currents_api_key:
            return {"articles": []}
        
        try:
            async with aiohttp.ClientSession() as session:
                params = {
                    "apiKey": self.currents_api_key,
                    "language": "en",
                    "page_size": min(max_articles, 200),
                }
                if region != "global":
                    country_name = self._get_country_name(region)
                    if country_name:
                        params["keywords"] = f"{country_name} OR {category}"
                else:
                    params["keywords"] = category
                
                async with session.get("https://api.currentsapi.services/v1/search", params=params, timeout=15) as response:
                    if response.status == 200:
                        data = await response.json()
                        articles = []
                        for article in data.get("news", []):
                            articles.append({
                                "title": article.get("title", ""),
                                "description": article.get("description", ""),
                                "url": article.get("url", ""),
                                "published_at": article.get("published", ""),
                                "source": {"name": article.get("author", "Currents")},
                                "content": article.get("description", "")
                            })
                        return {"articles": articles}
        except Exception as e:
            print(f"Currents API error: {e}")
        
        return {"articles": []}
    
    async def _fetch_from_worldnews(self, category: str, region: str, max_articles: int) -> Dict[str, Any]:
        """Fetch from WorldNews API"""
        if not self.worldnews_api_key:
            return {"articles": []}
        
        try:
            async with aiohttp.ClientSession() as session:
                params = {
                    "api-key": self.worldnews_api_key,
                    "number": min(max_articles, 100),
                    "language": "en",
                    "sort": "publish-time",
                    "sort-direction": "DESC"
                }
                
                # Add location-based filtering
                if region == "india":
                    params["location-filter"] = "IN"
                elif region == "us":
                    params["location-filter"] = "US"
                elif region == "uk":
                    params["location-filter"] = "GB"
                
                # Add category-based text filtering
                if category != "general":
                    params["text"] = category
                
                async with session.get("https://api.worldnewsapi.com/search-news", params=params, timeout=15) as response:
                    if response.status == 200:
                        data = await response.json()
                        articles = []
                        for article in data.get("news", []):
                            articles.append({
                                "title": article.get("title", ""),
                                "description": article.get("summary", ""),
                                "url": article.get("url", ""),
                                "published_at": article.get("publish_date", ""),
                                "source": {"name": article.get("source_country", "WorldNews")},
                                "content": article.get("text", "")
                            })
                        return {"articles": articles}
        except Exception as e:
            print(f"WorldNews API error: {e}")
        
        return {"articles": []}
    
    async def _fetch_from_newscatcher(self, category: str, region: str, max_articles: int) -> Dict[str, Any]:
        """Fetch from NewsCatcher API"""
        if not self.newscatcher_api_key:
            return {"articles": []}
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"x-api-key": self.newscatcher_api_key}
                params = {
                    "lang": "en",
                    "page_size": min(max_articles, 100),
                    "sort_by": "date"
                }
                
                # Add country filtering
                if region == "india":
                    params["countries"] = "IN"
                elif region == "us":
                    params["countries"] = "US" 
                elif region == "uk":
                    params["countries"] = "GB"
                
                # Add category/topic filtering
                if category != "general":
                    params["q"] = category
                
                async with session.get("https://api.newscatcherapi.com/v2/search", 
                                     params=params, headers=headers, timeout=15) as response:
                    if response.status == 200:
                        data = await response.json()
                        articles = []
                        for article in data.get("articles", []):
                            articles.append({
                                "title": article.get("title", ""),
                                "description": article.get("excerpt", ""),
                                "url": article.get("link", ""),
                                "published_at": article.get("published_date", ""),
                                "source": {"name": article.get("clean_url", "NewsCatcher")},
                                "content": article.get("summary", "")
                            })
                        return {"articles": articles}
        except Exception as e:
            print(f"NewsCatcher API error: {e}")
        
        return {"articles": []}
    
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
    
    def _get_country_name(self, region: str) -> str:
        """Convert region to country name for APIs that need full names"""
        region_map = {
            "india": "India",
            "us": "United States", 
            "uk": "United Kingdom",
            "global": None
        }
        return region_map.get(region.lower())
    
    def _get_mediastack_countries(self, region: str) -> str:
        """Get MediaStack-specific country codes"""
        region_map = {
            "india": "in",
            "us": "us",
            "uk": "gb",
            "global": "us,gb,in,au,ca"  # Multiple countries for global
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
        "apis_used": result.get("apis_used", []),
        "sources_used": result.get("sources_used", [])
    }


# Test function
async def test_enhanced_news():
    """Test the enhanced multi-API news system"""
    print("🧪 Testing Enhanced Multi-API News System")
    print("=" * 60)
    
    aggregator = MultiSourceNewsAggregator()
    
    # Show available APIs
    apis_available = []
    if aggregator.gnews_api_key: apis_available.append("GNews")
    if aggregator.news_api_key: apis_available.append("NewsAPI")
    if aggregator.newsdata_api_key: apis_available.append("NewsData")
    if aggregator.mediastack_api_key: apis_available.append("MediaStack")
    if aggregator.currents_api_key: apis_available.append("Currents")
    if aggregator.worldnews_api_key: apis_available.append("WorldNews")
    if aggregator.newscatcher_api_key: apis_available.append("NewsCatcher")
    
    print(f"🔑 Available APIs: {', '.join(apis_available) if apis_available else 'RSS Only'}")
    print("-" * 60)
    
    test_cases = [
        ("technology", "india", 3),
        ("business", "us", 3), 
        ("general", "global", 5)
    ]
    
    for category, region, count in test_cases:
        print(f"\n🔍 Testing: {category} news from {region} ({count} articles)")
        
        result = await aggregator.get_comprehensive_news(category, region, count)
        
        print(f"✅ Status: {result['status']}")
        print(f"📰 Found: {result['total_results']} articles")
        if result.get('apis_used'):
            print(f"🔗 APIs Used: {', '.join(result['apis_used'])}")
        if result.get('sources_used'):
            print(f"� Other Sources: {', '.join(result['sources_used'])}")
        
        for i, article in enumerate(result.get('articles', [])[:2], 1):
            print(f"\nArticle {i}: {article.get('title', 'No title')[:80]}...")
            print(f"Source: {article.get('source', {}).get('name', 'Unknown')}")
        
        print("-" * 40)


if __name__ == "__main__":
    asyncio.run(test_enhanced_news())
