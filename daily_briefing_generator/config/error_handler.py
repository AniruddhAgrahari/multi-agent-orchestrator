# config/error_handler.py
import asyncio
from typing import Callable, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentErrorHandler:
    """
    Centralized error handling following your best practices guide
    """
    
    @staticmethod
    async def with_retry(func: Callable, max_retries: int = 3, delay: float = 1.0) -> Any:
        """
        Implement retry logic for API calls as recommended in troubleshooting guide
        """
        for attempt in range(max_retries):
            try:
                return await func()
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise e
                await asyncio.sleep(delay * (2 ** attempt))  # Exponential backoff
    
    @staticmethod
    def handle_api_error(error: Exception, service_name: str) -> str:
        """
        Convert technical errors into user-friendly messages
        """
        error_msg = str(error).lower()
        
        if "timeout" in error_msg:
            return f"The {service_name} service is taking longer than expected. Please try again."
        elif "rate limit" in error_msg or "429" in error_msg:
            return f"We're making too many requests to {service_name}. Please wait a moment and try again."
        elif "unauthorized" in error_msg or "401" in error_msg:
            return f"There's an authentication issue with {service_name}. Please check the configuration."
        else:
            return f"We encountered a temporary issue with {service_name}. Please try again later."
