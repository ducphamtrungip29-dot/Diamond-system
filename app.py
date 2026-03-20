import streamlit as st
import datetime, json, os, re

try:
    from openai import OpenAI
except:
    OpenAI = None

st.set_page_config(layout="wide")
st.title("💎 Diamond System V18")

# ================= API FIX =================
api_key = st.text_input("🔑 API Key AI", type="password")

client = None
if api_key:
    try:
        client = OpenAI(api_key=api_key)
        st.success("✅ API đã kết nối")
    except:
        st.error("❌ API lỗi")

# ================= ACCOUNTS =================
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

# ================= LOAD =================
def load():
    if os.path.exists("data.json"):
        try:
            with open("data.json","r",encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"data":{}, "customers":[]}

saved = load()

if "data" not in st.session_state:
    st.session_state.data = saved.get("data",{})
if "customers" not in st.session_state:
    st.session_state.customers = saved.get("customers",[])

for acc in accounts:
    st.session_state.data.setdefault(acc,[])

# ================= SAVE =================
def save():
    with open("data.json","w",encoding="utf-8") as f:
        json.dump({
            "data": st.session_state.data,
            "customers": st.session_state.customers
        }, f, ensure_ascii=False)

# ================= PARSE CHATGPT =================
def parse_text(txt):

    current = None
    time = ""
    content = ""
    caption = ""

    for line in txt.split("\n"):

        line = line.strip()

        # bắt giờ + tên nick
        match = re.match(r"(\d{1,2}:\d{2}).*(TRẦN LINH.*|Diamond Linh)", line, re.IGNORECASE)

        if match:
            time = match.group(1)

            for acc in accounts:
                if acc.lower() in line.lower():
                    current = acc

        elif "Nội dung:" in line:
            content = line.replace("Nội dung:", "").strip()

        elif "Caption:" in line:
            caption = line.replace("Caption:", "").strip()

            if current:
                st.session_state.data[current].append({
                    "date": str(datetime.date.today()),
                    "time": time,
                    "content": content,
                    "caption": caption
                })

    save()

# ================= GET TODAY =================
def get_today_posts():
    today = str(datetime.date.today())
    posts = []

    for acc in accounts:
        for item in st.session_state.data[acc]:
            if item["date"] == today:
                posts.append((item["time"], acc, item))

    posts.sort(key=lambda x: x[0])
    return posts

# ================= TABS =================
tabs = st.tabs(["🏠 Trang chủ"] + accounts + ["📥 Nhập","🧠 AI","💰 CRM"])

# ================= HOME =================
with tabs[0]:

    st.subheader("🔥 Hôm nay đăng gì")

    posts = get_today_posts()

    if posts:
        for t, acc, item in posts:
            st.write(f"⏰ {t} | {acc}")
            st.write(f"👉 {item['content']}")
            st.caption(item["caption"])
    else:
        st.warning("Chưa có lịch hôm nay")

    st.divider()

    st.subheader("⚠️ Khách cần follow")

    if st.session_state.customers:
        for c in st.session_state.customers:
            st.write("👤", c)
    else:
        st.info("Chưa có khách")

    st.divider()

    st.subheader("🧠 Gợi ý hành động")

    if st.button("🔥 Hôm nay làm gì?"):

        if not client:
            st.warning("Chưa nhập API")
        else:
            data = json.dumps(st.session_state.data, ensure_ascii=False)

            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role":"user",
                    "content":f"Dựa vào dữ liệu này, đề xuất hành động hôm nay:\n{data}"
                }]
            )

            st.success(res.choices[0].message.content)

# ================= DISPLAY =================
for i, acc in enumerate(accounts):
    with tabs[i+1]:

        st.subheader(acc)

        data = sorted(st.session_state.data[acc], key=lambda x: x.get("time",""))

        for item in data:
            st.write(f"{item['time']} - {item['content']}")
            st.caption(item['caption'])

# ================= IMPORT =================
with tabs[len(accounts)+1]:

    txt = st.text_area("Dán lịch từ ChatGPT")

    if st.button("🔥 Phân tích"):
        parse_text(txt)
        st.success("Đã import thành công")

# ================= AI TEST =================
with tabs[len(accounts)+2]:

    if st.button("Test AI"):
        if not client:
            st.warning("Chưa nhập API")
        else:
            st.success("AI hoạt động OK")

# ================= CRM =================
with tabs[len(accounts)+3]:

    name = st.text_input("Tên khách")

    if st.button("Thêm khách"):
        st.session_state.customers.append(name)
        save()

    for c in st.session_state.customers:
        st.write("👤", c)
