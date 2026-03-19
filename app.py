import streamlit as st
import datetime
import random
import json
import os

st.set_page_config(layout="wide")

# ===== UI =====
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

st.title("💎 Diamond System")

# ===== LOAD DATA =====
if os.path.exists("data.json"):
    with open("data.json","r") as f:
        saved = json.load(f)
else:
    saved = {"data":{}, "customers":[]}

accounts = [
"Trần Linh Diamond","Trần Linh Jewellery","Trần Linh Kim Cương",
"Trần Linh","Diamond Linh","Fanpage","Zalo","TikTok"
]

if "data" not in st.session_state:
    if isinstance(saved, dict):
        st.session_state.data = saved.get("data",{acc:[] for acc in accounts})
    else:
        st.session_state.data = {acc:[] for acc in accounts}

if "customers" not in st.session_state:
    st.session_state.customers = saved.get("customers",[])

def save():
    with open("data.json","w") as f:
        json.dump({
            "data": st.session_state.data,
            "customers": st.session_state.customers
        },f)

# ===== STYLE =====
style_map = {
"Trần Linh Diamond":"ban_hang",
"Trần Linh Jewellery":"cam_xuc",
"Trần Linh Kim Cương":"story",
"Trần Linh":"ban_hang",
"Diamond Linh":"chot_don",
"Fanpage":"ban_hang","Zalo":"chot_don","TikTok":"story"
}

def caption(c,s):
    hooks = {
        "ban_hang":["Mẫu này đang rất hot","Khách hỏi rất nhiều"],
        "cam_xuc":["Không cần nói nhiều","Chỉ một ánh nhìn"],
        "story":["Có một câu chuyện phía sau"],
        "chot_don":["Số lượng có hạn","Giữ ngay hôm nay"]
    }
    end = ["Inbox nhé","Bạn thấy sao?","Nhắn mình","Đừng bỏ lỡ"]
    return f"{random.choice(hooks[s])}\n\n{c}\n\n{random.choice(end)}"

def suggest_full(content, style="ban_hang"):
    if style == "cam_xuc":
        return f"Có những thứ không cần nói nhiều...\n\n{content}\n\nBạn thấy sao?"
    elif style == "chot_don":
        return f"Số lượng không nhiều...\n\n{content}\n\nInbox ngay để giữ mẫu 💎"
    elif style == "story":
        return f"Có một câu chuyện phía sau...\n\n{content}\n\nBạn có cảm nhận không?"
    else:
        return f"Mẫu này đang được hỏi rất nhiều...\n\n{content}\n\nInbox để xem chi tiết 💎"

# ===== AUTO =====
content_pool = ["Nhẫn kim cương","Dây chuyền sang trọng","Trang sức cao cấp","Mẫu mới đẹp","Phong cách tinh tế"]
time_slots = ["09:00","12:00","19:30","21:00"]

def auto():
    today = datetime.date.today()
    for i in range(7):
        d = str(today + datetime.timedelta(days=i))
        for acc in accounts:
            c = random.choice(content_pool)
            s = style_map[acc]
            st.session_state.data[acc].append({
                "date":d,
                "time":random.choice(time_slots),
                "content":c,
                "caption":caption(c,s)
            })
    save()

# ===== TABS =====
tabs = st.tabs(["💎1","💎2","💎3","💎4","💎5","📘","💬","🎬","🚀","💬","💰","🔁","📊","💾"])

# ===== HIỂN THỊ =====
for i,acc in enumerate(accounts):
    with tabs[i]:
        st.subheader(acc)
        for item in st.session_state.data[acc]:
            st.markdown(f"""
            <div class="card">
            📅 {item['date']} • {item['time']}<br><br>
            {item['content']}<br><br>
            <i>{item['caption']}</i>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"✨ Gợi ý lại {item['date']}", key=f"{acc}{item['date']}"):
                item["caption"] = suggest_full(item["content"], style_map[acc])
                save()
                st.rerun()

# ===== AUTO =====
with tabs[8]:
    if st.button("🔥 Tạo lịch 7 ngày"):
        auto()
        st.success("Đã tạo xong")

# ===== CHAT =====
with tabs[9]:
    txt = st.text_area("Comment khách")
    if st.button("Gợi ý"):
        for t in txt.split("\n"):
            if "giá" in t.lower():
                st.success("Inbox mình nhé 💎")
            else:
                st.success("Inbox tư vấn nhé 💎")

# ===== CHỐT =====
with tabs[10]:
    txt = st.text_area("Tin nhắn")
    if st.button("Chốt"):
        st.success("Mẫu này đang có khách giữ rồi, mình chốt sớm giúp em nhé 💎")

# ===== FOLLOW =====
def follow_msg(status):
    if "VIP" in status:
        return "Mẫu đó còn ít, em giữ giúp mình nhé 💎"
    elif "Quan tâm" in status:
        return "Em gửi thêm mẫu phù hợp hơn cho mình nhé 💎"
    else:
        return "Bên em có mẫu mới, mình xem thử nhé 💎"

with tabs[11]:
    name = st.text_input("Tên khách")
    if st.button("Follow"):
        st.success(f"Nhắn {name} ngay 💎")

# ===== CRM =====
with tabs[12]:
    name = st.text_input("Tên khách")
    note = st.text_input("Ghi chú")
    status = st.selectbox("Trạng thái", ["🔥 VIP","🙂 Quan tâm","❄️ Lạnh"])
    date = st.date_input("Follow")

    if st.button("Thêm khách"):
        st.session_state.customers.append({
            "name": name,
            "note": note,
            "status": status,
            "date": str(date)
        })
        save()
        st.success("Đã lưu")

    for c in st.session_state.customers:
        st.markdown(f"""
        <div class="card">
        👤 {c['name']}<br>
        {c['status']}<br>
        🧠 {c['note']}<br>
        ⏰ {c['date']}
        </div>
        """, unsafe_allow_html=True)
        st.write(follow_msg(c["status"]))

# ===== BACKUP =====
with tabs[13]:
    if st.button("📥 Xuất backup"):
        file = json.dumps({
            "data": st.session_state.data,
            "customers": st.session_state.customers
        }, ensure_ascii=False)

        st.download_button("Tải file", file, "backup.json")

    uploaded = st.file_uploader("Khôi phục", type="json")
    if uploaded:
        content = json.load(uploaded)
        st.session_state.data = content.get("data", {})
        st.session_state.customers = content.get("customers", [])
        save()
        st.success("Khôi phục thành công")