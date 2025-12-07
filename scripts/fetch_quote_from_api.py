import requests
import os
from dotenv import load_dotenv
from scripts.logger import configure_logging

# Load environment variables from .env file
load_dotenv()
ZEN_QUOTES_URL = os.getenv("ZEN_QUOTES_URL")

logger = configure_logging()

def fetch_quote():
    """Fetches a daily quote from the Zen Quotes API."""

    logger.info("Fetching quote from API...")
    url = ZEN_QUOTES_URL
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            logger.error(f"Failed to fetch quote, status code: {response.status_code}")
            raise Exception(f"Status code {response.status_code}")
        
        data = response.json()
        
        if not isinstance(data, list) or not data[0].get("q"):
            logger.error(f"Malformed response structure")
            raise Exception("Malformed response structure")

        # Validate structure: expect list with at least one dictionary
        if not isinstance(data, list) or len(data) == 0 or not isinstance(data[0], dict):
            logger.error(f"Unexpected data format")
            raise Exception("Unexpected data format")
        
        quote, author = data[0]["q"].strip(), data[0]["a"].strip()
        logger.info(f"Quote fetched successfully: “{quote}” — {author}")
        return quote, author
    except Exception as e:
        logger.error(f"Quote fetch failed: {e}")
        return None, None
    
if __name__ == "__main__":
    fetch_quote()
