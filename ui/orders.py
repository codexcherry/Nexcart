import streamlit as st
from backend.services.order_service import get_orders
from utils.helpers import format_currency

_CSS = """
<style>
.orders-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border-radius: 16px;
    padding: 24px 32px;
    margin-bottom: 24px;
    border: 1px solid #2a2a3e;
}
.orders-title {
    font-size: 1.8rem;
    font-weight: 800;
    color: #00e676;
    margin-bottom: 4px;
}
.orders-subtitle {
    font-size: 0.9rem;
    color: #888;
}
.order-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 1px solid #2a2a3e;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    transition: all 0.3s ease;
}
.order-card:hover {
    border-color: #00e676;
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 230, 118, 0.15);
}
.order-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    padding-bottom: 16px;
    border-bottom: 1px solid #2a2a3e;
}
.order-id {
    font-size: 1.2rem;
    font-weight: 700;
    color: #00e676;
}
.order-date {
    font-size: 0.85rem;
    color: #888;
}
.status-badge {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.status-placed {
    background: linear-gradient(135deg, #0d2818, #1a4d2e);
    color: #00e676;
    border: 1px solid #00e676;
}
.status-shipped {
    background: linear-gradient(135deg, #1a2d3d, #2a4d6d);
    color: #40c4ff;
    border: 1px solid #40c4ff;
}
.status-delivered {
    background: linear-gradient(135deg, #2d1f00, #4d3500);
    color: #ffab40;
    border: 1px solid #ffab40;
}
.order-item {
    display: flex;
    gap: 16px;
    padding: 12px;
    background: #111827;
    border-radius: 8px;
    margin-bottom: 8px;
}
.item-image {
    width: 60px;
    height: 60px;
    object-fit: cover;
    border-radius: 6px;
    background: #1a1a2e;
}
.item-details {
    flex: 1;
}
.item-name {
    font-size: 0.95rem;
    font-weight: 600;
    color: #e8e8e8;
    margin-bottom: 4px;
}
.item-meta {
    font-size: 0.8rem;
    color: #888;
}
.item-price {
    font-size: 1rem;
    font-weight: 700;
    color: #fff;
    text-align: right;
}
.order-total {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 16px;
    padding-top: 16px;
    border-top: 2px solid #2a2a3e;
}
.total-label {
    font-size: 1.1rem;
    color: #aaa;
}
.total-amount {
    font-size: 1.5rem;
    font-weight: 800;
    color: #fff;
}
.delivery-info {
    background: #0f3460;
    border: 1px solid #2a2a3e;
    border-radius: 8px;
    padding: 12px 16px;
    margin-top: 12px;
}
.success-banner {
    background: linear-gradient(135deg, #0d2818, #1a4d2e);
    border: 2px solid #00e676;
    border-radius: 20px;
    padding: 48px 40px;
    text-align: center;
    margin: 40px auto;
    max-width: 600px;
}
.success-icon {
    font-size: 5rem;
    margin-bottom: 20px;
}
.success-title {
    font-size: 2rem;
    font-weight: 800;
    color: #00e676;
    margin-bottom: 12px;
}
.success-subtitle {
    font-size: 1.1rem;
    color: #aaa;
    margin-bottom: 24px;
}
</style>
"""


