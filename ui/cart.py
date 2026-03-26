import streamlit as st
from backend.services.cart_service import get_cart, update_cart, remove_from_cart
from backend.services.order_service import place_order
from utils.helpers import format_currency

_CSS = """
<style>
.cart-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border-radius: 16px;
    padding: 24px 32px;
    margin-bottom: 24px;
    border: 1px solid #2a2a3e;
}
.cart-title {
    font-size: 1.8rem;
    font-weight: 800;
    color: #00e676;
    margin-bottom: 4px;
}
.cart-subtitle {
    font-size: 0.9rem;
    color: #888;
}
.cart-item {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 1px solid #2a2a3e;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 12px;
    transition: all 0.3s ease;
}
.cart-item:hover {
    border-color: #00e676;
    transform: translateX(4px);
}
.item-image {
    width: 100px;
    height: 100px;
    object-fit: cover;
    border-radius: 8px;
    background: #0f0f0f;
}
.item-name {
    font-size: 1.1rem;
    font-weight: 700;
    color: #e8e8e8;
    margin-bottom: 4px;
}
.item-price {
    font-size: 1.3rem;
    font-weight: 800;
    color: #fff;
}
.item-category {
    font-size: 0.8rem;
    color: #888;
    margin-top: 4px;
}
.summary-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%);
    border: 2px solid #00e676;
    border-radius: 16px;
    padding: 24px;
}
.summary-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #e8e8e8;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid #2a2a3e;
}
.summary-row {
    display: flex;
    justify-content: space-between;
    padding: 8px 0;
    color: #aaa;
    font-size: 0.95rem;
}
.summary-total {
    display: flex;
    justify-content: space-between;
    padding: 16px 0;
    margin-top: 12px;
    border-top: 2px solid #2a2a3e;
    font-size: 1.4rem;
    font-weight: 800;
    color: #fff;
}
.empty-cart {
    text-align: center;
    padding: 80px 20px;
}
.empty-icon {
    font-size: 5rem;
    margin-bottom: 20px;
    opacity: 0.5;
}
.badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    background: #0d2818;
    color: #00e676;
}
</style>
"""


def render():
    st.markdown(_CSS, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="cart-header">
        <div class="cart-title">🛒 Shopping Cart</div>
        <div class="cart-subtitle">Review your items and proceed to checkout</div>
    </div>
    """, unsafe_allow_html=True)
    
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.markdown("""
        <div class="empty-cart">
            <div class="empty-icon">👤</div>
            <div style="font-size:1.3rem; font-weight:700; color:#e8e8e8; margin-bottom:12px;">Please Login</div>
            <div style="color:#888; margin-bottom:24px;">Select or register a user to view your cart</div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    cart_data = get_cart(user_id)
    
    if not cart_data or not cart_data.get("items"):
        st.markdown("""
        <div class="empty-cart">
            <div class="empty-icon">🛒</div>
            <div style="font-size:1.3rem; font-weight:700; color:#e8e8e8; margin-bottom:12px;">Your Cart is Empty</div>
            <div style="color:#888; margin-bottom:24px;">Add some products to get started!</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🛍️ Start Shopping", type="primary", use_container_width=True):
            st.session_state["page"] = "Home"
            st.rerun()
        return
    
    items = cart_data["items"]
    subtotal = cart_data["subtotal"]
    
    # Layout: Cart Items + Summary
    col_items, col_summary = st.columns([2, 1])
    
    with col_items:
        st.markdown(f'<div style="color:#888; font-size:0.9rem; margin-bottom:16px;">🛍️ {len(items)} item(s) in cart</div>', unsafe_allow_html=True)
        
        for item in items:
            # Cart Item Card
            st.markdown(f"""
            <div class="cart-item">
                <div style="display:flex; gap:20px; align-items:center;">
                    <img src="{item.get('image_url', 'https://via.placeholder.com/100')}" class="item-image" />
                    <div style="flex:1;">
                        <div class="item-name">{item['name']}</div>
                        <div class="item-category">📂 {item.get('category', 'Uncategorized')}</div>
                        <div class="item-price">{format_currency(item['price'])}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Quantity Controls
            qty_col, price_col, remove_col = st.columns([2, 2, 1])
            
            with qty_col:
                new_qty = st.number_input(
                    "Quantity",
                    min_value=1,
                    max_value=item["stock"],
                    value=item["quantity"],
                    key=f"qty_{item['product_id']}",
                    label_visibility="collapsed"
                )
                if new_qty != item["quantity"]:
                    try:
                        update_cart(item["cart_id"], new_qty)
                        st.rerun()
                    except ValueError as e:
                        st.error(str(e))
            
            with price_col:
                line_total = item["price"] * item["quantity"]
                st.markdown(f'<div style="padding:8px 0; color:#aaa;">Subtotal: <span style="color:#fff; font-weight:700;">{format_currency(line_total)}</span></div>', unsafe_allow_html=True)
            
            with remove_col:
                if st.button("🗑️", key=f"remove_{item['product_id']}", help="Remove item"):
                    remove_from_cart(item["cart_id"])
                    st.rerun()
            
            st.markdown('<hr style="border-color:#2a2a3e; margin:12px 0;">', unsafe_allow_html=True)
    
    with col_summary:
        # Order Summary
        st.markdown("""
        <div class="summary-card">
            <div class="summary-title">💳 Order Summary</div>
        """, unsafe_allow_html=True)
        
        # Calculate totals
        delivery_fee = 0 if subtotal >= 499 else 40
        tax = round(subtotal * 0.18, 2)  # 18% GST
        total = subtotal + delivery_fee + tax
        
        st.markdown(f"""
            <div class="summary-row">
                <span>Subtotal ({len(items)} items)</span>
                <span>{format_currency(subtotal)}</span>
            </div>
            <div class="summary-row">
                <span>Delivery Fee</span>
                <span>{'FREE' if delivery_fee == 0 else format_currency(delivery_fee)}</span>
            </div>
            <div class="summary-row">
                <span>GST (18%)</span>
                <span>{format_currency(tax)}</span>
            </div>
            <div class="summary-total">
                <span>Total</span>
                <span>{format_currency(total)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div style="margin-top:20px;">', unsafe_allow_html=True)
        
        # Delivery Info
        if delivery_fee == 0:
            st.success("🎉 Free delivery applied!")
        else:
            remaining = 499 - subtotal
            st.info(f"💡 Add {format_currency(remaining)} more for free delivery")
        
        # Checkout Button
        if st.button("🚀 Proceed to Checkout", type="primary", use_container_width=True):
            try:
                result = place_order(user_id)
                st.session_state["last_order"] = result
                st.session_state["page"] = "Order Success"
                st.rerun()
            except ValueError as e:
                st.error(f"❌ {str(e)}")
        
        # Continue Shopping
        if st.button("🛍️ Continue Shopping", use_container_width=True):
            st.session_state["page"] = "Home"
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Payment Info
        st.markdown("""
        <div style="margin-top:24px; padding:16px; background:#0d2818; border:1px solid #00e676; border-radius:8px;">
            <div style="font-size:0.85rem; color:#00e676; font-weight:700; margin-bottom:8px;">💵 Cash on Delivery</div>
            <div style="font-size:0.75rem; color:#888;">Pay when you receive your order</div>
        </div>
        """, unsafe_allow_html=True)
