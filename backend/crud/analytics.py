import sqlite3
from typing import Optional


def upsert_analytics_view(conn: sqlite3.Connection, product_id: int) -> None:
    """Increment the views counter for a product."""
    conn.execute(
        """INSERT INTO analytics (product_id, views, added_to_cart, purchased)
           VALUES (?, 1, 0, 0)
           ON CONFLICT(product_id) DO UPDATE SET views = views + 1""",
        (product_id,)
    )
    conn.commit()


def upsert_analytics_cart(conn: sqlite3.Connection, product_id: int) -> None:
    """Increment the added_to_cart counter for a product."""
    conn.execute(
        """INSERT INTO analytics (product_id, views, added_to_cart, purchased)
           VALUES (?, 0, 1, 0)
           ON CONFLICT(product_id) DO UPDATE SET added_to_cart = added_to_cart + 1""",
        (product_id,)
    )
    conn.commit()


def upsert_analytics_purchase(conn: sqlite3.Connection, product_id: int, quantity: int = 1) -> None:
    """Increment the purchased counter for a product by quantity."""
    conn.execute(
        """INSERT INTO analytics (product_id, views, added_to_cart, purchased)
           VALUES (?, 0, 0, ?)
           ON CONFLICT(product_id) DO UPDATE SET purchased = purchased + ?""",
        (product_id, quantity, quantity)
    )
    conn.commit()


def fetch_analytics(conn: sqlite3.Connection, product_id: int) -> Optional[dict]:
    """Fetch analytics row for a product."""
    row = conn.execute(
        "SELECT * FROM analytics WHERE product_id = ?", (product_id,)
    ).fetchone()
    return dict(row) if row else None


def get_analytics_report(conn: sqlite3.Connection) -> dict:
    """Generate the full analytics report."""
    top_selling = conn.execute(
        """SELECT p.name, p.product_id, a.purchased
           FROM analytics a JOIN products p USING(product_id)
           ORDER BY a.purchased DESC LIMIT 10"""
    ).fetchall()

    trending = conn.execute(
        """SELECT p.name, p.product_id, a.views, a.added_to_cart,
                  (a.views + a.added_to_cart * 2) AS trend_score
           FROM analytics a JOIN products p USING(product_id)
           ORDER BY trend_score DESC LIMIT 10"""
    ).fetchall()

    total_revenue_row = conn.execute(
        "SELECT COALESCE(SUM(total_amount), 0.0) FROM orders WHERE status = 'PLACED'"
    ).fetchone()
    total_revenue = total_revenue_row[0] if total_revenue_row else 0.0

    most_active_users = conn.execute(
        """SELECT u.name, u.email, COUNT(o.order_id) AS order_count,
                  COALESCE(SUM(o.total_amount), 0) AS total_spent
           FROM orders o JOIN users u USING(user_id)
           GROUP BY o.user_id ORDER BY order_count DESC LIMIT 5"""
    ).fetchall()

    return {
        "top_selling": [dict(r) for r in top_selling],
        "trending": [dict(r) for r in trending],
        "total_revenue": total_revenue,
        "most_active_users": [dict(r) for r in most_active_users],
    }
