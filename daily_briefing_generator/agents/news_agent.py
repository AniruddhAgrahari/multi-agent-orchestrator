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
        
    async def get_news_briefing(
        self,
        user_request: str,
        location: str = None,
        country: str = None,
        category: str = None
    ) -> str:
        """
        Enhanced news curation with robust fallback strategies.
        This agent understands context and filters content appropriately.

        Args:
            user_request: Natural language request from user
            location: Specific city/region (e.g., "Mumbai", "London") - makes news location-specific
            country: Country code (e.g., "in", "us", "uk") - filters news by country
            category: News category (e.g., "technology", "business")
        """
        # If structured parameters provided, use them directly (no re-parsing needed)
        if location or country or category:
            final_category = category or "general"
            final_country = country or "us"
            final_location = location or ""
            count = 5
        else:
            # Fall back to AI analysis if no structured parameters
            analysis_prompt = f"""
Analyze this news request: "{user_request}"

Extract these parameters clearly:
1. Category: technology, business, health, sports, entertainment, general. Use 'general' if no strong category is detected.
2. Country preference: use valid country code (us, in, uk, etc.). Extract from request, do not default.
3. Specific location: city or region name if mentioned (e.g., Mumbai, London, New York)
4. Number of articles to retrieve: default 5, maximum 10.

Respond ONLY in this format exactly:
CATEGORY: [category]
COUNTRY: [country code or "none"]
LOCATION: [location name or "none"]
COUNT: [number]
"""

            try:
                # Get AI analysis
                response = await self.model.generate_content_async(analysis_prompt)
                analysis = response.text

                # Parse the analysis
                final_category = self._extract_value(analysis, "CATEGORY:") or "general"
                extracted_country = self._extract_value(analysis, "COUNTRY:")
                extracted_location = self._extract_value(analysis, "LOCATION:")

                # Only use defaults if truly not specified
                final_country = extracted_country if extracted_country and extracted_country not in ["unspecified", "unknown", "none"] else "us"
                final_location = extracted_location if extracted_location and extracted_location not in ["unspecified", "unknown", "none"] else ""
                count = int(self._extract_value(analysis, "COUNT:") or "5")

            except Exception as e:
                # Fallback to safe defaults on analysis error
                final_category = "general"
                final_country = "us"
                final_location = ""
                count = 5

        try:
            # Build location-aware search query
            # CRITICAL FIX: Include location in query for geo-specific results
            if final_location:
                # Location-specific query: "Mumbai technology" or "London business"
                search_query = f"{final_location} {final_category}"
            else:
                # Category-only query if no location
                search_query = final_category

            # Fetch news data using enhanced tool with fallbacks
            news_data = await get_news_data(
                query=search_query,  # Now includes location for geo-specific results!
                category=final_category,
                country=final_country,
                max_articles=min(count, 10)  # Respect rate limits
            )
            
            # Enhanced error handling
            if news_data.get("status") == "error" or "error" in news_data:
                error_msg = news_data.get("error", "Unknown error occurred")
                # Try to provide a fallback response based on the request
                fallback_response = await self._generate_fallback_response(
                    user_request, final_category, final_country, final_location
                )
                return fallback_response

            # Check if we have valid articles
            articles = news_data.get("articles", [])
            if not articles:
                # Generate a meaningful response even without articles
                fallback_response = await self._generate_fallback_response(
                    user_request, final_category, final_country, final_location
                )
                return fallback_response

            # Let AI create a curated briefing with enhanced context
            articles_summary = self._format_articles_for_ai(articles)

            # Build location context for briefing
            location_context = f"Location: {final_location}, Country: {final_country.upper()}" if final_location else f"Country: {final_country.upper()}"

            briefing_prompt = f"""
Create a professional news briefing based on these articles:

{articles_summary}

User's original request: "{user_request}"
Request Context: Category={final_category}, {location_context}

Guidelines:
- Start with a brief overview mentioning the {"specific location (" + final_location + ")" if final_location else "region"} and category focus
- Highlight the most important stories with business implications
- {"Prioritize stories directly related to " + final_location + " or its immediate region" if final_location else "Focus on stories relevant to the " + final_country.upper() + " audience"}
- Keep it concise but informative
- Group related stories together
- End with key takeaways relevant to {"the " + final_location + " region" if final_location else "the audience's interests"}

Make it sound like a professional news briefing {"for " + final_location if final_location else "for " + final_country.upper() + " audience"}.
"""

            final_response = await self.model.generate_content_async(briefing_prompt)
            return final_response.text
            
        except Exception as e:
            return f"I encountered an error processing your news request: {str(e)}"
    
    async def _generate_fallback_response(
        self,
        user_request: str,
        category: str,
        country: str,
        location: str = None
    ) -> str:
        """Generate a meaningful response when no news articles are available"""
        location_info = f"location: {location}, " if location else ""
        fallback_prompt = f"""
The user requested: "{user_request}"
However, no current news articles are available for {location_info}category: {category}, country: {country}.

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
            location_str = f" in {location}" if location else ""
            return f"I apologize, but I'm currently unable to fetch news for {category}{location_str} from {country}. This could be due to API limitations or regional availability. Please try again later or consider a broader search term."
    
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
