"""Seed the database with sample Indian products and admin user on first run."""
from backend.db import get_connection


def seed_admin_user() -> bool:
    """Create admin user if not exists. Returns True if created."""
    conn = get_connection()
    try:
        # Check if admin exists
        existing = conn.execute(
            "SELECT user_id FROM users WHERE email = ?", 
            ("nithin@gmail.com",)
        ).fetchone()
        
        if existing:
            return False
        
        # Create admin user
        conn.execute(
            "INSERT INTO users (name, email, role) VALUES (?, ?, ?)",
            ("Nithin (Admin)", "nithin@gmail.com", "admin")
        )
        conn.commit()
        return True
    finally:
        conn.close()


SAMPLE_PRODUCTS = [
    {
        "name": "boAt Rockerz 450 Bluetooth Headphones",
        "price": 1299.0, "stock": 85, "category": "Electronics",
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400",
        "rating": 4.5, "num_reviews": 2341, "popularity_score": 9.2,
    },
    {
        "name": "Levi's Men's Slim Fit Jeans",
        "price": 2499.0, "stock": 120, "category": "Clothing",
        "image_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400",
        "rating": 4.3, "num_reviews": 876, "popularity_score": 8.1,
    },
    {
        "name": "Prestige Iris 750W Mixer Grinder",
        "price": 3199.0, "stock": 42, "category": "Home & Kitchen",
        "image_url": "https://images.unsplash.com/photo-1585515320310-259814833e62?w=400",
        "rating": 4.4, "num_reviews": 1203, "popularity_score": 8.7,
    },
    {
        "name": "Atomic Habits — James Clear",
        "price": 399.0, "stock": 200, "category": "Books",
        "image_url": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400",
        "rating": 4.8, "num_reviews": 5621, "popularity_score": 9.8,
    },
    {
        "name": "Redmi Note 13 Pro (8GB/256GB)",
        "price": 24999.0, "stock": 30, "category": "Electronics",
        "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400",
        "rating": 4.6, "num_reviews": 3102, "popularity_score": 9.5,
    },
    {
        "name": "Yoga Mat Anti-Slip 6mm",
        "price": 699.0, "stock": 5, "category": "Sports",
        "image_url": "https://images.unsplash.com/photo-1601925228008-f5e4c5e5e5e5?w=400",
        "rating": 4.2, "num_reviews": 432, "popularity_score": 7.3,
    },
    {
        "name": "Lakme Absolute Skin Natural Mousse SPF 8",
        "price": 549.0, "stock": 60, "category": "Beauty",
        "image_url": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400",
        "rating": 4.1, "num_reviews": 789, "popularity_score": 7.8,
    },
    {
        "name": "Milton Thermosteel Flip Lid Flask 1L",
        "price": 899.0, "stock": 75, "category": "Home & Kitchen",
        "image_url": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400",
        "rating": 4.5, "num_reviews": 1567, "popularity_score": 8.9,
    },
    {
        "name": "LEGO Classic Creative Bricks Set",
        "price": 1999.0, "stock": 0, "category": "Toys",
        "image_url": "https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400",
        "rating": 4.7, "num_reviews": 654, "popularity_score": 8.4,
    },
    {
        "name": "Fastrack Analog Watch for Men",
        "price": 1795.0, "stock": 18, "category": "Clothing",
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400",
        "rating": 4.3, "num_reviews": 921, "popularity_score": 8.0,
    },
]


def seed_products() -> int:
    """Insert sample products if the products table is empty. Returns count inserted."""
    conn = get_connection()
    try:
        count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        if count > 0:
            return 0
        inserted = 0
        for p in SAMPLE_PRODUCTS:
            conn.execute(
                """INSERT INTO products
                   (name, price, stock, category, image_url, rating, num_reviews, popularity_score)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (p["name"], p["price"], p["stock"], p["category"],
                 p["image_url"], p["rating"], p["num_reviews"], p["popularity_score"])
            )
            inserted += 1
        conn.commit()
        return inserted
    finally:
        conn.close()
