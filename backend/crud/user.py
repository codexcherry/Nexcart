import sqlite3
from typing import Optional

def insert_user(conn: sqlite3.Connection, user: dict) -> int:
    """Insert a user and return the new user_id. Raises IntegrityError on duplicate email."""
    cursor = conn.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        (user["name"], user["email"])
    )
    conn.commit()
    return cursor.lastrowid

def fetch_user_by_id(conn: sqlite3.Connection, user_id: int) -> Optional[dict]:
    """Fetch a user by ID, or None if not found."""
    row = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    return dict(row) if row else None

def fetch_user_by_email(conn: sqlite3.Connection, email: str) -> Optional[dict]:
    """Fetch a user by email, or None if not found."""
    row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    return dict(row) if row else None

def fetch_all_users(conn: sqlite3.Connection) -> list:
    """Fetch all users."""
    rows = conn.execute("SELECT * FROM users ORDER BY created_at DESC").fetchall()
    return [dict(row) for row in rows]

def update_last_active(conn: sqlite3.Connection, user_id: int) -> None:
    """Update the last_active timestamp for a user."""
    conn.execute(
        "UPDATE users SET last_active = datetime('now') WHERE user_id = ?",
        (user_id,)
    )
    conn.commit()
