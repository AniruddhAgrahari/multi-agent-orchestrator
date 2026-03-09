"""
Daily Briefing Generator - CLI Entry Point

Run from the daily_briefing_generator/ directory:
  python main.py                        # Single briefing
  python main.py --interactive          # Interactive mode
"""

import asyncio
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orchestrator.master_agent import MasterAgent


def print_banner():
    print("=" * 60)
    print("         🌅 DAILY BRIEFING GENERATOR 🌅")
    print("=" * 60)
    print(f"         {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()


async def run_briefing(query: str):
    """Run a single briefing request."""
    master_agent = MasterAgent()
    print(f"📋 Query: {query}\n")
    result = await master_agent.run_with_recovery(query)
    print(result)


async def interactive_mode():
    """Interactive terminal mode."""
    print_banner()
    print("🎯 Interactive Mode — type your briefing request")
    print("   Type 'quit' or press Ctrl+C to exit\n")

    master_agent = MasterAgent()

    while True:
        try:
            query = input("📝 Request: ").strip()
            if not query:
                continue
            if query.lower() in ("quit", "exit", "q"):
                print("👋 Goodbye!")
                break
            print("\n⏳ Generating briefing...\n")
            result = await master_agent.run_with_recovery(query)
            print(result)
            print("\n" + "-" * 60 + "\n")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        asyncio.run(interactive_mode())
    else:
        # Default: run a morning briefing
        default_query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Morning briefing with top news and weather"
        print_banner()
        try:
            asyncio.run(run_briefing(default_query))
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
