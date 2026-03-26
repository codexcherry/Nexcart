import sqlite3
from backend.db import get_connection
from backend.crud.user import insert_user, fetch_user_by_id, fetch_all_users, update_last_active

def add_user(data: dict) -> int:
    """Register a new user. Validates name; raises ValueError on duplicate email."""
    if not data.get("name") or not str(data["name"]).strip():
        raise ValueError("User name must be a non-empty string")
    if not data.get("email") or not str(data["email"]).strip():
        raise ValueError("User email must be a non-empty string")
    conn = get_connection()
    try:
        return insert_user(conn, data)
    except sqlite3.IntegrityError:
        raise ValueError("Email already in use")
    finally:
        conn.close()

def get_user(user_id: int) -> dict:
    """Fetch a user by ID. Raises ValueError if not found."""
    conn = get_connection()
    try:
        user = fetch_user_by_id(conn, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        update_last_active(conn, user_id)
        return user
    finally:
        conn.close()

def get_all_users() -> list:
    """Fetch all registered users."""
    conn = get_connection()
    try:
        return fetch_all_users(conn)
    finally:
        conn.close()
