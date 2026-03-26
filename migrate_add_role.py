"""Migration script to add role column to existing users table."""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "nexcart.db")

def migrate():
    """Add role column to users table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    try:
        # Check if role column exists
        cursor = conn.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if "role" not in columns:
            print("Adding 'role' column to users table...")
            conn.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'customer' CHECK(role IN ('admin', 'customer'))")
            conn.commit()
            print("✅ Migration complete: role column added")
        else:
            print("✅ Role column already exists, no migration needed")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
