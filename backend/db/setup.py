"""
Database setup script for the AI Learning Platform.
This script initializes the database schema and loads seed data.
"""

import os
import sys
from pathlib import Path

import dotenv
from supabase import create_client, Client

# Add the parent directory to the path so we can import from app
sys.path.append(str(Path(__file__).parent.parent))

from app.core.config import settings

def setup_database():
    """
    Set up the database schema and seed data.
    """
    print("Setting up database...")
    
    # Load environment variables
    dotenv.load_dotenv()
    
    # Get Supabase credentials
    supabase_url = settings.SUPABASE_URL
    supabase_key = settings.SUPABASE_KEY
    
    if not supabase_url or not supabase_key:
        print("Error: SUPABASE_URL and SUPABASE_KEY must be set in the environment or .env file.")
        sys.exit(1)
    
    # Create Supabase client
    supabase = create_client(supabase_url, supabase_key)
    
    # Read schema SQL
    schema_path = Path(__file__).parent / "schema.sql"
    with open(schema_path, "r") as f:
        schema_sql = f.read()
    
    # Read seed SQL
    seed_path = Path(__file__).parent / "seed.sql"
    with open(seed_path, "r") as f:
        seed_sql = f.read()
    
    # Execute schema SQL
    print("Creating database schema...")
    try:
        # Split the schema SQL into individual statements
        schema_statements = schema_sql.split(";")
        for statement in schema_statements:
            if statement.strip():
                # Execute each statement
                supabase.postgrest.rpc("exec_sql", {"query": statement}).execute()
        print("Schema created successfully.")
    except Exception as e:
        print(f"Error creating schema: {e}")
        sys.exit(1)
    
    # Execute seed SQL
    print("Loading seed data...")
    try:
        # Split the seed SQL into individual statements
        seed_statements = seed_sql.split(";")
        for statement in seed_statements:
            if statement.strip():
                # Execute each statement
                supabase.postgrest.rpc("exec_sql", {"query": statement}).execute()
        print("Seed data loaded successfully.")
    except Exception as e:
        print(f"Error loading seed data: {e}")
        sys.exit(1)
    
    print("Database setup complete.")

if __name__ == "__main__":
    setup_database()
