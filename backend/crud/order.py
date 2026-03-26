import sqlite3
from typing import Optional


def insert_order(
    conn: sqlite3.Connection,
    user_id: int,
    total: float,
    payment_mode: str,
    delivery_estimate: str
) -> int:
    """Insert a new order and return its order_id."""
    cursor = conn.execute(
        """INSERT INTO orders (user_id, total_amount, status, payment_mode, delivery_estimate)
           VALUES (?, ?, 'PLACED', ?, ?)""",
        (user_id, total, payment_mode, delivery_estimate)
    )
    return cursor.lastrowid


def insert_order_items(conn: sqlite3.Connection, order_id: int, items: list) -> None:
    """Batch insert order items with snapshotted prices."""
    conn.executemany(
        "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
        [(order_id, item["product_id"], item["quantity"], item["price"]) for item in items]
    )


def fetch_orders(conn: sqlite3.Connection, user_id: int) -> list:
    """Fetch all orders for a user, newest first."""
    rows = conn.execute(
        "SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,)
    ).fetchall()
    return [dict(row) for row in rows]


def fetch_order_items(conn: sqlite3.Connection, order_id: int) -> list:
    """Fetch all items for a specific order, with product name from products table or saved name."""
    rows = conn.execute(
        """SELECT oi.id, oi.order_id, oi.product_id, oi.quantity, oi.price,
                  COALESCE(p.name, oi.product_name, '[Deleted Product]') as name
           FROM order_items oi
           LEFT JOIN products p ON oi.product_id = p.product_id
           WHERE oi.order_id = ?""",
        (order_id,)
    ).fetchall()
    return [dict(row) for row in rows]


def fetch_all_orders(conn: sqlite3.Connection) -> list:
    """Fetch all orders (admin view), newest first."""
    rows = conn.execute(
        """SELECT o.*, u.name as user_name, u.email
           FROM orders o JOIN users u ON o.user_id = u.user_id
           ORDER BY o.created_at DESC"""
    ).fetchall()
    return [dict(row) for row in rows]
