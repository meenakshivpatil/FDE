import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL=os.getenv("DATABASE_URL", "postgresql://fde_user:FDE_2026@localhost:5432/fde_db")
connection = psycopg2.connect(DATABASE_URL)

def get_db_connection():
    return connection.cursor(cursor_factory=RealDictCursor)

def close_db_connection():
    connection.close()

def commit_db_connection():
    connection.commit()

