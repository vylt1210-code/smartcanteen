
import streamlit as st
from pathlib import Path
from datetime import datetime
import uuid
import qrcode
from io import BytesIO

# ============================================================
# UTH SMART CANTEEN
# Full interactive prototype based on the supplied concept:
# - redesigned UTH-style home
# - smart ordering
# - smart grocery
# - QR / cashless payment prototype
# - order status
# - feedback + anonymous feedback
# - loyalty points + vouchers
# - personalization / recommendations
# - scheduled pickup
# - student profile
# - canteen management dashboard
# ============================================================

st.set_page_config(
    page_title="UTH Smart Canteen",
    page_icon="🍱",
    layout="centered",
    initial_sidebar_state="collapsed",
)

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"

# -----------------------------
# Theme / CSS
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');

:root{
    --uth:#176f70;
    --uth-dark:#0d4f51;
    --uth-light:#e6f4f3;
    --yellow:#fedd1f;
    --navy:#05256e;
    --pink:#f56f8b;
    --text:#173b3d;
    --muted:#899899;
    --bg:#f4f8f8;
    --card:#ffffff;
}
html, body, [class*="css"] {
    font-family:'Be Vietnam Pro', sans-serif !important;
}
.stApp { background:var(--bg); }
.block-container{
    max-width:480px;
    padding:12px 10px 92px !important;
}
#MainMenu, footer, header { visibility:hidden; }

div[data-testid="stVerticalBlock"] > div { gap: 0.35rem; }
div[data-testid="stHorizontalBlock"] { gap: 7px; }

h1,h2,h3,h4,p { font-family:'Be Vietnam Pro', sans-serif !important; }

.stButton > button{
    border-radius:12px !important;
    min-height:38px !important;
    font-weight:700 !important;
    border:1px solid #dbe9e8 !important;
}
.stButton > button[kind="primary"]{
    background:var(--uth) !important;
    color:#fff !important;
    border-color:var(--uth) !important;
}
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"]{
    border-radius:12px !important;
}
[data-testid="stMetric"]{
    background:#fff;
    border:1px solid #e8eeee;
    border-radius:14px;
    padding:10px;
}

/* Header */
.topbar{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin:2px 2px 12px;
}
.profile-head{display:flex;align-items:center;gap:9px;}
.avatar{
    width:43px;height:43px;border-radius:50%;
    display:flex;align-items:center;justify-content:center;
    background:#e1eeee;font-size:23px;
}
.hello{font-size:16px;font-weight:800;color:var(--text);}
.mssv{font-size:9px;color:var(--muted);margin-top:2px;}
.qr-head{
    background:#fff;border-radius:12px;padding:8px 10px;
    font-size:10px;font-weight:700;box-shadow:0 2px 10px rgba(0,0,0,.05);
}

