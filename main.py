import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from backend.db import init_db, get_connection
from backend.services.user_service import add_user, get_all_users

# ── Bootstrap ────────────────────────────────────────────────────
init_db()
from backend.seed import seed_products, seed_admin_user
seed_admin_user()
seed_products()

# ── Page config ──────────────────────────────────────────────────
st.set_page_config(
    page_title="NexCart",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Dark Mode Global CSS ──────────────────────────────────────────
st.markdown("""
<style>
/* ── Base dark theme with animations ── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #0f0f0f !important;
    color: #e8e8e8 !important;
}
[data-testid="stHeader"] { background-color: #0f0f0f !important; }

/* ── Smooth transitions ── */
* {
    transition: all 0.2s ease;
}

/* ── Sidebar with gradient ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827 0%, #1a1a2e 100%) !important;
    border-right: 1px solid #2a2a3e !important;
}
[data-testid="stSidebar"] * { color: #e8e8e8 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stTextInput label { color: #aaa !important; }

/* ── All text inputs / selects with glow ── */
input, textarea, select,
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-baseweb="select"] {
    background-color: #1e1e2e !important;
    color: #e8e8e8 !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
}
input:focus, textarea:focus, select:focus {
    border-color: #00e676 !important;
    box-shadow: 0 0 0 2px rgba(0, 230, 118, 0.1) !important;
}
[data-baseweb="select"] * { color: #e8e8e8 !important; background-color: #1e1e2e !important; }

/* ── Buttons with hover effects ── */
.stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    transition: all 0.18s ease !important;
    border: none !important;
    padding: 8px 16px !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0, 230, 118, 0.25) !important;
}
/* Primary = green gradient */
.stButton > button[kind="primary"],
button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #00e676, #00c853) !important;
    color: #0f0f0f !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #00ff88, #00e676) !important;
}
/* Secondary = dark */
.stButton > button[kind="secondary"],
button[data-testid="baseButton-secondary"] {
    background-color: #1e1e2e !important;
    color: #e8e8e8 !important;
    border: 1px solid #333 !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: #00e676 !important;
}
/* Disabled */
.stButton > button:disabled {
    background-color: #2a2a2a !important;
    color: #555 !important;
    cursor: not-allowed !important;
    transform: none !important;
}

/* ── Expanders with animation ── */
[data-testid="stExpander"] {
    background-color: #1a1a2e !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
}
[data-testid="stExpander"]:hover {
    border-color: #00e676 !important;
}
[data-testid="stExpander"] summary { color: #e8e8e8 !important; }

/* ── Metrics ── */
[data-testid="stMetric"] {
    background-color: #1a1a2e !important;
    border-radius: 10px !important;
    padding: 14px !important;
    border: 1px solid #2a2a3e !important;
}
[data-testid="stMetricValue"] { color: #00e676 !important; }
[data-testid="stMetricLabel"] { color: #aaa !important; }

/* ── Tabs with active state ── */
[data-testid="stTabs"] [role="tab"] {
    color: #aaa !important;
    border-radius: 8px 8px 0 0 !important;
    padding: 12px 20px !important;
}
[data-testid="stTabs"] [role="tab"]:hover {
    color: #00e676 !important;
    background-color: rgba(0, 230, 118, 0.05) !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #00e676 !important;
    border-bottom: 3px solid #00e676 !important;
    background-color: #1a1a2e !important;
}

/* ── Forms ── */
[data-testid="stForm"] {
    background-color: #1a1a2e !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

/* ── Alerts with icons ── */
[data-testid="stAlert"] { border-radius: 8px !important; }
.stSuccess { background-color: #0d2818 !important; color: #00e676 !important; border-left: 4px solid #00e676 !important; }
.stError   { background-color: #2d0a0a !important; color: #ff5252 !important; border-left: 4px solid #ff5252 !important; }
.stWarning { background-color: #2d1f00 !important; color: #ffab40 !important; border-left: 4px solid #ffab40 !important; }
.stInfo    { background-color: #0a1a2d !important; color: #40c4ff !important; border-left: 4px solid #40c4ff !important; }

/* ── Dividers ── */
hr { border-color: #2a2a3e !important; margin: 12px 0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0f0f0f; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #00c853; }

/* ── Number input ── */
[data-testid="stNumberInput"] button {
    background-color: #2a2a3e !important;
    color: #e8e8e8 !important;
    border: none !important;
}
[data-testid="stNumberInput"] button:hover {
    background-color: #00e676 !important;
    color: #0f0f0f !important;
}

/* ── Dataframe styling ── */
[data-testid="stDataFrame"] {
    border-radius: 8px !important;
    overflow: hidden !important;
}

/* ── Loading animation ── */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
.stSpinner > div {
    border-color: #00e676 !important;
    animation: pulse 1.5s ease-in-out infinite;
}
</style>
""", unsafe_allow_html=True)

# ── Session state defaults ────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state["page"] = "Home"
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "user_name" not in st.session_state:
    st.session_state["user_name"] = None

# ── Sidebar ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 8px 0 16px;">
        <div style="font-size:2rem;">🛒</div>
        <div style="font-size:1.4rem; font-weight:800; color:#00e676; letter-spacing:1px;">NexCart</div>
        <div style="font-size:0.75rem; color:#888; margin-top:2px;">Smart Shopping, Simplified</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr style="border-color:#2a2a3e;">', unsafe_allow_html=True)

    # User selector / registration
    st.markdown('<div style="font-size:0.8rem; color:#888; margin-bottom:6px;">👤 ACCOUNT</div>', unsafe_allow_html=True)
    users = get_all_users()

    if users:
        user_options = {f"{u['name']} ({u['email']})": u["user_id"] for u in users}
        user_options["➕ Register new user"] = None
        current_idx = 0
        if st.session_state["user_id"]:
            for i, u in enumerate(users):
                if u["user_id"] == st.session_state["user_id"]:
                    current_idx = i
                    break
        selected_label = st.selectbox("User", list(user_options.keys()), index=current_idx, label_visibility="collapsed")
        selected_id = user_options[selected_label]
        if selected_id is not None:
            st.session_state["user_id"] = selected_id
            st.session_state["user_name"] = selected_label.split(" (")[0]
    else:
        selected_id = None

    if selected_id is None:
        with st.form("register_form", clear_on_submit=True):
            reg_name = st.text_input("Name", placeholder="Your full name")
            reg_email = st.text_input("Email", placeholder="you@email.com")
            if st.form_submit_button("Register", use_container_width=True, type="primary"):
                try:
                    uid = add_user({"name": reg_name, "email": reg_email})
                    st.session_state["user_id"] = uid
                    st.session_state["user_name"] = reg_name
                    st.success(f"Welcome, {reg_name}!")
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

    if st.session_state.get("user_name"):
        st.markdown(f'<div style="background:#0d2818;border-radius:8px;padding:8px 12px;color:#00e676;font-size:0.85rem;margin-top:6px;">👋 Hi, <b>{st.session_state["user_name"]}</b>!</div>', unsafe_allow_html=True)

    st.markdown('<hr style="border-color:#2a2a3e; margin:16px 0;">', unsafe_allow_html=True)

    # Navigation
    st.markdown('<div style="font-size:0.8rem; color:#888; margin-bottom:8px;">🗺️ NAVIGATION</div>', unsafe_allow_html=True)
    
    # Get current user role
    current_user_role = None
    if st.session_state.get("user_id"):
        conn = get_connection()
        try:
            user_row = conn.execute("SELECT role FROM users WHERE user_id = ?", (st.session_state["user_id"],)).fetchone()
            if user_row:
                current_user_role = user_row[0]
        finally:
            conn.close()
    
    # Build navigation items based on role
    nav_items = [("🏠", "Home"), ("🛒", "Cart"), ("📦", "Orders")]
    if current_user_role == "admin":
        nav_items.append(("🧑‍💼", "Admin"))
    
    for icon, page in nav_items:
        is_active = st.session_state["page"] == page
        btn_type = "primary" if is_active else "secondary"
        if st.button(f"{icon}  {page}", use_container_width=True, type=btn_type, key=f"nav_{page}"):
            st.session_state["page"] = page
            st.rerun()

    st.markdown('<hr style="border-color:#2a2a3e; margin:16px 0;">', unsafe_allow_html=True)

# ── Page routing ──────────────────────────────────────────────────
page = st.session_state["page"]

if page == "Home":
    from ui.home import render
    render()
elif page == "Cart":
    from ui.cart import render
    render()
elif page == "Orders":
    from ui.orders import render
    render()
elif page == "Order Success":
    from ui.orders import render_success
    render_success()
elif page == "Admin":
    from ui.admin import render
    render()
else:
    st.session_state["page"] = "Home"
    st.rerun()
