# agents/news_agent.py
import asyncio
import os
import sys
from typing import Dict, List, Any
from dotenv import load_dotenv
import google.generativeai as genai

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.news_tool import get_news_data

# Load environment variables from parent directory
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

class NewsAgent:
    def __init__(self):
        """
        Your second intelligent agent, Master Aniruddh!
        This agent specializes in curating and presenting news for your daily briefing.
        """
        # Configure Google AI Studio
        api_key = os.getenv("GOOGLE_AI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Google AI API key not found. Please set GOOGLE_AI_API_KEY in your .env file")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-flash-lite-latest')
        
    async def get_news_briefing(self, user_request: str) -> str:
        """
        Enhanced news curation with robust fallback strategies.
        This agent understands context and filters content appropriately.
        """
        # Let AI analyze what kind of news the user wants
        analysis_prompt = f"""
Analyze this news request from the perspective of providing relevant and timely news for India: "{user_request}"

Extract these parameters clearly:
1. Category: technology, business, health, sports, entertainment, general. Use 'general' if no strong category is detected.
2. Country preference: use valid country code (us, in, uk, etc.). Default to 'in' (India) if no country is specified.
3. Number of articles to retrieve: default 5, maximum 10.
4. Specific topics or keywords relevant to the request, especially focusing on India-related terms.

Respond ONLY in this format exactly:
CATEGORY: [category]
COUNTRY: [country code]  
COUNT: [number]
KEYWORDS: [keywords, if any, else "None"]
"""
        
        try:
            # Get AI analysis
            response = await self.model.generate_content_async(analysis_prompt)
            analysis = response.text
            
            # Parse the analysis
            category = self._extract_value(analysis, "CATEGORY:") or "general"
            country = self._extract_value(analysis, "COUNTRY:")
            # Handle unspecified or invalid country codes
            if not country or country in ["unspecified", "unknown", "none"]:
                country = "us"  # Default to US
            count = int(self._extract_value(analysis, "COUNT:") or "5")
            
            # Fetch news data using enhanced tool with fallbacks
            news_data = await get_news_data(
                query=category,  # Use category as query
                category=category,
                country=country,
                max_articles=min(count, 10)  # Respect rate limits
            )
            
            # Enhanced error handling
            if news_data.get("status") == "error" or "error" in news_data:
                error_msg = news_data.get("error", "Unknown error occurred")
                # Try to provide a fallback response based on the request
                fallback_response = await self._generate_fallback_response(user_request, category, country)
                return fallback_response
            
            # Check if we have valid articles
            articles = news_data.get("articles", [])
            if not articles:
                # Generate a meaningful response even without articles
                fallback_response = await self._generate_fallback_response(user_request, category, country)
                return fallback_response
            
            # Let AI create a curated briefing with enhanced context
            articles_summary = self._format_articles_for_ai(articles)
            
            briefing_prompt = f"""
Create a professional news briefing based on these articles:

{articles_summary}

User's original request: "{user_request}"
Request Context: Category={category}, Country={country}

Guidelines:
- Start with a brief overview mentioning the region/category focus
- Highlight the most important stories with business implications
- Keep it concise but informative
- If articles seem limited, acknowledge this but focus on what's available
- Group related stories together
- End with key takeaways relevant to the user's location/interests

Make it sound like a professional news briefing for {country.upper() if country else 'international'} audience.
"""
            
            final_response = await self.model.generate_content_async(briefing_prompt)
            return final_response.text
            
        except Exception as e:
            return f"I encountered an error processing your news request: {str(e)}"
    
    async def _generate_fallback_response(self, user_request: str, category: str, country: str) -> str:
        """Generate a meaningful response when no news articles are available"""
        fallback_prompt = f"""
The user requested: "{user_request}"
However, no current news articles are available for category: {category}, country: {country}.

Create a professional response that:
1. Acknowledges the limitation
2. Explains why this might happen (API limits, regional availability, etc.)
3. Suggests alternative approaches or general insights about the requested topic/region
4. Maintains a professional, helpful tone

Keep it concise and actionable.
"""
        
        try:
            response = await self.model.generate_content_async(fallback_prompt)
            return response.text
        except Exception:
            return f"I apologize, but I'm currently unable to fetch news for {category} from {country}. This could be due to API limitations or regional availability. Please try again later or consider a broader search term."
    
    def _extract_value(self, text: str, key: str) -> str:
        """Helper method to parse AI responses"""
        lines = text.split('\n')
        for line in lines:
            if line.strip().startswith(key):
                return line.split(':', 1)[1].strip()
        return ""
    
    def _format_articles_for_ai(self, articles: List[Dict]) -> str:
        """Format articles for AI processing - following content filtering best practices"""
        formatted = []
        for i, article in enumerate(articles, 1):
            # Filter out articles with missing critical information
            if not article.get('title') or not article.get('description'):
                continue
                
            formatted.append(f"""
Article {i}:
Title: {article['title']}
Source: {article['source']['name']}
Description: {article['description']}
Published: {article['publishedAt']}
""")
        
        return "\n".join(formatted)

# Test function following your testing best practices
async def test_news_agent():
    """Comprehensive testing as per your deployment checklist"""
    agent = NewsAgent()
    
    test_requests = [
        "Give me today's top technology news",
        "What's happening in business news?",
        "Any important health news from India?",
        "Show me 3 sports headlines"
    ]
    
    print("🧪 TESTING ENHANCED NEWS AGENT")
    print("=" * 50)
    
    for request in test_requests:
        print(f"\n🤖 User: {request}")
        response = await agent.get_news_briefing(request)
        print(f"📰 Agent: {response}")
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(test_news_agent())
