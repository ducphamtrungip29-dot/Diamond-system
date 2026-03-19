import streamlit as st
import datetime
import random
import json
import os

st.set_page_config(layout="wide")

# ===== STYLE LUXURY =====
st.markdown("""
<style>
body {background:#0b0f1a;}
h1 {text-align:center;color:#f5d27a;font-size:22px;}
.stTabs [role="tab"] {font-size:13px;padding:8px;}
.card {
background:#111827;
padding:12px;
border-radius:14px;
margin-bottom:12px;
border:1px solid rgba(245,210,122,0.2);
font-size:14px;
}
.stButton>button {
width:100%;
height:45px;
border-radius:12px;
font-size:16px;
background:linear-gradient(135deg,#f5d27a,#c9a44c);
color:black;
font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

st.title("💎 Diamond System FINAL")

# ===== DANH SÁCH TÀI KHOẢN =====
accounts = [
"Trần Linh Diamond",
"Trần Linh Jewellery",
"Trần Linh Kim Cương",
"Trần Linh",
"Diamond Linh",
"Fanpage",
"Zalo",
"TikTok"
]

# ===== LOAD SAFE =====
def load_data():
    try:
        if os.path.exists("data.json"):
            with open("data.json","r",encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
    except:
        pass
    return {"data":{}, "customers":[]}

saved = load_data()

# ===== INIT STATE =====
if "data" not in st.session_state:
    st.session_state.data = saved.get("data", {})
    if not isinstance(st.session_state.data, dict):
        st.session_state.data = {}

if "customers" not in st.session_state:
    st.session_state.customers = saved.get("customers", [])
    if not isinstance(st.session_state.customers, list):
        st.session_state.customers = []

# đảm bảo đủ account
for acc in accounts:
    st.session_state.data.setdefault(acc, [])

# ===== SAVE SAFE =====
def save():
    try:
        with open("data.json","w",encoding="utf-8") as f:
            json.dump({
                "data": st.session_state.data,
                "customers": st.session_state.customers
            }, f, ensure_ascii=False)
    except:
        pass

# ===== DATA AUTO =====
content_pool = ["Nhẫn kim cương","Dây chuyền cao cấp","Trang sức sang trọng","Mẫu mới về","Thiết kế độc quyền"]
time_slots = ["09:00","12:00","19:30","21:00"]

def auto_generate():
    today = datetime.date.today()
    for i in range(7):
        d = str(today + datetime.timedelta(days=i))
        for acc in accounts:
            st.session_state.data[acc].append({
                "date": d,
                "time": random.choice(time_slots),
                "content": random.choice(content_pool),
                "caption": "Inbox để xem chi tiết 💎"
            })
    save()

# ===== UI TABS =====
tabs = st.tabs(accounts + ["🚀 Auto","💬 Comment","💰 CRM","💾 Backup"])

# ===== HIỂN THỊ LỊCH =====
for i, acc in enumerate(accounts):
    with tabs[i]:
        st.subheader(acc)

        for idx, item in enumerate(st.session_state.data.get(acc, [])):
            st.markdown(f"""
            <div class="card">
            📅 {item.get('date','')} • {item.get('time','')}<br><br>
            {item.get('content','')}<br><br>
            <i>{item.get('caption','')}</i>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"✨ Gợi ý lại {idx}", key=f"{acc}{idx}"):
                item["caption"] = item["content"] + "\n\nInbox ngay để nhận tư vấn 💎"
                save()
                st.rerun()

# ===== AUTO =====
with tabs[len(accounts)]:
    if st.button("🔥 Tạo lịch 7 ngày"):
        auto_generate()
        st.success("Đã tạo lịch tự động")

# ===== COMMENT TOOL =====
with tabs[len(accounts)+1]:
    cmt = st.text_area("Nhập comment khách")
    if st.button("Gợi ý trả lời"):
        st.success("Dạ anh/chị inbox để em tư vấn chi tiết hơn 💎")

# ===== CRM =====
with tabs[len(accounts)+2]:
    name = st.text_input("Tên khách")
    if st.button("Thêm khách"):
        if name:
            st.session_state.customers.append({"name": name})
            save()

    st.subheader("Danh sách khách")
    for c in st.session_state.customers:
        st.write("👤", c.get("name",""))

# ===== BACKUP =====
with tabs[len(accounts)+3]:

    if st.button("Xuất dữ liệu"):
        data = json.dumps({
            "data": st.session_state.data,
            "customers": st.session_state.customers
        }, ensure_ascii=False)

        st.download_button("Tải file", data, "backup.json")

    up = st.file_uploader("Nhập dữ liệu", type="json")
    if up:
        try:
            content = json.load(up)
            st.session_state.data = content.get("data", {})
            st.session_state.customers = content.get("customers", [])
            save()
            st.success("Đã nhập dữ liệu")
        except:
            st.error("File lỗi")
