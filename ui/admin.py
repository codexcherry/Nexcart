import streamlit as st
import pandas as pd
from backend.services.product_service import add_product, update_product, delete_product, get_products
from backend.services.user_service import add_user, get_all_users
from backend.crud.order import fetch_all_orders
from backend.db import get_connection
from backend.crud.analytics import get_analytics_report
from utils.helpers import format_currency
from utils.reporter import write_report


def _check_admin_access() -> bool:
    """Check if current user is admin. Returns True if admin, False otherwise."""
    user_id = st.session_state.get("user_id")
    if not user_id:
        return False
    
    conn = get_connection()
    try:
        user_row = conn.execute("SELECT role FROM users WHERE user_id = ?", (user_id,)).fetchone()
        if user_row and user_row[0] == "admin":
            return True
        return False
    finally:
        conn.close()


_CSS = """
<style>
.admin-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border-radius: 16px;
    padding: 24px 32px;
    margin-bottom: 24px;
    border: 1px solid #2a2a3e;
}
.admin-title {
    font-size: 1.8rem;
    font-weight: 800;
    color: #00e676;
    margin-bottom: 4px;
}
.admin-subtitle {
    font-size: 0.9rem;
    color: #888;
}
.metric-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%);
    border: 1px solid #2a2a3e;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    transition: transform 0.2s;
}
.metric-card:hover {
    transform: translateY(-4px);
    border-color: #00e676;
}
.metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: #00e676;
    margin-bottom: 4px;
}
.metric-label {
    font-size: 0.85rem;
    color: #aaa;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.metric-change {
    font-size: 0.75rem;
    color: #00e676;
    margin-top: 4px;
}
.section-header {
    font-size: 1.2rem;
    font-weight: 700;
    color: #e8e8e8;
    margin: 32px 0 16px;
    padding-bottom: 8px;
    border-bottom: 2px solid #2a2a3e;
}
.action-card {
    background: #1a1a2e;
    border: 1px solid #2a2a3e;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
}
.status-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
}
.status-placed { background: #0d2818; color: #00e676; }
.status-shipped { background: #1a2d3d; color: #40c4ff; }
.status-delivered { background: #2d1f00; color: #ffab40; }
</style>
"""


