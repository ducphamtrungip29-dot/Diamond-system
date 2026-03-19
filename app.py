import streamlit as st
import pandas as pd
import datetime
import json
import os

st.set_page_config(layout="wide")
st.title("💎 Diamond System FINAL")

# ===== LOAD DATA =====
if "data" not in st.session_state:
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            st.session_state.data = json.load(f)
    else:
        st.session_state.data = []

# ===== PROFILE (ID KHÓA CỨNG) =====
if "profiles" not in st.session_state:
    st.session_state.profiles = {
        "fb1": {"name": "FB 1", "image": None},
        "fb2": {"name": "FB 2", "image": None},
        "fb3": {"name": "FB 3", "image": None},
        "fb4": {"name": "FB 4", "image": None},
        "fb5": {"name": "FB 5", "image": None},
        "fanpage1": {"name": "Fanpage", "image": None},
        "zalo1": {"name": "Zalo", "image": None},
        "tiktok1": {"name": "TikTok", "image": None},
    }

tab_ids = list(st.session_state.profiles.keys())
tab_labels = [st.session_state.profiles[i]["name"] for i in tab_ids]

tabs = st.tabs(tab_labels + ["📥 Nhập lịch", "🧠 V6", "⚙️ Cài đặt"])

# ===== HIỂN THỊ LỊCH =====
for i, pid in enumerate(tab_ids):
    with tabs[i]:
        profile = st.session_state.profiles[pid]

        st.markdown(f"### 👤 {profile['name']}")

        if profile["image"]:
            st.image(profile["image"], use_container_width=True)

        df = pd.DataFrame(st.session_state.data)

        if not df.empty:
            st.dataframe(df[df["Kênh"] == pid], use_container_width=True)

# ===== PARSE AUTO =====
def parse(text):
    mapping = {
        "fb 1": "fb1",
        "fb 2": "fb2",
        "fb 3": "fb3",
        "fb 4": "fb4",
        "fb 5": "fb5",
        "fanpage": "fanpage1",
        "zalo": "zalo1",
        "tiktok": "tiktok1"
    }

    lines = text.split("\n")
    result = []

    for line in lines:
        parts = line.split("|")

        if len(parts) >= 5:
            channel_input = parts[0].strip().lower()
            channel_id = mapping.get(channel_input, "fb1")

            result.append({
                "Kênh": channel_id,
                "Ngày": parts[1].strip(),
                "Giờ": parts[2].strip(),
                "Nội dung": parts[3].strip(),
                "Loại": parts[4].strip()
            })

    return result

# ===== NHẬP LỊCH =====
with tabs[len(tab_ids)]:
    st.subheader("📥 Dán lịch")

    st.info("Ví dụ: FB 1|19/03|09:00|Đăng bài|Post")

    text = st.text_area("Dán vào đây", height=200)

    if st.button("🚀 Lưu lịch"):
        new = parse(text)

        st.session_state.data.extend(new)

        with open("data.json", "w") as f:
            json.dump(st.session_state.data, f)

        st.success(f"Đã lưu {len(new)} lịch")

# ===== V6 =====
with tabs[len(tab_ids)+1]:
    st.subheader("🧠 Phân tích khách")

    cmt = st.text_area("Dán comment")

    def score(c):
        c = c.lower()
        if "giá" in c:
            return "🔥 VIP", "Inbox chốt giá"
        elif "ib" in c:
            return "🔥 Quan tâm", "Check inbox"
        elif "đẹp" in c:
            return "🙂 Khen", "Giữ tương tác"
        else:
            return "❄️ Lạnh", "Bỏ qua"

    if st.button("Phân tích"):
        for line in cmt.split("\n"):
            tag, rep = score(line)
            st.write(f"{line} → {tag}")
            st.write(f"💬 {rep}")

# ===== CÀI ĐẶT =====
with tabs[len(tab_ids)+2]:
    st.subheader("⚙️ Tùy chỉnh kênh")

    selected = st.selectbox("Chọn kênh", tab_ids)

    new_name = st.text_input("Tên", st.session_state.profiles[selected]["name"])
    img = st.file_uploader("Ảnh", type=["png","jpg"])

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
SUMMARY:{item['Kênh']} - {item['Nội dung']}
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

if st.button("📥 Xuất lịch (có thông báo 5p)"):
    export(st.session_state.data)

    with open("schedule.ics","rb") as f:
        st.download_button("📱 Tải file", f, "schedule.ics")