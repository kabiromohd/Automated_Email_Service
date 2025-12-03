import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

LOG_FILE = os.getenv("LOG_FILE_QUOTE")

def configure_logging():
    """Configure logging for the application."""
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE, mode='a'),  # 'a' mode appends to the file
            logging.StreamHandler()
        ]
    )
    return logging.getLogger()

if __name__ == "__main__":
    configure_logging()