def render():
    # Check admin access
    if not _check_admin_access():
        st.markdown(_CSS, unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center; padding:80px 20px;">
            <div style="font-size:4rem; margin-bottom:20px;">🔒</div>
            <div style="font-size:1.5rem; font-weight:700; color:#ff5252; margin-bottom:12px;">Access Denied</div>
            <div style="color:#888; margin-bottom:24px;">Admin privileges required to access this page</div>
            <div style="background:#1a1a2e; border:1px solid #2a2a3e; border-radius:12px; padding:20px; max-width:400px; margin:0 auto;">
                <div style="color:#aaa; font-size:0.9rem; margin-bottom:8px;">Admin Account:</div>
                <div style="color:#00e676; font-weight:700;">nithin@gmail.com</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown(_CSS, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="admin-header">
        <div class="admin-title">🧑‍💼 Admin Dashboard</div>
        <div class="admin-subtitle">Manage products, orders, and analytics</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get analytics data
    conn = get_connection()
    try:
        total_products = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        total_users = conn.execute("SELECT COUNT(*) FROM users WHERE role='customer'").fetchone()[0]
        total_orders = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        total_revenue = conn.execute("SELECT COALESCE(SUM(total_amount), 0) FROM orders").fetchone()[0]
        low_stock = conn.execute("SELECT COUNT(*) FROM products WHERE stock <= 5 AND stock > 0").fetchone()[0]
        out_of_stock = conn.execute("SELECT COUNT(*) FROM products WHERE stock = 0").fetchone()[0]
    finally:
        conn.close()
    
    # Metrics Dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size:2.5rem; margin-bottom:8px;">📦</div>
            <div class="metric-value">{total_products}</div>
            <div class="metric-label">Total Products</div>
            <div class="metric-change">⚠️ {low_stock} low stock</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size:2.5rem; margin-bottom:8px;">👥</div>
            <div class="metric-value">{total_users}</div>
            <div class="metric-label">Customers</div>
            <div class="metric-change">Active users</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size:2.5rem; margin-bottom:8px;">🛍️</div>
            <div class="metric-value">{total_orders}</div>
            <div class="metric-label">Total Orders</div>
            <div class="metric-change">All time</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size:2.5rem; margin-bottom:8px;">💰</div>
            <div class="metric-value">{format_currency(total_revenue)}</div>
            <div class="metric-label">Revenue</div>
            <div class="metric-change">Total earnings</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📦 Products", "🛍️ Orders", "📊 Analytics", "👥 Users"])
    
    # TAB 1: Products Management
    with tab1:
        st.markdown('<div class="section-header">Product Management</div>', unsafe_allow_html=True)
        
        col_a, col_b = st.columns([2, 1])
        with col_a:
            st.markdown("### Add New Product")
        with col_b:
            if st.button("🔄 Refresh Products", use_container_width=True):
                st.rerun()
        
        # Add Product Form
        with st.form("add_product_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Product Name *", placeholder="e.g. iPhone 15 Pro")
                price = st.number_input("Price (₹) *", min_value=0.0, step=100.0)
                stock = st.number_input("Stock Quantity *", min_value=0, step=1)
            with col2:
                category = st.selectbox("Category", ["Electronics", "Clothing", "Books", "Home & Kitchen", "Sports", "Beauty", "Toys", "Other"])
                rating = st.slider("Rating", 0.0, 5.0, 4.0, 0.1)
                num_reviews = st.number_input("Number of Reviews", min_value=0, step=1, value=0)
            
            image_url = st.text_input("Image URL", placeholder="https://example.com/image.jpg")
            
            if st.form_submit_button("➕ Add Product", type="primary", use_container_width=True):
                try:
                    add_product({
                        "name": name,
                        "price": price,
                        "stock": stock,
                        "category": category,
                        "image_url": image_url or None,
                        "rating": rating,
                        "num_reviews": num_reviews,
                        "popularity_score": rating * 2
                    })
                    st.success(f"✅ Product '{name}' added successfully!")
                    st.rerun()
                except ValueError as e:
                    st.error(f"❌ {str(e)}")
        
        st.markdown('<div class="section-header">All Products</div>', unsafe_allow_html=True)
        
        # Products Table
        products = get_products()
        if products:
            # Create DataFrame for better display
            df = pd.DataFrame(products)
            df = df[['product_id', 'name', 'price', 'stock', 'category', 'rating', 'num_reviews']]
            df.columns = ['ID', 'Name', 'Price (₹)', 'Stock', 'Category', 'Rating', 'Reviews']
            
            # Display as interactive table
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Price (₹)": st.column_config.NumberColumn(format="₹%.2f"),
                    "Rating": st.column_config.NumberColumn(format="⭐ %.1f"),
                    "Stock": st.column_config.NumberColumn(
                        help="Inventory count",
                        format="%d units"
                    )
                }
            )
            
            # Product Actions
            st.markdown("### Quick Actions")
            action_col1, action_col2 = st.columns(2)
            
            with action_col1:
                product_ids = [p["product_id"] for p in products]
                product_names = [f"{p['product_id']} - {p['name']}" for p in products]
                selected = st.selectbox("Select Product to Edit/Delete", product_names)
                selected_id = int(selected.split(" - ")[0])
            
            with action_col2:
                st.write("")
                st.write("")
                if st.button("🗑️ Delete Selected Product", type="secondary", use_container_width=True):
                    try:
                        delete_product(selected_id)
                        st.success("✅ Product deleted!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ {str(e)}")
        else:
            st.info("📦 No products found. Add your first product above!")
    
    # TAB 2: Orders Management
    with tab2:
        st.markdown('<div class="section-header">Order Management</div>', unsafe_allow_html=True)
        
        conn = get_connection()
        try:
            orders = fetch_all_orders(conn)
        finally:
            conn.close()
        
        if orders:
            # Orders DataFrame
            df_orders = pd.DataFrame(orders)
            df_orders = df_orders[['order_id', 'user_name', 'email', 'total_amount', 'status', 'payment_mode', 'created_at']]
            df_orders.columns = ['Order ID', 'Customer', 'Email', 'Amount (₹)', 'Status', 'Payment', 'Date']
            
            st.dataframe(
                df_orders,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Amount (₹)": st.column_config.NumberColumn(format="₹%.2f"),
                    "Status": st.column_config.TextColumn(help="Order status")
                }
            )
            
            # Order Details Expander
            st.markdown("### Order Details")
            for order in orders[:10]:  # Show last 10 orders
                with st.expander(f"Order #{order['order_id']} - {order['user_name']} - {format_currency(order['total_amount'])}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"**Customer:** {order['user_name']}")
                        st.markdown(f"**Email:** {order['email']}")
                    with col2:
                        st.markdown(f"**Status:** `{order['status']}`")
                        st.markdown(f"**Payment:** {order['payment_mode']}")
                    with col3:
                        st.markdown(f"**Date:** {order['created_at'][:16]}")
                        st.markdown(f"**Amount:** {format_currency(order['total_amount'])}")
        else:
            st.info("📦 No orders yet")
    
    # TAB 3: Analytics
    with tab3:
        st.markdown('<div class="section-header">Analytics & Insights</div>', unsafe_allow_html=True)
        
        conn = get_connection()
        try:
            report = get_analytics_report(conn)
        finally:
            conn.close()
        
        # Top Selling Products
        st.markdown("### 🔥 Top Selling Products")
        if report['top_selling']:
            top_df = pd.DataFrame(report['top_selling'])
            top_df = top_df[['name', 'purchased']]
            top_df.columns = ['Product', 'Units Sold']
            st.dataframe(top_df, use_container_width=True, hide_index=True)
        else:
            st.info("No sales data yet")
        
        # Trending Products
        st.markdown("### 📈 Trending Products")
        if report['trending']:
            trend_df = pd.DataFrame(report['trending'])
            trend_df = trend_df[['name', 'views', 'added_to_cart', 'trend_score']]
            trend_df.columns = ['Product', 'Views', 'Cart Adds', 'Trend Score']
            st.dataframe(trend_df, use_container_width=True, hide_index=True)
        else:
            st.info("No trending data yet")
        
        # Most Active Users
        st.markdown("### 👥 Most Active Users")
        if report['most_active_users']:
            users_df = pd.DataFrame(report['most_active_users'])
            users_df = users_df[['name', 'email', 'order_count', 'total_spent']]
            users_df.columns = ['User', 'Email', 'Orders', 'Total Spent (₹)']
            st.dataframe(users_df, use_container_width=True, hide_index=True)
        else:
            st.info("No user activity yet")
        
        # Generate Report
        if st.button("📄 Generate Full Report", type="primary"):
            report_text = write_report()
            st.success("✅ Report generated successfully")
            st.text_area("Report Preview", report_text, height=300)
    
    # TAB 4: Users
    with tab4:
        st.markdown('<div class="section-header">User Management</div>', unsafe_allow_html=True)
        
        users = get_all_users()
        if users:
            df_users = pd.DataFrame(users)
            df_users = df_users[['user_id', 'name', 'email', 'role', 'created_at']]
            df_users.columns = ['ID', 'Name', 'Email', 'Role', 'Joined']
            
            st.dataframe(
                df_users,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Role": st.column_config.TextColumn(help="User role")
                }
            )
        else:
            st.info("👥 No users found")