def render():
    st.markdown(_CSS, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="orders-header">
        <div class="orders-title">📦 My Orders</div>
        <div class="orders-subtitle">Track and manage your orders</div>
    </div>
    """, unsafe_allow_html=True)
    
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.markdown("""
        <div style="text-align:center; padding:80px 20px;">
            <div style="font-size:5rem; margin-bottom:20px; opacity:0.5;">👤</div>
            <div style="font-size:1.3rem; font-weight:700; color:#e8e8e8; margin-bottom:12px;">Please Login</div>
            <div style="color:#888; margin-bottom:24px;">Select or register a user to view orders</div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    orders = get_orders(user_id)
    
    if not orders:
        st.markdown("""
        <div style="text-align:center; padding:80px 20px;">
            <div style="font-size:5rem; margin-bottom:20px; opacity:0.5;">📦</div>
            <div style="font-size:1.3rem; font-weight:700; color:#e8e8e8; margin-bottom:12px;">No Orders Yet</div>
            <div style="color:#888; margin-bottom:24px;">Start shopping to place your first order!</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🛍️ Start Shopping", type="primary", use_container_width=True):
            st.session_state["page"] = "Home"
            st.rerun()
        return
    
    st.markdown(f'<div style="color:#888; font-size:0.9rem; margin-bottom:20px;">📋 {len(orders)} order(s) found</div>', unsafe_allow_html=True)
    
    for order in orders:
        status_class = f"status-{order['status'].lower()}"
        
        st.markdown(f"""
        <div class="order-card">
            <div class="order-header">
                <div>
                    <div class="order-id">Order #{order['order_id']}</div>
                    <div class="order-date">📅 {order['created_at'][:16]}</div>
                </div>
                <div class="status-badge {status_class}">
                    ✓ {order['status']}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Order Items
        for item in order.get("items", []):
            st.markdown(f"""
            <div class="order-item">
                <div class="item-details">
                    <div class="item-name">{item['name']}</div>
                    <div class="item-meta">Qty: {item['quantity']} × {format_currency(item['price'])}</div>
                </div>
                <div class="item-price">{format_currency(item['price'] * item['quantity'])}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Order Total
        st.markdown(f"""
            <div class="order-total">
                <div class="total-label">Total Amount</div>
                <div class="total-amount">{format_currency(order['total_amount'])}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Delivery Info
        if order.get("delivery_estimate"):
            st.markdown(f"""
            <div class="delivery-info">
                <div style="font-size:0.85rem; color:#aaa; margin-bottom:4px;">🚚 Estimated Delivery</div>
                <div style="font-size:1rem; font-weight:700; color:#40c4ff;">{order['delivery_estimate']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Payment Mode
        st.markdown(f"""
            <div style="margin-top:12px; font-size:0.85rem; color:#888;">
                💵 Payment: <span style="color:#00e676; font-weight:600;">{order['payment_mode']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_success():
    """Render order success page"""
    st.markdown(_CSS, unsafe_allow_html=True)

    order = st.session_state.get("last_order", {})
    order_id = order.get('order_id', 'N/A')
    total = format_currency(order.get('total_amount', 0))
    delivery = order.get('delivery_estimate', 'N/A')

    st.markdown('<div class="success-banner">', unsafe_allow_html=True)
    st.markdown('<div class="success-icon">🎉</div>', unsafe_allow_html=True)
    st.markdown('<div class="success-title">Order Placed Successfully!</div>', unsafe_allow_html=True)
    st.markdown('<div class="success-subtitle">Thank you for your order</div>', unsafe_allow_html=True)

    st.markdown(f'<div style="background:#0f0f0f;border-radius:12px;padding:20px;margin:24px 0;"><div style="font-size:0.9rem;color:#888;margin-bottom:8px;">Order ID</div><div style="font-size:1.5rem;font-weight:800;color:#00e676;">#{order_id}</div></div>', unsafe_allow_html=True)

    st.markdown(f'<div style="display:flex;gap:20px;justify-content:center;margin-bottom:24px;"><div style="text-align:center;"><div style="font-size:0.8rem;color:#888;">Total Amount</div><div style="font-size:1.2rem;font-weight:700;color:#e8e8e8;">{total}</div></div><div style="text-align:center;"><div style="font-size:0.8rem;color:#888;">Delivery By</div><div style="font-size:1.2rem;font-weight:700;color:#e8e8e8;">{delivery}</div></div></div>', unsafe_allow_html=True)

    st.markdown('<div style="background:#0d2818;border:1px solid #00e676;border-radius:8px;padding:12px;margin-bottom:24px;"><div style="font-size:0.85rem;color:#00e676;">💵 Cash on Delivery</div><div style="font-size:0.75rem;color:#888;margin-top:4px;">Pay when you receive your order</div></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📦 View Orders", type="primary", use_container_width=True):
            st.session_state["page"] = "Orders"
            st.rerun()
    with col2:
        if st.button("🛍️ Continue Shopping", use_container_width=True):
            st.session_state["page"] = "Home"
            st.rerun()
