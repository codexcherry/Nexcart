import streamlit as st
from backend.services.product_service import get_products, record_view
from backend.services.cart_service import add_to_cart
from utils.helpers import format_currency

CATEGORIES = ["All","Electronics","Clothing","Books","Home & Kitchen","Sports","Beauty","Toys","Other"]
CAT_ICONS = {"All":"🏠","Electronics":"📱","Clothing":"👕","Books":"📚","Home & Kitchen":"🏠","Sports":"⚽","Beauty":"💄","Toys":"🧸","Other":"📦"}
SORT_OPTIONS = {"🔥 Popularity":"popularity_score","⭐ Rating":"rating","💰 Price: Low → High":"price","🔤 Name A–Z":"name"}


_CSS = """<style>
.page-hdr{background:linear-gradient(135deg,#1a1a2e,#16213e);border-radius:16px;padding:22px 28px;margin-bottom:18px;border:1px solid #2a2a3e}
.page-hdr h2{font-size:1.7rem;font-weight:800;color:#00e676;margin:0 0 4px}
.page-hdr p{font-size:.88rem;color:#888;margin:0}
.cat-nav{display:flex;gap:8px;overflow-x:auto;padding:4px 0 12px;scrollbar-width:none}
.cat-nav::-webkit-scrollbar{display:none}
.cat-pill{display:inline-flex;align-items:center;gap:5px;padding:7px 16px;border-radius:24px;font-size:.82rem;font-weight:600;white-space:nowrap;background:#1a1a2e;border:1px solid #2a2a3e;color:#aaa}
.srch-wrap{background:#1a1a2e;border:1px solid #2a2a3e;border-radius:14px;padding:14px 18px;margin-bottom:18px}
.sec-title{font-size:1.2rem;font-weight:800;color:#e8e8e8;margin:24px 0 16px;padding-left:12px;border-left:4px solid #00e676}
.nc-card{background:linear-gradient(135deg,#1a1a2e,#16213e);border:1px solid #2a2a3e;border-radius:14px;overflow:hidden;margin-bottom:20px;transition:transform .25s,box-shadow .25s,border-color .25s}
.nc-card:hover{transform:translateY(-5px);border-color:#00e676;box-shadow:0 10px 28px rgba(0,230,118,.2)}
.nc-img{position:relative;height:170px;overflow:hidden;background:#0f0f0f}
.nc-img img{width:100%;height:100%;object-fit:cover;transition:transform .35s}
.nc-card:hover .nc-img img{transform:scale(1.08)}
.nc-body{padding:13px}
.nc-name{font-size:.88rem;font-weight:700;color:#e8e8e8;line-height:1.35;min-height:36px;margin-bottom:5px}
.nc-cat{font-size:.72rem;color:#888;margin-bottom:5px}
.nc-stars{color:#ffa726;font-size:.8rem;margin-bottom:8px}
.nc-rev{color:#888;font-size:.72rem;margin-left:3px}
.nc-pr-row{display:flex;align-items:baseline;gap:6px;flex-wrap:wrap}
.nc-price{font-size:1.2rem;font-weight:900;color:#fff}
.nc-mrp{font-size:.78rem;color:#555;text-decoration:line-through}
.nc-disc{font-size:.68rem;font-weight:700;background:#0d2818;color:#00e676;padding:2px 6px;border-radius:4px}
.nc-ctrl{padding:10px 13px;background:#111827;border-top:1px solid #2a2a3e}
.empty{text-align:center;padding:70px 20px;color:#555}
.empty .ico{font-size:4.5rem;margin-bottom:14px;opacity:.4}
</style>"""


def _stars(r):
    return "⭐"*int(r)+"☆"*(5-int(r))

def render():
    st.markdown(_CSS, unsafe_allow_html=True)
    st.markdown("""<div class="page-hdr"><h2>🛒 NexCart</h2><p>India's smartest shopping — fast, fresh &amp; affordable</p></div>""", unsafe_allow_html=True)
    pills="".join(f'<div class="cat-pill">{CAT_ICONS.get(c,"📦")} {c}</div>' for c in CATEGORIES)
    st.markdown(f'<div class="cat-nav">{pills}</div>', unsafe_allow_html=True)
    st.markdown('<div class="srch-wrap">', unsafe_allow_html=True)
    c1,c2,c3=st.columns([4,2,2])
    with c1:
        search=st.text_input("🔍",placeholder="Search products, brands and more...",label_visibility="collapsed")
    with c2:
        cat_lbl=st.selectbox("Cat",CATEGORIES,label_visibility="collapsed")
        category=None if cat_lbl=="All" else cat_lbl
    with c3:
        srt_lbl=st.selectbox("Sort",list(SORT_OPTIONS.keys()),label_visibility="collapsed")
        sort_by=SORT_OPTIONS[srt_lbl]
    st.markdown('</div>', unsafe_allow_html=True)
    
    products=get_products(category=category,search=search or None,sort_by=sort_by)
    if not products:
        st.markdown('<div class="empty"><div class="ico">🔍</div><div style="font-size:1.1rem;font-weight:700;color:#e8e8e8">No Products Found</div></div>', unsafe_allow_html=True)
        return
    
    if not search and category is None:
        featured=sorted(products,key=lambda p:p.get("popularity_score",0),reverse=True)[:4]
        st.markdown('<div class="sec-title">🔥 Trending Right Now</div>', unsafe_allow_html=True)
        for col,p in zip(st.columns(4),featured):
            with col: _card(p,key_prefix="feat_")
        st.markdown('<div class="sec-title">🛍️ All Products</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="sec-title">🛍️ {len(products)} result(s)</div>', unsafe_allow_html=True)
    cols=st.columns(4)
    for idx,product in enumerate(products):
        with cols[idx%4]: _card(product,key_prefix="grid_")

def _card(product,key_prefix=""):
    pid=product["product_id"]; kid=f"{key_prefix}{pid}"
    mrp=round(product["price"]*1.2); disc=round(((mrp-product["price"])/mrp)*100)
    img=product.get("image_url") or "https://placehold.co/400x300/1a1a2e/888?text=No+Image"
    revs=product.get("num_reviews",0)
    
    st.markdown(f"""<div class="nc-card"><div class="nc-img"><img src="{img}" alt="{product['name']}" /></div><div class="nc-body"><div class="nc-name">{product['name']}</div><div class="nc-cat">📂 {product.get('category','')}</div><div class="nc-stars">{_stars(product.get('rating',0))} <span class="nc-rev">({revs:,})</span></div><div class="nc-pr-row"><span class="nc-price">{format_currency(product['price'])}</span><span class="nc-mrp">{format_currency(mrp)}</span><span class="nc-disc">{disc}% OFF</span></div></div><div class="nc-ctrl">""", unsafe_allow_html=True)
    if product["stock"]>0:
        qc,bc=st.columns([1,2])
        with qc:
            qty=st.number_input("Qty",min_value=1,max_value=product["stock"],value=1,key=f"qty_{kid}",label_visibility="collapsed")
        with bc:
            if st.button("🛒 Add",key=f"add_{kid}",use_container_width=True,type="primary"):
                uid=st.session_state.get("user_id")
                if not uid: st.warning("👤 Select a user first")
                else:
                    try:
                        record_view(pid); res=add_to_cart(uid,pid,qty)
                        if res["success"]: st.success("✅ Added!")
                        else: st.warning(res["message"])
                    except ValueError as e: st.error(str(e))
    else:
        st.button("❌ Out of Stock",disabled=True,use_container_width=True,key=f"oos_{kid}")
    st.markdown("</div></div>", unsafe_allow_html=True)
