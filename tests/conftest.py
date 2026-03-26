import sqlite3
import pytest
import sys
import os

# Add nexcart root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.schema import create_tables

@pytest.fixture
def db():
    """In-memory SQLite database with all tables created."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    create_tables(conn)
    yield conn
    conn.close()

@pytest.fixture
def sample_product(db):
    """Insert and return a sample product."""
    cursor = db.execute(
        "INSERT INTO products (name, price, stock, category) VALUES (?, ?, ?, ?)",
        ("Test Product", 29.99, 100, "Electronics")
    )
    db.commit()
    return {"product_id": cursor.lastrowid, "name": "Test Product", "price": 29.99, "stock": 100, "category": "Electronics"}

@pytest.fixture
def sample_user(db):
    """Insert and return a sample user."""
    cursor = db.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        ("Test User", "test@example.com")
    )
    db.commit()
    return {"user_id": cursor.lastrowid, "name": "Test User", "email": "test@example.com"}
