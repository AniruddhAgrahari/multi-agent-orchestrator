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
        """        # Configure Google AI Studio
        api_key = os.getenv("GOOGLE_AI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Google AI API key not found. Please set GOOGLE_AI_API_KEY in your .env file")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    async def get_news_briefing(self, user_request: str) -> str:
        """
        Intelligent news curation following your best practices guide.
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
            analysis = response.text            # Parse the analysis
            category = self._extract_value(analysis, "CATEGORY:") or "general"
            country = self._extract_value(analysis, "COUNTRY:")
            # Handle unspecified or invalid country codes
            if not country or country in ["unspecified", "unknown", "none"]:
                country = "us"  # Default to US
            count = int(self._extract_value(analysis, "COUNT:") or "5")
            
            # Debug: Print what AI analyzed
            print(f"DEBUG AI Analysis: category={category}, country={country}, count={count}")
            print(f"DEBUG Analysis text: {analysis}")
            
            # Fetch news data using your tool
            news_data = await get_news_data(
                query=category,  # Use category as query
                category=category,
                country=country,
                max_articles=min(count, 10)  # Respect rate limits
            )
            
            if "error" in news_data:
                return f"Sorry, I couldn't fetch news: {news_data['error']}"
            
            # Debug: Print what we got
            print(f"DEBUG: Got {news_data.get('total_results', 0)} articles")
            print(f"DEBUG: Articles key exists: {'articles' in news_data}")
            print(f"DEBUG: Articles count: {len(news_data.get('articles', []))}")
            
            if not news_data.get("articles"):
                return "No recent news articles found for your request."
                return "No recent news articles found for your request."
            
            # Let AI create a curated briefing
            articles_summary = self._format_articles_for_ai(news_data["articles"])
            
            briefing_prompt = f"""
            Create a professional news briefing based on these articles:
            
            {articles_summary}
            
            User's original request: "{user_request}"
            
            Guidelines:
            - Start with a brief overview
            - Highlight the most important stories
            - Keep it concise but informative
            - Group related stories together
            - End with a summary of key takeaways
            
            Make it sound like a professional news briefing.
            """
            
            final_response = await self.model.generate_content_async(briefing_prompt)
            return final_response.text
            
        except Exception as e:
            return f"I encountered an error processing your news request: {str(e)}"
    
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
    
    print("🧪 TESTING NEWS AGENT")
    print("=" * 50)
    
    for request in test_requests:
        print(f"\n🤖 User: {request}")
        response = await agent.get_news_briefing(request)
        print(f"📰 Agent: {response}")
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(test_news_agent())
