import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

# Reuse the shared .env from week2-postgresql/Day4 (this file is in week3-typescript_reactjs/day6/homeassignment2)
FDE_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(FDE_ROOT / "week2-postgresql" / "Day4" / ".env")
DATABASE_URL = os.getenv("DATABASE_URL")


def get_db_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set. Check week2-postgresql/Day4/.env")
    return psycopg2.connect(DATABASE_URL)
