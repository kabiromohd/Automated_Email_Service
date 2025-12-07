import duckdb
import os  
from dotenv import load_dotenv
from scripts.logger import configure_logging

load_dotenv()
DB_PATH = os.getenv('DUCKDB_PATH')
logger = configure_logging()

def get_connection():
    """Establish and return a connection to the DuckDB database."""

    logger.info("Connecting to the database...")
    return duckdb.connect(DB_PATH)

if __name__ == "__main__":
    get_connection()