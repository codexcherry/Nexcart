import os
from datetime import datetime
from pathlib import Path

from backend.db import get_connection
from backend.crud.analytics import get_analytics_report

DATA_DIR = Path(__file__).parent.parent / "data"
REPORTS_PATH = DATA_DIR / "reports.txt"


def write_report() -> str:
    """Generate and write the analytics report to reports.txt. Returns the report text."""
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = get_connection()
    try:
        report = get_analytics_report(conn)
    finally:
        conn.close()

    lines = [
        f"=== NexCart Analytics Report ===",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"Total Revenue: ₹{report['total_revenue']:,.2f}",
        "",
        "Top Selling Products:",
    ]
    for i, p in enumerate(report["top_selling"], 1):
        lines.append(f"  {i}. {p['name']} — {p['purchased']} units sold")

    lines += ["", "Trending Products:"]
    for i, p in enumerate(report["trending"], 1):
        lines.append(f"  {i}. {p['name']} — {p['views']} views, {p['added_to_cart']} cart adds")

    lines += ["", "Most Active Users:"]
    for i, u in enumerate(report["most_active_users"], 1):
        lines.append(f"  {i}. {u['name']} ({u['email']}) — {u['order_count']} orders, ₹{u['total_spent']:,.2f} spent")

    text = "\n".join(lines) + "\n"
    with open(REPORTS_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    return text
