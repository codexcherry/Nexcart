import os
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
LOGS_PATH = DATA_DIR / "logs.txt"


def _write(line: str) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOGS_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {line}\n")


def log_order(order_id: int, user_id: int, total: float) -> None:
    _write(f"ORDER_PLACED order_id={order_id} user_id={user_id} total={total:.2f}")


def log_product_added(product_id: int, name: str) -> None:
    _write(f"PRODUCT_ADDED product_id={product_id} name={name!r}")


def log_user_created(user_id: int, email: str) -> None:
    _write(f"USER_CREATED user_id={user_id} email={email!r}")


def log_error(message: str) -> None:
    _write(f"ERROR {message}")
