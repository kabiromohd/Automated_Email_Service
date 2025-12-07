import duckdb
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database path from environment variable
DB_PATH = os.getenv("DUCKDB_PATH")
# Create a connection to duckdb

# Establish connection to DuckDB database
conn = duckdb.connect(DB_PATH)

# create users table
conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    subscription_status VARCHAR(10) CHECK (subscription_status IN ('active', 'inactive')) DEFAULT 'active',
    email_frequency VARCHAR(10) CHECK (email_frequency IN ('daily', 'weekly')) DEFAULT 'daily',
    last_emailed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
""")

# Insert sample data into users table (In real scenario, data would come from user registrations)
conn.execute("""
INSERT INTO users 
(user_id, name, email, subscription_status, email_frequency)
VALUES
(1, 'Full Name 1', 'example1@yahoo.com', 'active', 'daily'),
(2, 'Full Name 2', 'example2@gmail.com', 'active', 'weekly'),
(3, 'Full Name 3', 'example3@yahoo.com', 'inactive', 'daily'),
(4, 'Full Name 4', 'example4@gmail.com', 'active', 'weekly'),
(5, 'Full Name 5', 'example5@yahoo.com', 'active', 'daily');
""")