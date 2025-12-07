import duckdb
import os
import pandas as pd
from dotenv import load_dotenv
from scripts.logger import configure_logging
from scripts.connect_to_db import get_connection

logger = configure_logging()

def get_active_users():
    """Fetches active users from the DuckDB database."""

    conn = get_connection()
    logger.info(f"Connected to database to fetch active users")

    query = """
        SELECT *
        FROM users
        WHERE subscription_status = 'active';
    """

    users = conn.execute(query).fetchdf()
    conn.close()
    logger.info(f"Fetched {len(users)} active users from database")

    return users

if __name__ == "__main__":
    get_active_users()

    