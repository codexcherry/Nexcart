import sqlite3
import os
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "nexcart.db"

def get_connection() -> sqlite3.Connection:
    """Returns a configured SQLite3 connection."""
    os.makedirs(DB_PATH.parent, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db() -> None:
    """Initialize the database, creating all tables."""
    from backend.schema import create_tables
    conn = get_connection()
    create_tables(conn)
    conn.close()