/* Hero */
.hero{
    border-radius:17px;
    background:linear-gradient(135deg,#0c6465,#178983);
    color:#fff;
    min-height:148px;
    padding:18px;
    position:relative;
    overflow:hidden;
    box-shadow:0 5px 18px rgba(23,111,112,.15);
}
.hero-logo{font-size:11px;font-weight:800;letter-spacing:.5px;}
.hero-title{font-size:23px;font-weight:800;line-height:1.15;margin:9px 0 11px;}
.hero-pill{
    display:inline-block;background:var(--yellow);color:#174e50;
    padding:6px 11px;border-radius:20px;font-size:10px;font-weight:800;
}
.hero-art{
    position:absolute;right:-2px;bottom:-22px;font-size:96px;
    transform:rotate(-5deg);
}

/* Cards */
.card{
    background:#fff;border-radius:15px;padding:13px;
    box-shadow:0 2px 11px rgba(20,55,55,.045);
    margin-bottom:10px;
}
.section{
    display:flex;justify-content:space-between;align-items:center;
    margin:14px 2px 8px;
}
.section h3{margin:0;color:var(--text);font-size:15px;font-weight:800;}
.section span{color:#278982;font-size:10px;font-weight:700;}

.quick{
    background:#fff;border-radius:15px;padding:12px 4px;
    display:grid;grid-template-columns:repeat(4,1fr);
    box-shadow:0 2px 11px rgba(20,55,55,.045);
    margin:12px 0;
}
.quick-item{text-align:center;font-size:10px;font-weight:700;color:#294849;}
.quick-icon{font-size:24px;margin-bottom:4px;}
.quick-sub{font-size:8px;color:#99a5a6;font-weight:400;}

.cat{
    background:#fff;border-radius:13px;padding:6px 3px;text-align:center;
    min-height:96px;box-shadow:0 1px 8px rgba(0,0,0,.035);
}
.cat-img{
    height:53px;border-radius:10px;background:#eef6f5;
    display:flex;align-items:center;justify-content:center;font-size:29px;
}
.cat-name{font-size:9px;font-weight:800;color:#294849;margin-top:5px;}
.cat-sub{font-size:7px;color:#9aa7a8;margin-top:2px;}

.preorder{
    background:#e3f2f2;border-radius:15px;padding:12px;
    display:flex;align-items:center;justify-content:space-between;
    margin:12px 0;
}
.pre-title{font-size:13px;font-weight:800;color:#234748;}
.pre-sub{font-size:8px;color:#788889;line-height:1.4;margin-top:4px;}
.clock{font-size:42px;color:var(--uth);}
.mini-btn{
    background:var(--uth);color:#fff;border-radius:18px;padding:7px 10px;
    font-size:9px;font-weight:800;
}

.reward{
    background:#fff;border-radius:15px;padding:10px;
    display:grid;grid-template-columns:1fr 1fr;margin-bottom:10px;
    box-shadow:0 2px 10px rgba(0,0,0,.04);
}
.reward-cell{display:flex;align-items:center;gap:8px;padding:3px 7px;}
.reward-cell + .reward-cell{border-left:1px solid #edf0f0;}
.reward-icon{
    width:35px;height:35px;border-radius:50%;display:flex;align-items:center;
    justify-content:center;background:#e4f4f2;font-size:17px;
}
.reward-label{font-size:9px;color:#738384;}
.reward-value{font-size:11px;color:#274647;font-weight:800;margin-top:2px;}

.food{
    background:#fff;border-radius:13px;overflow:hidden;
    box-shadow:0 2px 9px rgba(0,0,0,.045);
}
.food-img{
    height:110px;background:linear-gradient(135deg,#eef4ef,#dfece6);
    display:flex;align-items:center;justify-content:center;overflow:hidden;
}
.food-img img{width:100%;height:100%;object-fit:cover;}
.food-emoji{font-size:60px;}
.food-body{padding:7px 8px 9px;}
.food-name{font-size:9px;font-weight:800;color:#294849;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.food-price{font-size:10px;font-weight:700;color:#173f40;margin-top:6px;}
.add-dot{
    float:right;background:#16857e;color:white;width:19px;height:19px;
    border-radius:50%;display:flex;align-items:center;justify-content:center;
    font-size:14px;margin-top:-2px;
}

/* Product list */
.list-card{
    background:#fff;border-radius:14px;padding:10px;margin-bottom:8px;
    display:flex;align-items:center;gap:10px;
}
.list-icon{
    width:57px;height:57px;border-radius:12px;background:#edf5f4;
    display:flex;align-items:center;justify-content:center;font-size:31px;overflow:hidden;
}
.list-icon img{width:100%;height:100%;object-fit:cover;}
.list-main{flex:1;}
.list-name{font-size:11px;font-weight:800;color:#284849;}
.list-meta{font-size:9px;color:#8b999a;margin-top:3px;}
.list-price{font-size:11px;font-weight:800;color:var(--uth);margin-top:4px;}

.page-title{
    font-size:22px;font-weight:800;color:var(--text);margin:4px 0 12px;
}
.small-muted{font-size:9px;color:#8a999a;}
.badge{
    display:inline-block;padding:4px 8px;border-radius:15px;
    background:#e4f4f2;color:#147770;font-size:9px;font-weight:800;
}
.badge-yellow{background:#fff4bd;color:#765d00;}
.badge-pink{background:#ffe6ec;color:#a93d59;}

.timeline{
    display:flex;justify-content:space-between;gap:3px;margin:18px 0;
}
.step{text-align:center;flex:1;font-size:8px;color:#9aa7a8;}
.step-dot{
    width:28px;height:28px;border-radius:50%;background:#e8efef;
    margin:0 auto 5px;display:flex;align-items:center;justify-content:center;
}
.step.done{color:var(--uth);font-weight:800;}
.step.done .step-dot{background:#dff1ef;color:var(--uth);}

.bottom{
    display:none;
}
div[data-testid="stHorizontalBlock"]:has(button[key^="bn_"]) {
    position:fixed;bottom:0;left:50%;transform:translateX(-50%);
    width:min(480px,100%);background:rgba(255,255,255,.98);
    border-top:1px solid #e6eeee;padding:6px 4px 7px;z-index:1000;
}
.nav-label{text-align:center;color:#9aa6a7;font-size:8px;font-weight:600;}
.nav-label.active{color:var(--uth);font-weight:800;}
.nav-icon{font-size:20px;line-height:21px;margin-bottom:1px;}
.nav-badge{background:#ee4e57;color:white;border-radius:10px;padding:1px 4px;font-size:7px;position:absolute;margin-left:-5px;margin-top:-2px;}

/* Admin */
.admin-head{
    background:linear-gradient(135deg,#05256e,#176f70);
    color:#fff;border-radius:17px;padding:16px;margin-bottom:12px;
}
.admin-title{font-size:20px;font-weight:800;}
.admin-sub{font-size:9px;opacity:.8;margin-top:3px;}
.table-row{
    display:flex;justify-content:space-between;padding:9px 0;
    border-bottom:1px solid #edf1f1;font-size:10px;
}
.table-row:last-child{border-bottom:none;}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Data
# -----------------------------
FOODS = [
    dict(id="F01", name="Cơm gà xối mỡ", price=25000, category="Thức ăn",
         desc="Cơm nóng, gà chiên giòn, rau củ.", emoji="🍗", asset="com_ga.jpg", stock=32),
    dict(id="F02", name="Phở bò", price=30000, category="Thức ăn",
         desc="Phở bò truyền thống, nước dùng đậm vị.", emoji="🍜", asset="pho_bo.jpg", stock=24),
    dict(id="F03", name="Mì xào hải sản", price=28000, category="Thức ăn",
         desc="Mì xào cùng hải sản và rau củ.", emoji="🍝", asset="mi_xao.jpg", stock=18),
    dict(id="F04", name="Trà sữa trân châu", price=22000, category="Nước uống",
         desc="Trà sữa mát lạnh, trân châu.", emoji="🧋", asset="tra_sua.jpg", stock=45),
    dict(id="F05", name="Cơm sườn", price=30000, category="Thức ăn",
         desc="Cơm sườn nướng và rau ăn kèm.", emoji="🍱", asset="", stock=20),
    dict(id="F06", name="Bún thịt nướng", price=28000, category="Thức ăn",
         desc="Bún, thịt nướng, rau và nước mắm.", emoji="🥗", asset="", stock=17),
    dict(id="F07", name="Cà phê sữa", price=18000, category="Nước uống",
         desc="Cà phê sữa đá.", emoji="☕", asset="", stock=50),
    dict(id="F08", name="Nước suối", price=10000, category="Nước uống",
         desc="Nước suối đóng chai.", emoji="💧", asset="", stock=60),
]

GROCERIES = [
    dict(id="G01", name="Nước suối 500ml", price=10000, category="Nhu yếu phẩm", emoji="💧", stock=60),
    dict(id="G02", name="Snack", price=12000, category="Bánh snack", emoji="🍿", stock=35),
    dict(id="G03", name="Bút bi", price=5000, category="Dụng cụ học tập", emoji="🖊️", stock=80),
    dict(id="G04", name="Tập A4", price=18000, category="Dụng cụ học tập", emoji="📒", stock=42),
    dict(id="G05", name="Khăn giấy", price=10000, category="Vật dụng cá nhân", emoji="🧻", stock=25),
]

STATUSES = [
    ("Đã đặt", "✓"),
    ("Đang chuẩn bị", "👨‍🍳"),
    ("Sẵn sàng", "📦"),
    ("Hoàn tất", "✓"),
]

# -----------------------------
# Session state
# -----------------------------
defaults = {
    "page": "home",
    "cart": [],
    "orders": [],
    "points": 350,
    "vouchers": 3,
    "favorites": set(),
    "selected_product": None,
    "selected_order": None,
    "checkout_method": "QR thanh toán",
    "pickup": "Quầy Smart Canteen",
    "schedule": "Ngay khi có món",
    "role": "student",
    "notifications": [
        "🎁 Bạn có voucher mới từ Smart Canteen.",
        "📦 Đơn #UTH0001 đã sẵn sàng nhận.",
        "⭐ Đánh giá đơn hàng để nhận thêm điểm."
    ],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Seed demo order so tracking/dashboard has content
if not st.session_state.orders:
    st.session_state.orders = [{
        "id": "UTH0001",
        "items": [FOODS[1]],
        "total": FOODS[1]["price"],
        "status_index": 2,
        "status": "Sẵn sàng",
        "time": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "pickup": "Quầy Smart Canteen",
        "method": "QR thanh toán",
        "reviewed": False,
    }]

# -----------------------------
# Helpers
# -----------------------------
def money(n):
    return f"{n:,.0f}đ".replace(",", ".")

def find_item(item_id):
    for x in FOODS + GROCERIES:
        if x["id"] == item_id:
            return x
    return None

def img_for(item):
    if item.get("asset"):
        p = ASSETS / item["asset"]
        if p.exists():
            return str(p)
    return None

def go(page):
    st.session_state.page = page
    st.rerun()

def add_cart(item, qty=1):
    for row in st.session_state.cart:
        if row["id"] == item["id"]:
            row["qty"] += qty
            break
    else:
        st.session_state.cart.append({"id": item["id"], "qty": qty})
    st.toast(f"Đã thêm {item['name']} vào giỏ.", icon="🛒")

def cart_items():
    out = []
    for row in st.session_state.cart:
        item = find_item(row["id"])
        if item:
            out.append((item, row["qty"]))
    return out

def cart_total():
    return sum(item["price"] * qty for item, qty in cart_items())

def clear_cart():
    st.session_state.cart = []

def qr_png(text):
    qr = qrcode.QRCode(box_size=8, border=2)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image()
    bio = BytesIO()
    img.save(bio, format="PNG")
    return bio.getvalue()

def product_card(item, key_prefix=""):
    image = img_for(item)
    if image:
        media = f'<img src="data:image/jpeg;base64,{__import__("base64").b64encode(Path(image).read_bytes()).decode()}">'
    else:
        media = f'<div class="food-emoji">{item["emoji"]}</div>'
    st.markdown(f"""
    <div class="food">
      <div class="food-img">{media}</div>
      <div class="food-body">
        <div class="food-name">{item["name"]}</div>
        <div class="food-price">{money(item["price"])} <span class="add-dot">+</span></div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Thêm", key=f"{key_prefix}_{item['id']}", type="primary", use_container_width=True):
        add_cart(item)

def top_header():
    st.markdown("""
    <div class="topbar">
      <div class="profile-head">
        <div class="avatar">👨🏻</div>
        <div>
          <div class="hello">Chào, LÊ THÁI VỸ 👋</div>
          <div class="mssv">MSSV: 072204001210</div>
        </div>
      </div>
      <div class="qr-head">▦ &nbsp; Quét QR</div>
    </div>
    """, unsafe_allow_html=True)

def bottom_nav():
    page = st.session_state.page
    active = "home" if page == "home" else ("menu" if page in ["menu","product"] else ("cart" if page=="cart" else ("orders" if page in ["orders","tracking","review"] else "profile")))
    # Functional bottom navigation.
    cols = st.columns(5)
    nav_items = [
        (0, "⌂\nTrang chủ", "home"),
        (1, "🍽️\nĐặt món", "menu"),
        (2, f"🛒 {len(st.session_state.cart)}\nGiỏ hàng", "cart"),
        (3, "📋\nĐơn hàng", "orders"),
        (4, "●\nCá nhân", "profile"),
    ]
    for col, (_, label, target) in zip(cols, nav_items):
        with col:
            if st.button(label, key=f"bn_{target}", use_container_width=True):
                go(target)

# -----------------------------
# HOME
# -----------------------------
def home():
    top_header()
    st.markdown("""
    <div class="hero">
      <div class="hero-logo">◉ &nbsp; SMART CANTEEN</div>
      <div class="hero-title">Đặt món nhanh<br>– Nhận món lẹ</div>
      <div class="hero-pill">Không xếp hàng</div>
      <div class="hero-art">🍱</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🍱 Đặt món ngay", type="primary", use_container_width=True, key="hero_order"):
        go("menu")

    st.markdown('<div class="quick">', unsafe_allow_html=True)
    qcols = st.columns(4)
    quicks = [
        ("🍽️", "Đặt món", "Smart Canteen", "menu"),
        ("📋", "Đơn hàng", "Của tôi", "orders"),
        ("💳", "Thanh toán", "Trực tuyến", "cart"),
        ("🎁", "Ưu đãi", "Dành cho bạn", "loyalty"),
    ]
    for col, (icon, title, sub, target) in zip(qcols, quicks):
        with col:
            st.markdown(f'<div style="text-align:center;font-size:24px">{icon}</div><div style="text-align:center;font-size:10px;font-weight:800;color:#294849">{title}</div><div style="text-align:center;font-size:8px;color:#99a5a6">{sub}</div>', unsafe_allow_html=True)
            if st.button("Mở", key=f"quick_{target}", use_container_width=True):
                go(target)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section"><h3>Danh mục dịch vụ</h3><span>Xem tất cả</span></div>', unsafe_allow_html=True)
    cats = [
        ("🍱","Thức ăn","Đa dạng món"),
        ("🧋","Nước uống","Trà sữa, cafe..."),
        ("✏️","Văn phòng phẩm","Dụng cụ học tập"),
        ("🖨️","In ấn tài liệu","In nhanh, tiện lợi"),
    ]
    cols = st.columns(4)
    cat_targets = ["menu", "menu", "grocery", "grocery"]
    for col,(icon,name,sub),target in zip(cols,cats,cat_targets):
        with col:
            st.markdown(f'<div class="cat"><div class="cat-img">{icon}</div><div class="cat-name">{name}</div><div class="cat-sub">{sub}</div></div>', unsafe_allow_html=True)
            if st.button("Mở", key=f"cat_{name}", use_container_width=True):
                go(target)

    st.markdown("""
    <div class="preorder">
      <div><div class="pre-title">Đặt trước<br>theo giờ hẹn</div>
      <div class="pre-sub">Nhận món đúng giờ,<br>tiết kiệm thời gian</div></div>
      <div class="clock">◷</div><div class="mini-btn">Đặt ngay</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("⏰ Đặt trước theo giờ hẹn", type="primary", use_container_width=True, key="preorder_home"):
        go("schedule")
    if st.button("Chọn giờ nhận món", type="primary", use_container_width=True):
        go("schedule")

    st.markdown(f"""
    <div class="reward">
      <div class="reward-cell"><div class="reward-icon">★</div><div>
        <div class="reward-label">Tích điểm</div><div class="reward-value">{st.session_state.points} điểm</div>
      </div></div>
      <div class="reward-cell"><div class="reward-icon">🎟</div><div>
        <div class="reward-label">Voucher của bạn</div><div class="reward-value">{st.session_state.vouchers} voucher</div>
      </div></div>
    </div>
    """, unsafe_allow_html=True)
    rc1, rc2 = st.columns(2)
    with rc1:
        if st.button("Xem điểm", use_container_width=True, key="reward_points"):
            go("loyalty")
    with rc2:
        if st.button("Xem voucher", use_container_width=True, key="reward_voucher"):
            go("loyalty")

    st.markdown('<div class="section"><h3>Gợi ý cho bạn</h3><span>Cá nhân hóa</span></div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for col,item in zip(cols,FOODS[:4]):
        with col:
            product_card(item,"home")

    bottom_nav()

# -----------------------------
# MENU
# -----------------------------
def menu():
    st.markdown('<div class="page-title">🍽️ Đặt món</div>', unsafe_allow_html=True)
    q = st.text_input("Tìm kiếm", placeholder="Tìm món ăn, nước uống...", label_visibility="collapsed")
    category = st.selectbox("Danh mục", ["Tất cả","Thức ăn","Nước uống"])
    filtered = FOODS
    if category != "Tất cả":
        filtered = [x for x in filtered if x["category"] == category]
    if q:
        filtered = [x for x in filtered if q.lower() in x["name"].lower()]

    for item in filtered:
        image = img_for(item)
        if image:
            import base64
            media = f'<img src="data:image/jpeg;base64,{base64.b64encode(Path(image).read_bytes()).decode()}">'
        else:
            media = item["emoji"]
        st.markdown(f"""
        <div class="list-card">
          <div class="list-icon">{media}</div>
          <div class="list-main">
            <div class="list-name">{item["name"]}</div>
            <div class="list-meta">{item["category"]} · Còn {item["stock"]} phần</div>
            <div class="list-price">{money(item["price"])}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        c1,c2 = st.columns(2)
        with c1:
            if st.button("Xem chi tiết", key=f"detail_{item['id']}"): 
                st.session_state.selected_product=item["id"]; go("product")
        with c2:
            if st.button("＋ Thêm", key=f"addmenu_{item['id']}", type="primary"):
                add_cart(item)

    bottom_nav()

# -----------------------------
# PRODUCT DETAIL
# -----------------------------
def product_detail():
    item = find_item(st.session_state.selected_product)
    if not item:
        go("menu")
        return
    st.markdown('<div class="page-title">← Chi tiết món</div>', unsafe_allow_html=True)
    image = img_for(item)
    if image:
        st.image(image, use_container_width=True)
    else:
        st.markdown(f'<div class="card" style="text-align:center;font-size:90px">{item["emoji"]}</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card">
      <div style="font-size:20px;font-weight:800;color:#173b3d">{item["name"]}</div>
      <div style="font-size:18px;color:#147770;font-weight:800;margin-top:5px">{money(item["price"])}</div>
      <div class="small-muted" style="margin-top:8px">{item["desc"]}</div>
      <div style="margin-top:10px"><span class="badge">Còn {item["stock"]} phần</span></div>
    </div>
    """, unsafe_allow_html=True)
    qty = st.number_input("Số lượng", min_value=1, max_value=10, value=1)
    note = st.text_input("Ghi chú", placeholder="Ví dụ: ít đá, không hành...")
    if st.button("🛒 Thêm vào giỏ", type="primary", use_container_width=True):
        add_cart(item, int(qty))
        go("cart")
    if st.button("Đặt ngay", use_container_width=True):
        add_cart(item, int(qty))
        go("cart")
    bottom_nav()

# -----------------------------
# GROCERY
# -----------------------------
def grocery():
    st.markdown('<div class="page-title">🛍️ Bách hóa thông minh</div>', unsafe_allow_html=True)
    st.caption("Nhu yếu phẩm, bánh snack, dụng cụ học tập và vật dụng cá nhân.")
    q = st.text_input("Tìm sản phẩm", placeholder="Tìm nước uống, bút, tập...", label_visibility="collapsed")
    for item in GROCERIES:
        if q and q.lower() not in item["name"].lower():
            continue
        st.markdown(f"""
        <div class="list-card">
          <div class="list-icon">{item["emoji"]}</div>
          <div class="list-main">
            <div class="list-name">{item["name"]}</div>
            <div class="list-meta">{item["category"]} · Còn hàng: {item["stock"]}</div>
            <div class="list-price">{money(item["price"])}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Thêm vào giỏ", key=f"g_{item['id']}", type="primary", use_container_width=True):
            add_cart(item)
    bottom_nav()

# -----------------------------
# CART / CHECKOUT
# -----------------------------
def cart():
    st.markdown('<div class="page-title">🛒 Giỏ hàng</div>', unsafe_allow_html=True)
    rows = cart_items()
    if not rows:
        st.info("Giỏ hàng đang trống.")
        if st.button("Xem thực đơn", type="primary", use_container_width=True): go("menu")
        bottom_nav()
        return

    for item,qty in rows:
        st.markdown(f"""
        <div class="list-card">
          <div class="list-icon">{item["emoji"]}</div>
          <div class="list-main">
            <div class="list-name">{item["name"]}</div>
            <div class="list-meta">Số lượng: {qty}</div>
            <div class="list-price">{money(item["price"]*qty)}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        with c1:
            if st.button("−", key=f"minus_{item['id']}"):
                for row in st.session_state.cart:
                    if row["id"]==item["id"]:
                        row["qty"]=max(1,row["qty"]-1)
                st.rerun()
        with c2:
            st.markdown(f"<div style='text-align:center;padding-top:9px;font-weight:800'>{qty}</div>",unsafe_allow_html=True)
        with c3:
            if st.button("＋", key=f"plus_{item['id']}"):
                for row in st.session_state.cart:
                    if row["id"]==item["id"]:
                        row["qty"]+=1
                st.rerun()

    total=cart_total()
    st.markdown(f"""
    <div class="card">
      <div style="display:flex;justify-content:space-between"><span>Tạm tính</span><b>{money(total)}</b></div>
      <div style="display:flex;justify-content:space-between;margin-top:7px"><span>Phí dịch vụ</span><b>0đ</b></div>
      <hr>
      <div style="display:flex;justify-content:space-between;font-size:17px"><b>Tổng</b><b style="color:#147770">{money(total)}</b></div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("💳 Tiến hành thanh toán", type="primary", use_container_width=True):
        go("checkout")
    if st.button("🗑️ Xóa toàn bộ giỏ"):
        clear_cart(); st.rerun()
    bottom_nav()

def checkout():
    st.markdown('<div class="page-title">💳 Xác nhận & thanh toán</div>', unsafe_allow_html=True)
    if not cart_items():
        st.warning("Giỏ hàng đang trống.")
        go("menu")
        return
    total=cart_total()
    st.markdown(f"""
    <div class="card">
      <div style="font-weight:800">Tóm tắt đơn hàng</div>
      <div class="small-muted" style="margin-top:5px">{len(cart_items())} loại sản phẩm · {money(total)}</div>
    </div>
    """, unsafe_allow_html=True)

    st.session_state.checkout_method=st.radio(
        "Phương thức thanh toán",
        ["QR thanh toán","Ví điện tử","Tài khoản ngân hàng"],
        index=["QR thanh toán","Ví điện tử","Tài khoản ngân hàng"].index(st.session_state.checkout_method)
    )
    st.session_state.pickup=st.selectbox("Địa điểm nhận hàng", ["Quầy Smart Canteen","Quầy A","Quầy B"])
    st.session_state.schedule=st.selectbox("Thời gian nhận", ["Ngay khi có món","11:30","12:00","12:30","13:00"])
    voucher=st.checkbox(f"🎟 Dùng voucher ({st.session_state.vouchers} voucher)")
    if voucher and total>=20000:
        discount=min(5000,total)
    else:
        discount=0
    final=total-discount

    st.markdown(f"""
    <div class="card">
      <div style="display:flex;justify-content:space-between"><span>Tạm tính</span><b>{money(total)}</b></div>
      <div style="display:flex;justify-content:space-between;margin-top:6px"><span>Voucher</span><b>-{money(discount)}</b></div>
      <hr><div style="display:flex;justify-content:space-between;font-size:17px"><b>Thanh toán</b><b style="color:#147770">{money(final)}</b></div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Xác nhận đặt hàng", type="primary", use_container_width=True):
        order_id=f"UTH{len(st.session_state.orders)+1:04d}"
        order={
            "id":order_id,
            "items":[{"item":i,"qty":q} for i,q in cart_items()],
            "total":final,
            "status_index":0,
            "status":"Đã đặt",
            "time":datetime.now().strftime("%d/%m/%Y %H:%M"),
            "pickup":st.session_state.pickup,
            "method":st.session_state.checkout_method,
            "reviewed":False,
        }
        st.session_state.orders.insert(0,order)
        st.session_state.points += max(5,final//10000)
        if voucher: st.session_state.vouchers=max(0,st.session_state.vouchers-1)
        clear_cart()
        st.session_state.selected_order=order_id
        go("payment_success")

# -----------------------------
# PAYMENT SUCCESS
# -----------------------------
def payment_success():
    order=next((o for o in st.session_state.orders if o["id"]==st.session_state.selected_order),None)
    if not order:
        go("orders"); return
    st.markdown('<div class="page-title">✅ Đặt hàng thành công</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card" style="text-align:center">
      <div style="font-size:55px">🎉</div>
      <div style="font-size:18px;font-weight:800;color:#173b3d">Đơn #{order["id"]}</div>
      <div class="small-muted" style="margin-top:5px">Đã ghi nhận đơn hàng của bạn.</div>
      <div style="margin-top:10px"><span class="badge">{order["status"]}</span></div>
    </div>
    """, unsafe_allow_html=True)
    st.image(qr_png(f"UTH SMART CANTEEN|{order['id']}|{order['pickup']}"), width=180)
    st.caption(f"Mã QR nhận món · {order['pickup']}")
    if st.button("📦 Theo dõi đơn hàng", type="primary", use_container_width=True):
        go("tracking")
    if st.button("🏠 Về trang chủ", use_container_width=True): go("home")

# -----------------------------
# ORDERS / TRACKING
# -----------------------------
def orders():
    st.markdown('<div class="page-title">📋 Đơn hàng của tôi</div>', unsafe_allow_html=True)
    for order in st.session_state.orders:
        st.markdown(f"""
        <div class="card">
          <div style="display:flex;justify-content:space-between">
            <b>#{order["id"]}</b><span class="badge">{order["status"]}</span>
          </div>
          <div class="small-muted" style="margin-top:6px">{order["time"]} · {order["pickup"]}</div>
          <div style="font-size:11px;margin-top:8px">{len(order["items"])} loại sản phẩm · <b>{money(order["total"])}</b></div>
        </div>
        """, unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1:
            if st.button("Theo dõi",key=f"track_{order['id']}"):
                st.session_state.selected_order=order["id"];go("tracking")
        with c2:
            if st.button("Đánh giá",key=f"rev_{order['id']}"):
                st.session_state.selected_order=order["id"];go("review")
    bottom_nav()

def tracking():
    order=next((o for o in st.session_state.orders if o["id"]==st.session_state.selected_order),None)
    if not order:
        go("orders"); return
    st.markdown('<div class="page-title">📦 Theo dõi đơn hàng</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card">
      <div style="display:flex;justify-content:space-between"><b>#{order["id"]}</b><span class="badge">{order["status"]}</span></div>
      <div class="small-muted" style="margin-top:5px">Nhận tại: {order["pickup"]}</div>
    </div>
    """,unsafe_allow_html=True)

    idx=order["status_index"]
    st.markdown('<div class="timeline">'+''.join(
        f'<div class="step {"done" if i<=idx else ""}"><div class="step-dot">{icon if i<=idx else "○"}</div>{label}</div>'
        for i,(label,icon) in enumerate(STATUSES)
    )+'</div>',unsafe_allow_html=True)

    st.info("Quy trình: Đặt hàng & thanh toán → Tiếp nhận & chế biến → Thông báo nhận hàng → Nhận hàng & hoàn tất.")
    if idx<3 and st.button("▶ Mô phỏng chuyển trạng thái", type="primary", use_container_width=True):
        order["status_index"] += 1
        order["status"]=STATUSES[order["status_index"]][0]
        st.rerun()
    if idx>=2:
        st.image(qr_png(f"UTH|{order['id']}"),width=170)
        st.caption("Xuất trình mã QR tại quầy để nhận món.")
    if st.button("⭐ Đánh giá đơn hàng",use_container_width=True):
        go("review")
    bottom_nav()

# -----------------------------
# SCHEDULE / NOTIFICATIONS
# -----------------------------
def schedule():
    st.markdown('<div class="page-title">⏰ Đặt trước theo giờ hẹn</div>',unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
      <b>Nhận món đúng giờ</b>
      <div class="small-muted" style="margin-top:5px">Chọn khung giờ, địa điểm nhận và món cần đặt.</div>
    </div>
    """,unsafe_allow_html=True)
    st.selectbox("Khung giờ",["11:30","12:00","12:30","13:00"])
    st.selectbox("Địa điểm nhận",["Quầy Smart Canteen","Quầy A","Quầy B"])
    if st.button("Xác nhận giờ hẹn",type="primary",use_container_width=True):
        st.success("Đã lưu lịch nhận món cho prototype.")
    if st.button("Đặt món"):
        go("menu")
    bottom_nav()

def notifications():
    st.markdown('<div class="page-title">🔔 Thông báo</div>',unsafe_allow_html=True)
    for n in st.session_state.notifications:
        st.markdown(f'<div class="card">{n}<div class="small-muted" style="margin-top:5px">Smart Canteen</div></div>',unsafe_allow_html=True)
    bottom_nav()

# -----------------------------
# LOYALTY / VOUCHERS / REVIEW
# -----------------------------
def loyalty():
    st.markdown('<div class="page-title">★ Tích điểm & ưu đãi</div>',unsafe_allow_html=True)
    st.markdown(f"""
    <div class="admin-head" style="background:linear-gradient(135deg,#176f70,#2a9690)">
      <div class="admin-title">{st.session_state.points} điểm</div>
      <div class="admin-sub">Điểm tích lũy từ mua hàng và phản hồi.</div>
    </div>
    """,unsafe_allow_html=True)
    st.markdown('<div class="section"><h3>Voucher của bạn</h3></div>',unsafe_allow_html=True)
    vouchers=[("Giảm 5.000đ","Đơn từ 20.000đ"),("Nước miễn phí","Đổi 100 điểm"),("Combo sinh viên","Ưu đãi theo khung giờ")]
    for i,(title,sub) in enumerate(vouchers):
        st.markdown(f'<div class="card"><b>🎟 {title}</b><div class="small-muted" style="margin-top:4px">{sub}</div></div>',unsafe_allow_html=True)
        if st.button("Đổi voucher",key=f"redeem_{i}"):
            if st.session_state.points>=100:
                st.session_state.points-=100
                st.session_state.vouchers+=1
                st.success("Đã đổi voucher.")
            else: st.warning("Chưa đủ điểm.")
    bottom_nav()

def review():
    order=next((o for o in st.session_state.orders if o["id"]==st.session_state.selected_order),None)
    st.markdown('<div class="page-title">⭐ Đánh giá chất lượng dịch vụ</div>',unsafe_allow_html=True)
    if order:
        st.caption(f"Đánh giá đơn #{order['id']}")
    rating=st.slider("Mức độ hài lòng",1,5,5)
    st.markdown("**Bạn ấn tượng về điều gì?**")
    tags=st.multiselect("",["Hương vị","Độ tươi ngon","Kích cỡ khẩu phần","Bao bì đóng gói","Thực đơn đa dạng"],label_visibility="collapsed")
    comment=st.text_area("Nhận xét",placeholder="Chia sẻ trải nghiệm của bạn...")
    anonymous=st.checkbox("Góp ý ẩn danh")
    if st.button("Gửi đánh giá",type="primary",use_container_width=True):
        if order: order["reviewed"]=True
        st.session_state.points+=5
        st.success("Cảm ơn bạn! Bạn nhận được +5 điểm.")
        if anonymous:
            st.caption("Phản hồi được ghi nhận ở chế độ ẩn danh.")
    bottom_nav()

# -----------------------------
# PROFILE
# -----------------------------
def profile():
    st.markdown('<div class="page-title">👤 Cá nhân</div>',unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card" style="text-align:center">
      <div class="avatar" style="margin:auto;font-size:30px">👨🏻</div>
      <div style="font-size:18px;font-weight:800;margin-top:8px">LÊ THÁI VỸ</div>
      <div class="small-muted">Sinh viên UTH · MSSV 072204001210</div>
    </div>
    """,unsafe_allow_html=True)
    cols=st.columns(3)
    cols[0].metric("Điểm",st.session_state.points)
    cols[1].metric("Voucher",st.session_state.vouchers)
    cols[2].metric("Đơn hàng",len(st.session_state.orders))
    for label,page in [
        ("★ Tích điểm & voucher","loyalty"),
        ("🔔 Thông báo","notifications"),
        ("🛍️ Bách hóa thông minh","grocery"),
        ("⚙️ Quản lý Smart Canteen (Demo)","admin"),
    ]:
        if st.button(label,use_container_width=True):
            go(page)
    st.markdown('<div class="small-muted" style="margin-top:12px">Prototype học thuật / portfolio — chưa kết nối hệ thống UTH thật.</div>',unsafe_allow_html=True)
    bottom_nav()

# -----------------------------
# ADMIN DASHBOARD
# -----------------------------
def admin():
    st.markdown("""
    <div class="admin-head">
      <div class="admin-title">Smart Canteen · Quản lý</div>
      <div class="admin-sub">Bảng điều khiển vận hành prototype</div>
    </div>
    """,unsafe_allow_html=True)

    pending=sum(1 for o in st.session_state.orders if o["status_index"]<3)
    revenue=sum(o["total"] for o in st.session_state.orders)
    a,b=st.columns(2)
    a.metric("Đơn đang xử lý",pending)
    b.metric("Doanh thu demo",money(revenue))

    st.markdown('<div class="section"><h3>Quy trình vận hành</h3></div>',unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
      <div class="table-row"><b>01 · Đặt hàng & thanh toán</b><span>✓</span></div>
      <div class="table-row"><b>02 · Tiếp nhận & chế biến</b><span>🍳</span></div>
      <div class="table-row"><b>03 · Thông báo nhận hàng</b><span>🔔</span></div>
      <div class="table-row"><b>04 · Nhận hàng & hoàn tất</b><span>📦</span></div>
    </div>
    """,unsafe_allow_html=True)

    st.markdown('<div class="section"><h3>Đơn hàng gần đây</h3></div>',unsafe_allow_html=True)
    for order in st.session_state.orders[:6]:
        st.markdown(f"""
        <div class="card">
          <div style="display:flex;justify-content:space-between"><b>#{order["id"]}</b><span class="badge">{order["status"]}</span></div>
          <div class="small-muted">{order["time"]} · {money(order["total"])}</div>
        </div>
        """,unsafe_allow_html=True)
        if order["status_index"]<3:
            if st.button("Chuyển trạng thái",key=f"admin_next_{order['id']}",type="primary"):
                order["status_index"]+=1
                order["status"]=STATUSES[order["status_index"]][0]
                st.rerun()

    st.markdown('<div class="section"><h3>Tồn kho</h3></div>',unsafe_allow_html=True)
    for item in FOODS[:6]:
        st.markdown(f"""
        <div class="table-row">
          <span>{item["emoji"]} {item["name"]}</span>
          <b>{item["stock"]}</b>
        </div>
        """,unsafe_allow_html=True)

    if st.button("← Về giao diện sinh viên",use_container_width=True):
        go("home")

# -----------------------------
# Router
# -----------------------------
page=st.session_state.page
if page=="home": home()
elif page=="menu": menu()
elif page=="product": product_detail()
elif page=="grocery": grocery()
elif page=="cart": cart()
elif page=="checkout": checkout()
elif page=="payment_success": payment_success()
elif page=="orders": orders()
elif page=="tracking": tracking()
elif page=="schedule": schedule()
elif page=="notifications": notifications()
elif page=="loyalty": loyalty()
elif page=="review": review()
elif page=="profile": profile()
elif page=="admin": admin()
else: home()
