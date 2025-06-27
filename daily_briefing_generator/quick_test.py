import aiohttp
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if API key is loaded
api_key = os.getenv('OPENWEATHERMAP_API_KEY')
print('✅ Environment variables loaded!')
print(f'✅ API Key present: {bool(api_key)}')

# Test aiohttp session creation
async def test_session():
    async with aiohttp.ClientSession() as session:
        print('✅ aiohttp session created successfully!')
        return True

# Run the async test
result = asyncio.run(test_session())
print('🎉 All systems operational!')
