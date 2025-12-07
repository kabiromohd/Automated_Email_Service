import duckdb
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Get database path from environment variable
DB_PATH = os.getenv("DUCKDB_PATH")

def check_db_update():
    """Used to Check updates in the data DuckDB database."""
    
    # Establish connection to DuckDB database
    conn = duckdb.connect(DB_PATH)

    # check the users table for updates
    result = conn.execute("SELECT * FROM users").fetchdf()
    print(result)
    conn.close()

if __name__ == "__main__":
    check_db_update()