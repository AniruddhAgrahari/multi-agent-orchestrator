import os
from dotenv import load_dotenv

load_dotenv()

print("🔍 All Environment Variables (API keys only):")
print("=" * 50)

# Get all environment variables and filter for likely API keys
all_env = dict(os.environ)
api_related = {}

for key, value in all_env.items():
    # Look for variables that might be API keys
    if any(keyword in key.upper() for keyword in ['API', 'KEY', 'TOKEN', 'SECRET']):
        if 'NEWS' in key.upper() or 'WEATHER' in key.upper() or 'GOOGLE' in key.upper():
            # Show first 10 and last 5 characters for security
            if len(value) > 15:
                api_related[key] = f"{value[:10]}...{value[-5:]}"
            else:
                api_related[key] = "configured"

print("Found API-related variables:")
for key, value in api_related.items():
    print(f"  {key}: {value}")

# Also check specifically for news-related variables
print("\nSpecifically checking for news APIs:")
news_apis = [
    'NEWS_API_KEY', 'GNEWS_API_KEY', 'NEWSDATA_API_KEY', 
    'MEDIASTACK_API_KEY', 'CURRENTS_API_KEY', 'WORLDNEWS_API_KEY',
    'NEWSCATCHER_API_KEY', 'WORLD_NEWS_API_KEY'
]

for api in news_apis:
    value = os.getenv(api)
    if value:
        print(f"  ✅ {api}: configured")
    else:
        print(f"  ❌ {api}: not found")
