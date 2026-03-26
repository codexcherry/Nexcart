import sqlite3


def upsert_cart_item(conn: sqlite3.Connection, user_id: int, product_id: int, quantity: int) -> None:
    """Insert or replace a cart item (replace semantics on conflict)."""
    conn.execute(
        """INSERT INTO cart (user_id, product_id, quantity)
           VALUES (?, ?, ?)
           ON CONFLICT(user_id, product_id)
           DO UPDATE SET quantity = excluded.quantity, added_at = datetime('now')""",
        (user_id, product_id, quantity)
    )
    conn.commit()


def update_cart_quantity(conn: sqlite3.Connection, cart_id: int, quantity: int) -> bool:
    """Update quantity for a specific cart row."""
    cursor = conn.execute(
        "UPDATE cart SET quantity = ? WHERE cart_id = ?",
        (quantity, cart_id)
    )
    conn.commit()
    return cursor.rowcount > 0


def delete_cart_item(conn: sqlite3.Connection, cart_id: int) -> bool:
    """Remove a specific cart item by cart_id."""
    cursor = conn.execute("DELETE FROM cart WHERE cart_id = ?", (cart_id,))
    conn.commit()
    return cursor.rowcount > 0


def fetch_cart(conn: sqlite3.Connection, user_id: int) -> list:
    """Fetch all cart items for a user, joined with product details."""
    rows = conn.execute(
        """SELECT c.cart_id, c.user_id, c.product_id, c.quantity, c.added_at,
                  p.name, p.price, p.stock, p.image_url, p.category
           FROM cart c
           JOIN products p ON c.product_id = p.product_id
           WHERE c.user_id = ?
           ORDER BY c.added_at""",
        (user_id,)
    ).fetchall()
    return [dict(row) for row in rows]


def clear_cart(conn: sqlite3.Connection, user_id: int) -> None:
    """Remove all cart items for a user."""
    conn.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
    conn.commit()
