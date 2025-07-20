import os
from dotenv import load_dotenv

load_dotenv()

print("🔑 API Key Status Check:")
print("=" * 30)

apis = {
    'NewsAPI': 'NEWS_API_KEY',
    'GNews': 'GNEWS_API_KEY', 
    'NewsData': 'NEWSDATA_API_KEY',
    'MediaStack': 'MEDIASTACK_API_KEY',
    'Currents': 'CURRENTS_API_KEY',
    'WorldNews': 'WORLDNEWS_API_KEY',
    'NewsCatcher': 'NEWSCATCHER_API_KEY'
}

for name, env_var in apis.items():
    key = os.getenv(env_var)
    status = "✅ Configured" if key else "❌ Not set"
    print(f"{name}: {status}")
