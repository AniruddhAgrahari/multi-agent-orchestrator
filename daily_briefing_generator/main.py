"""
Daily Briefing Generator - Main Entry Point

A comprehensive daily briefing system that aggregates weather and news information
to provide personalized daily updates.
"""

import sys
import os
from datetime import datetime
from typing import Optional, List

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orchestrator.master_agent import MasterAgent
from config.settings import Settings

def print_banner():
    """Print a welcome banner."""
    print("=" * 60)
    print("         🌅 DAILY BRIEFING GENERATOR 🌅")
    print("=" * 60)
    print(f"         Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

def main():
    """Main function to generate and display daily briefing."""
    try:
        # Print banner
        print_banner()
        
        # Initialize the master agent
        print("🚀 Initializing Daily Briefing Generator...")
        master_agent = MasterAgent()
        
        # Validate settings
        settings = Settings()
        validation_issues = settings.validate_settings()
        
        if validation_issues:
            print("⚠️  Configuration Issues Found:")
            for issue in validation_issues:
                print(f"   - {issue}")
            print("\n💡 Please check your .env file and configure API keys.")
            print("   The system will continue with placeholder data.")
            print()
        
        # Generate briefing
        print("📋 Generating your daily briefing...")
        print()
        
        # You can customize these parameters
        location = None  # Will use default from settings
        topics = None    # Will use default from settings
        
        # Generate the briefing
        briefing = master_agent.generate_daily_briefing(location=location, topics=topics)
        
        # Display the briefing
        print(briefing)
        
        # Show summary
        summary = master_agent.get_briefing_summary()
        print("=" * 60)
        print("📊 BRIEFING SUMMARY")
        print("=" * 60)
        print(f"Location: {summary['default_location']}")
        print(f"News Topics: {', '.join(summary['default_news_topics'])}")
        print(f"Save to File: {summary['save_briefings']}")
        if summary['save_briefings']:
            print(f"Output Directory: {summary['output_directory']}")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error generating briefing: {e}")
        print("Please check your configuration and try again.")
        return 1
    
    return 0

def interactive_mode():
    """Run in interactive mode for custom briefings."""
    print_banner()
    print("🎯 Interactive Mode - Customize Your Briefing")
    print()
    
    try:
        master_agent = MasterAgent()
        
        # Get user preferences
        location = input("Enter location (or press Enter for default): ").strip()
        if not location:
            location = None
        
        topics_input = input("Enter news topics (comma-separated, or press Enter for default): ").strip()
        topics = None
        if topics_input:
            topics = [topic.strip() for topic in topics_input.split(",") if topic.strip()]
        
        print("\n📋 Generating your custom briefing...")
        print()
        
        briefing = master_agent.generate_daily_briefing(location=location, topics=topics)
        print(briefing)
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        exit_code = main()
        sys.exit(exit_code)
