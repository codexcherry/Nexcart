import sqlite3
from typing import Optional

ALLOWED_SORT_FIELDS = {"name", "price", "rating", "popularity_score"}


def insert_product(conn: sqlite3.Connection, product: dict) -> int:
    """Insert a product and return its new product_id."""
    cursor = conn.execute(
        """INSERT INTO products (name, price, stock, category, image_url, rating, num_reviews, popularity_score)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            product["name"],
            product["price"],
            product.get("stock", 0),
            product.get("category"),
            product.get("image_url"),
            product.get("rating", 0.0),
            product.get("num_reviews", 0),
            product.get("popularity_score", 0.0),
        )
    )
    conn.commit()
    return cursor.lastrowid


def update_product(conn: sqlite3.Connection, product_id: int, fields: dict) -> bool:
    """Update only the provided fields for a product. Returns True if a row was updated."""
    if not fields:
        return False
    allowed = {"name", "price", "stock", "category", "image_url", "rating", "num_reviews", "popularity_score"}
    updates = {k: v for k, v in fields.items() if k in allowed}
    if not updates:
        return False
    set_clause = ", ".join(f"{k} = ?" for k in updates)
    values = list(updates.values()) + [product_id]
    cursor = conn.execute(f"UPDATE products SET {set_clause} WHERE product_id = ?", values)
    conn.commit()
    return cursor.rowcount > 0


def delete_product(conn: sqlite3.Connection, product_id: int) -> bool:
    """Delete a product and all its dependent rows. Returns True if a row was deleted."""
    # First, get the product name to preserve in order history
    product = conn.execute("SELECT name FROM products WHERE product_id = ?", (product_id,)).fetchone()
    if product:
        product_name = product[0]
        # Update order_items to preserve product name and set product_id to NULL
        conn.execute(
            "UPDATE order_items SET product_name = ?, product_id = NULL WHERE product_id = ?",
            (product_name, product_id)
        )
    
    # Clear FK references in order: cart → analytics → products
    conn.execute("DELETE FROM cart WHERE product_id = ?", (product_id,))
    conn.execute("DELETE FROM analytics WHERE product_id = ?", (product_id,))
    cursor = conn.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
    conn.commit()
    return cursor.rowcount > 0


def fetch_products(
    conn: sqlite3.Connection,
    category: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = "name",
    limit: int = 50
) -> list:
    """Fetch products with optional category filter, search, sort, and limit."""
    if sort_by not in ALLOWED_SORT_FIELDS:
        raise ValueError(f"Invalid sort_by '{sort_by}'. Must be one of {ALLOWED_SORT_FIELDS}")
    if limit < 1:
        raise ValueError("limit must be >= 1")

    query = "SELECT * FROM products WHERE 1=1"
    params = []

    if category is not None:
        query += " AND category = ?"
        params.append(category)

    if search is not None:
        query += " AND name LIKE ?"
        params.append(f"%{search}%")

    query += f" ORDER BY {sort_by} LIMIT ?"
    params.append(limit)

    rows = conn.execute(query, params).fetchall()
    return [dict(row) for row in rows]


def fetch_product_by_id(conn: sqlite3.Connection, product_id: int) -> Optional[dict]:
    """Fetch a single product by ID, or None if not found."""
    row = conn.execute("SELECT * FROM products WHERE product_id = ?", (product_id,)).fetchone()
    return dict(row) if row else None


def update_stock(conn: sqlite3.Connection, product_id: int, delta: int) -> bool:
    """Adjust stock by delta (negative to decrement). Returns True if updated."""
    cursor = conn.execute(
        "UPDATE products SET stock = stock + ? WHERE product_id = ?",
        (delta, product_id)
    )
    conn.commit()
    return cursor.rowcount > 0
