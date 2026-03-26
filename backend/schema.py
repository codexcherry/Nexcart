import sqlite3

def create_tables(conn: sqlite3.Connection) -> None:
    """Create all NexCart tables if they don't exist."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS products (
            product_id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name             TEXT    NOT NULL,
            price            REAL    NOT NULL CHECK(price > 0),
            stock            INTEGER NOT NULL DEFAULT 0 CHECK(stock >= 0),
            category         TEXT,
            image_url        TEXT,
            created_at       TEXT    DEFAULT (datetime('now')),
            rating           REAL    DEFAULT 0.0,
            num_reviews      INTEGER DEFAULT 0,
            popularity_score REAL    DEFAULT 0.0
        );

        CREATE TABLE IF NOT EXISTS users (
            user_id     INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            email       TEXT    NOT NULL UNIQUE,
            role        TEXT    DEFAULT 'customer' CHECK(role IN ('admin', 'customer')),
            created_at  TEXT    DEFAULT (datetime('now')),
            last_active TEXT    DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS cart (
            cart_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL REFERENCES users(user_id),
            product_id INTEGER NOT NULL REFERENCES products(product_id),
            quantity   INTEGER NOT NULL CHECK(quantity >= 1),
            added_at   TEXT    DEFAULT (datetime('now')),
            UNIQUE(user_id, product_id)
        );

        CREATE TABLE IF NOT EXISTS orders (
            order_id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id           INTEGER NOT NULL REFERENCES users(user_id),
            total_amount      REAL    NOT NULL,
            status            TEXT    DEFAULT 'PLACED',
            payment_mode      TEXT    DEFAULT 'COD',
            created_at        TEXT    DEFAULT (datetime('now')),
            delivery_estimate TEXT
        );

        CREATE TABLE IF NOT EXISTS order_items (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id     INTEGER NOT NULL REFERENCES orders(order_id),
            product_id   INTEGER REFERENCES products(product_id),
            quantity     INTEGER NOT NULL,
            price        REAL    NOT NULL,
            product_name TEXT
        );

        CREATE TABLE IF NOT EXISTS analytics (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id    INTEGER NOT NULL UNIQUE REFERENCES products(product_id),
            views         INTEGER DEFAULT 0,
            added_to_cart INTEGER DEFAULT 0,
            purchased     INTEGER DEFAULT 0
        );
    """)
    conn.commit()
