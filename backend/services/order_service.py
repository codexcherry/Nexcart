import os
import random
from datetime import datetime, timedelta
from pathlib import Path

from backend.db import get_connection
from backend.crud.cart import fetch_cart
from backend.crud.product import fetch_product_by_id
from backend.crud.order import insert_order, insert_order_items, fetch_orders, fetch_order_items

DATA_DIR = Path(__file__).parent.parent.parent / "data"
LOGS_PATH = DATA_DIR / "logs.txt"


def _log_order(order_id: int, user_id: int, total: float) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOGS_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] ORDER_PLACED order_id={order_id} user_id={user_id} total={total:.2f}\n")


def _log_error(message: str) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOGS_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] ERROR {message}\n")


def place_order(user_id: int) -> dict:
    """
    Atomically place a COD order from the user's cart.
    All DB writes happen in a single transaction — no intermediate commits.
    """
    conn = get_connection()
    # Disable autocommit so intermediate CRUD calls don't commit mid-transaction
    conn.isolation_level = None  # manual transaction control
    try:
        # Step 1: Fetch and validate cart
        cart_items = fetch_cart(conn, user_id)
        if not cart_items:
            raise ValueError("Cannot place order with empty cart")

        # Step 2: Validate stock for ALL items before touching DB
        for item in cart_items:
            product = fetch_product_by_id(conn, item["product_id"])
            if not product:
                raise ValueError(f"Product {item['product_id']} not found")
            if item["quantity"] > product["stock"]:
                raise ValueError(
                    f"Insufficient stock for '{product['name']}' "
                    f"(available: {product['stock']}, requested: {item['quantity']})"
                )

        # Step 3: Compute total and delivery estimate
        total = round(sum(item["price"] * item["quantity"] for item in cart_items), 2)
        delivery_estimate = (datetime.now() + timedelta(days=random.randint(3, 5))).strftime("%Y-%m-%d")

        # Step 4: Single atomic transaction — no conn.commit() inside
        conn.execute("BEGIN")
        try:
            order_id = conn.execute(
                """INSERT INTO orders (user_id, total_amount, status, payment_mode, delivery_estimate)
                   VALUES (?, ?, 'PLACED', 'COD', ?)""",
                (user_id, total, delivery_estimate)
            ).lastrowid

            # Insert order items with product names
            for item in cart_items:
                product = fetch_product_by_id(conn, item["product_id"])
                conn.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity, price, product_name) VALUES (?, ?, ?, ?, ?)",
                    (order_id, item["product_id"], item["quantity"], item["price"], product["name"])
                )

            for item in cart_items:
                conn.execute(
                    "UPDATE products SET stock = stock - ? WHERE product_id = ?",
                    (item["quantity"], item["product_id"])
                )
                conn.execute(
                    """INSERT INTO analytics (product_id, views, added_to_cart, purchased)
                       VALUES (?, 0, 0, ?)
                       ON CONFLICT(product_id) DO UPDATE SET purchased = purchased + ?""",
                    (item["product_id"], item["quantity"], item["quantity"])
                )

            conn.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
            conn.execute("COMMIT")

        except Exception as e:
            try:
                conn.execute("ROLLBACK")
            except Exception:
                pass
            _log_error(str(e))
            raise

        _log_order(order_id, user_id, total)
        return {"order_id": order_id, "total_amount": total, "delivery_estimate": delivery_estimate}

    finally:
        conn.close()


def get_orders(user_id: int) -> list:
    conn = get_connection()
    try:
        orders = fetch_orders(conn, user_id)
        for order in orders:
            order["items"] = fetch_order_items(conn, order["order_id"])
        return orders
    finally:
        conn.close()
