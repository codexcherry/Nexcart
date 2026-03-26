"""Update existing nithin@gmail.com user to admin role."""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "nexcart.db")

def update_admin():
    """Update nithin@gmail.com to admin role."""
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            "UPDATE users SET role = 'admin', name = 'Nithin (Admin)' WHERE email = 'nithin@gmail.com'"
        )
        conn.commit()
        print("✅ Updated nithin@gmail.com to admin role")
        
        # Verify
        cursor = conn.execute("SELECT user_id, name, email, role FROM users WHERE email = 'nithin@gmail.com'")
        user = cursor.fetchone()
        if user:
            print(f"   User: {user}")
    except Exception as e:
        print(f"❌ Update failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    update_admin()
