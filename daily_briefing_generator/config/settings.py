"""
Settings and configuration for the daily briefing generator.
"""

import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

class Settings:
    def __init__(self):
        """Initialize settings with default values and load from environment."""
        # Load environment variables
        load_dotenv()
        
        # Default settings
        self.default_location = os.getenv("DEFAULT_LOCATION", "New York, NY")
        self.default_news_topics = self._parse_list_env("DEFAULT_NEWS_TOPICS", ["technology", "business"])
        self.save_briefings = os.getenv("SAVE_BRIEFINGS", "true").lower() == "true"
        self.output_directory = os.getenv("OUTPUT_DIRECTORY", "./briefings")
        
        # API Keys
        self.weather_api_key = os.getenv("WEATHER_API_KEY")
        self.news_api_key = os.getenv("NEWS_API_KEY")
        
        # API Settings
        self.weather_units = os.getenv("WEATHER_UNITS", "metric")
        self.news_country = os.getenv("NEWS_COUNTRY", "us")
        self.news_language = os.getenv("NEWS_LANGUAGE", "en")
        
        # Briefing Settings
        self.max_news_articles = int(os.getenv("MAX_NEWS_ARTICLES", "5"))
        self.include_weather_forecast = os.getenv("INCLUDE_WEATHER_FORECAST", "true").lower() == "true"
        self.forecast_days = int(os.getenv("FORECAST_DAYS", "3"))
    
    def _parse_list_env(self, env_var: str, default: List[str]) -> List[str]:
        """
        Parse a comma-separated environment variable into a list.
        
        Args:
            env_var (str): Environment variable name
            default (List[str]): Default value if env var not set
            
        Returns:
            List[str]: Parsed list
        """
        env_value = os.getenv(env_var)
        if env_value:
            return [item.strip() for item in env_value.split(",") if item.strip()]
        return default
    
    def update_settings(self, new_settings: Dict) -> None:
        """
        Update settings with new values.
        
        Args:
            new_settings (Dict): Dictionary of new setting values
        """
        for key, value in new_settings.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def get_all_settings(self) -> Dict:
        """
        Get all current settings as a dictionary.
        
        Returns:
            Dict: All settings
        """
        return {
            "default_location": self.default_location,
            "default_news_topics": self.default_news_topics,
            "save_briefings": self.save_briefings,
            "output_directory": self.output_directory,
            "weather_api_key": "***" if self.weather_api_key else None,
            "news_api_key": "***" if self.news_api_key else None,
            "weather_units": self.weather_units,
            "news_country": self.news_country,
            "news_language": self.news_language,
            "max_news_articles": self.max_news_articles,
            "include_weather_forecast": self.include_weather_forecast,
            "forecast_days": self.forecast_days
        }
    
    def validate_settings(self) -> List[str]:
        """
        Validate current settings and return any issues.
        
        Returns:
            List[str]: List of validation issues
        """
        issues = []
        
        if not self.weather_api_key:
            issues.append("Weather API key not configured")
        
        if not self.news_api_key:
            issues.append("News API key not configured")
        
        if self.max_news_articles <= 0:
            issues.append("Max news articles must be greater than 0")
        
        if self.forecast_days <= 0:
            issues.append("Forecast days must be greater than 0")
        
        return issues
