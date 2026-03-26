import sqlite3
from backend.db import get_connection
from backend.crud.cart import (
    upsert_cart_item, update_cart_quantity, delete_cart_item,
    fetch_cart, clear_cart
)
from backend.crud.product import fetch_product_by_id


def add_to_cart(user_id: int, product_id: int, quantity: int) -> dict:
    """Add or update a cart item with stock validation."""
    if quantity < 1:
        raise ValueError("Quantity must be >= 1")
    conn = get_connection()
    try:
        product = fetch_product_by_id(conn, product_id)
        if not product:
            raise ValueError(f"Product {product_id} not found")
        if product["stock"] == 0:
            return {"success": False, "message": "Out of stock"}
        if quantity > product["stock"]:
            raise ValueError(f"Only {product['stock']} units available")
        upsert_cart_item(conn, user_id, product_id, quantity)
        conn.execute(
            """INSERT INTO analytics (product_id, views, added_to_cart, purchased)
               VALUES (?, 0, 1, 0)
               ON CONFLICT(product_id) DO UPDATE SET added_to_cart = added_to_cart + 1""",
            (product_id,)
        )
        conn.commit()
        cart = fetch_cart(conn, user_id)
        return {"success": True, "message": "Added to cart", "cart_item_count": len(cart)}
    finally:
        conn.close()


def get_cart(user_id: int) -> dict:
    """Return enriched cart with subtotal and item count."""
    conn = get_connection()
    try:
        items = fetch_cart(conn, user_id)
        for item in items:
            item["out_of_stock"] = item["stock"] == 0
            item["line_total"] = round(item["price"] * item["quantity"], 2)
        subtotal = round(sum(i["price"] * i["quantity"] for i in items), 2)
        return {"items": items, "subtotal": subtotal, "item_count": len(items)}
    finally:
        conn.close()


def update_cart(cart_id: int, quantity: int) -> dict:
    """Update quantity for a cart item with stock validation."""
    if quantity < 1:
        raise ValueError("Quantity must be >= 1")
    conn = get_connection()
    try:
        row = conn.execute(
            """SELECT c.quantity, p.stock FROM cart c
               JOIN products p ON c.product_id = p.product_id
               WHERE c.cart_id = ?""",
            (cart_id,)
        ).fetchone()
        if not row:
            raise ValueError(f"Cart item {cart_id} not found")
        if quantity > row["stock"]:
            raise ValueError(f"Only {row['stock']} units available")
        update_cart_quantity(conn, cart_id, quantity)
        return {"success": True, "message": "Cart updated"}
    finally:
        conn.close()


def remove_from_cart(cart_id: int) -> None:
    """Remove a cart item."""
    conn = get_connection()
    try:
        delete_cart_item(conn, cart_id)
    finally:
        conn.close()
