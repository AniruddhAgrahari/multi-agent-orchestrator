"""
Clean test for Master Agent without debug output
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

from orchestrator.master_agent import master_agent

async def clean_test():
    print("🎯 Master Agent - Final Production Test")
    print("=" * 60)
    
    test_requests = [
        "Give me a complete daily briefing for Mumbai with weather and technology news",
        "What's the weather like in London today?",
        "I need the latest business news updates",
        "Full morning briefing for New York - weather and all news categories"
    ]
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n📋 Test {i}: {request}")
        print("-" * 50)
        
        try:
            response = await master_agent.run(request)
            print(f"✅ Master Agent Response:\n{response}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print("\n" + "="*60)

if __name__ == "__main__":
    asyncio.run(clean_test())
