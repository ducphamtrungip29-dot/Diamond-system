import streamlit as st
import pandas as pd
import datetime
import re

st.set_page_config(layout="wide")

st.title("💎 Diamond System PRO")

# ===== PROFILE DATA =====
if "profiles" not in st.session_state:
    st.session_state.profiles = {
        "FB 1": {"name": "FB 1", "image": None},
        "FB 2": {"name": "FB 2", "image": None},
        "FB 3": {"name": "FB 3", "image": None},
        "FB 4": {"name": "FB 4", "image": None},
        "FB 5": {"name": "FB 5", "image": None},
        "Fanpage": {"name": "Fanpage", "image": None},
        "Zalo": {"name": "Zalo", "image": None},
        "TikTok": {"name": "TikTok", "image": None},
    }

# ===== DATA =====
if "data" not in st.session_state:
    st.session_state.data = []

# ===== TABS =====
tab_names = list(st.session_state.profiles.keys())
tabs = st.tabs(tab_names + ["📥 Nhập lịch", "🧠 V6", "⚙️ Cài đặt"])

# ===== HIỂN THỊ LỊCH =====
for i, tab_name in enumerate(tab_names):
    with tabs[i]:
        profile = st.session_state.profiles[tab_name]

        st.subheader(f"👤 {profile['name']}")

        if profile["image"]:
            st.image(profile["image"], use_container_width=True)

        df = pd.DataFrame(st.session_state.data)

        if not df.empty:
            st.dataframe(df[df["Kênh"] == tab_name], use_container_width=True)

# ===== NHẬP LỊCH =====
with tabs[len(tab_names)]:
    st.subheader("📥 Dán lịch")

    text = st.text_area("Format: 19/03|09:00|Nội dung|Loại", height=200)

    def parse(text):
        lines = text.split("\n")
        result = []

        for line in lines:
            parts = line.split("|")
            if len(parts) >= 4:
                result.append({
                    "Ngày": parts[0].strip(),
                    "Giờ": parts[1].strip(),
                    "Nội dung": parts[2].strip(),
                    "Loại": parts[3].strip(),
                    "Kênh": "FB 1"
                })
        return result

    if st.button("🚀 Lưu"):
        new = parse(text)
        st.session_state.data.extend(new)
        st.success(f"Đã thêm {len(new)} lịch")

# ===== V6 =====
with tabs[len(tab_names)+1]:
    st.subheader("🧠 Phân tích khách")

    cmt = st.text_area("Dán comment")

    def score(c):
        c = c.lower()
        if "giá" in c:
            return "🔥 VIP", "Inbox chốt giá"
        elif "ib" in c:
            return "🔥 Quan tâm", "Check inbox"
        else:
            return "❄️ Lạnh", "Nuôi tiếp"

    if st.button("Phân tích"):
        lines = cmt.split("\n")
        for line in lines:
            tag, reply = score(line)
            st.write(f"{line} → {tag}")
            st.write(f"💬 {reply}")

# ===== CÀI ĐẶT =====
with tabs[len(tab_names)+2]:
    st.subheader("⚙️ Cài đặt nick")

    selected = st.selectbox("Chọn", tab_names)

    new_name = st.text_input("Tên mới", st.session_state.profiles[selected]["name"])
    img = st.file_uploader("Ảnh nền", type=["png","jpg"])

    if st.button("💾 Lưu"):
        st.session_state.profiles[selected]["name"] = new_name
        if img:
            st.session_state.profiles[selected]["image"] = img
        st.success("Đã lưu")

# ===== EXPORT ICS =====
def export(data):
    ics = "BEGIN:VCALENDAR\nVERSION:2.0\n"

    for item in data:
        try:
            dt = datetime.datetime.strptime(item["Ngày"]+" "+item["Giờ"], "%d/%m %H:%M")
        except:
            continue

        dt_str = dt.strftime("%Y%m%dT%H%M%S")

        ics += f"""BEGIN:VEVENT
SUMMARY:{item['Nội dung']}
DTSTART:{dt_str}
BEGIN:VALARM
TRIGGER:-PT5M
ACTION:DISPLAY
DESCRIPTION:Đến giờ đăng bài
END:VALARM
END:VEVENT
"""

    ics += "END:VCALENDAR"

    with open("schedule.ics","w") as f:
        f.write(ics)

if st.button("📥 Xuất lịch"):
    export(st.session_state.data)
    with open("schedule.ics","rb") as f:
        st.download_button("Tải file", f, "schedule.ics")