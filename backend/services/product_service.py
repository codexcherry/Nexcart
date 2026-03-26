import sqlite3
from backend.db import get_connection
from backend.crud.product import (
    insert_product, update_product as crud_update_product,
    delete_product as crud_delete_product, fetch_products, fetch_product_by_id
)

def add_product(data: dict) -> int:
    """Add a new product. Validates name and price before inserting."""
    if not data.get("name") or not str(data["name"]).strip():
        raise ValueError("Product name must be a non-empty string")
    if not data.get("price") or float(data["price"]) <= 0:
        raise ValueError("Product price must be greater than zero")
    conn = get_connection()
    try:
        return insert_product(conn, data)
    finally:
        conn.close()

def update_product(product_id: int, data: dict) -> bool:
    """Update product fields. Raises ValueError if product not found."""
    conn = get_connection()
    try:
        if not fetch_product_by_id(conn, product_id):
            raise ValueError(f"Product {product_id} not found")
        return crud_update_product(conn, product_id, data)
    finally:
        conn.close()

def delete_product(product_id: int) -> bool:
    """Delete a product. Raises ValueError if product not found."""
    conn = get_connection()
    try:
        if not fetch_product_by_id(conn, product_id):
            raise ValueError(f"Product {product_id} not found")
        return crud_delete_product(conn, product_id)
    finally:
        conn.close()

def get_products(category: str = None, search: str = None, sort_by: str = "name") -> list:
    """Fetch products with optional filters."""
    conn = get_connection()
    try:
        return fetch_products(conn, category=category, search=search, sort_by=sort_by)
    finally:
        conn.close()

def get_product(product_id: int) -> dict:
    """Fetch a single product by ID."""
    conn = get_connection()
    try:
        product = fetch_product_by_id(conn, product_id)
        if not product:
            raise ValueError(f"Product {product_id} not found")
        return product
    finally:
        conn.close()

def record_view(product_id: int) -> None:
    """Increment the view counter for a product in analytics."""
    conn = get_connection()
    try:
        conn.execute(
            """INSERT INTO analytics (product_id, views, added_to_cart, purchased)
               VALUES (?, 1, 0, 0)
               ON CONFLICT(product_id) DO UPDATE SET views = views + 1""",
            (product_id,)
        )
        conn.commit()
    finally:
        conn.close()
