"""
Test location-specific news after fix
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.master_agent import MasterAgent

async def test_location_specific_news():
    """Test that news is location-specific"""
    print("="*60)
    print("TESTING LOCATION-SPECIFIC NEWS FIX")
    print("="*60)

    master = MasterAgent()

    test_cases = [
        {
            "query": "Morning briefing for Mumbai with tech news",
            "expected_location": "Mumbai",
            "expected_country": "India"
        },
        {
            "query": "Give me business news for London",
            "expected_location": "London",
            "expected_country": "UK"
        },
        {
            "query": "Technology news for New York",
            "expected_location": "New York",
            "expected_country": "US"
        }
    ]

    for i, test in enumerate(test_cases, 1):
        print(f"\nTEST {i}/{len(test_cases)}")
        print(f"Query: {test['query']}")
        print(f"Expected: {test['expected_location']}, {test['expected_country']}")
        print("-"*60)

        try:
            response = await master.process_request(test['query'])

            # Check if location appears in response
            location_found = test['expected_location'].lower() in response.lower()
            country_found = test['expected_country'].lower() in response.lower()

            print(f"RESPONSE (first 500 chars):\n{response[:500]}...")
            print(f"\nVERIFICATION:")
            print(f"  Location '{test['expected_location']}' found: {'YES' if location_found else 'NO'}")
            print(f"  Country '{test['expected_country']}' context: {'YES' if country_found else 'NO'}")

            if location_found or country_found:
                print("  Result: PASS - Location-specific news working!")
            else:
                print("  Result: FAIL - News not location-specific")

        except Exception as e:
            print(f"ERROR: {str(e)}")

        print("="*60)

if __name__ == "__main__":
    asyncio.run(test_location_specific_news())
