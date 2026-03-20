import streamlit as st
import datetime, json, os, re

try:
    from openai import OpenAI
except:
    OpenAI = None

st.set_page_config(layout="wide")
st.title("💎 Diamond System V16")

# ===== API =====
api_key = st.text_input("🔑 API Key AI", type="password")
client = OpenAI(api_key=api_key) if (api_key and OpenAI) else None

# ===== ACCOUNTS =====
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

# ===== LOAD =====
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

# ===== SAVE =====
def save():
    with open("data.json","w",encoding="utf-8") as f:
        json.dump(st.session_state.data, f, ensure_ascii=False)

# ===== PARSE CHATGPT TEXT =====
def parse_text(txt):

    current = None
    time = ""
    content = ""
    caption = ""

    for line in txt.split("\n"):

        line = line.strip()

        # ===== detect time + account =====
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

# ===== SORT =====
def sort_data():
    for acc in accounts:
        st.session_state.data[acc].sort(key=lambda x: x.get("time",""))

# ===== TABS =====
tabs = st.tabs(accounts + ["📥 Nhập","🧠 AI","💰 CRM"])

# ===== DISPLAY =====
for i, acc in enumerate(accounts):
    with tabs[i]:
        st.subheader(acc)

        # SORT trước khi hiển thị
        sort_data()

        for item in st.session_state.data[acc]:
            st.write(f"{item['time']} - {item['content']}")
            st.caption(item['caption'])

# ===== IMPORT =====
with tabs[len(accounts)]:
    txt = st.text_area("Dán lịch ChatGPT")

    if st.button("🔥 Xử lý"):
        parse_text(txt)
        st.success("Đã phân tích đúng format ChatGPT")

# ===== AI =====
with tabs[len(accounts)+1]:

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

# ===== CRM =====
with tabs[len(accounts)+2]:

    name = st.text_input("Tên khách")

    if st.button("Thêm"):
        st.session_state.customers.append(name)
        save()

    for c in st.session_state.customers:
        st.write("👤",c)
