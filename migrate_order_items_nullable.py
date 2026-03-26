"""Migration script to allow NULL product_id in order_items for deleted products."""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "nexcart.db")

def migrate():
    """Recreate order_items table to allow NULL product_id."""
    conn = sqlite3.connect(DB_PATH)
    try:
        print("Creating backup of order_items...")
        
        # Create temporary table with existing data
        conn.execute("""
            CREATE TABLE order_items_backup AS 
            SELECT * FROM order_items
        """)
        
        # Drop old table
        conn.execute("DROP TABLE order_items")
        
        # Create new table with nullable product_id
        conn.execute("""
            CREATE TABLE order_items (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id   INTEGER NOT NULL REFERENCES orders(order_id),
                product_id INTEGER REFERENCES products(product_id),
                quantity   INTEGER NOT NULL,
                price      REAL    NOT NULL,
                product_name TEXT
            )
        """)
        
        # Copy data back
        conn.execute("""
            INSERT INTO order_items (id, order_id, product_id, quantity, price)
            SELECT id, order_id, product_id, quantity, price
            FROM order_items_backup
        """)
        
        # Update product names from products table
        conn.execute("""
            UPDATE order_items 
            SET product_name = (
                SELECT name FROM products WHERE products.product_id = order_items.product_id
            )
            WHERE product_id IS NOT NULL
        """)
        
        # Drop backup
        conn.execute("DROP TABLE order_items_backup")
        
        conn.commit()
        print("✅ Migration complete: order_items.product_id is now nullable")
        print("✅ Added product_name column to preserve product info")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
