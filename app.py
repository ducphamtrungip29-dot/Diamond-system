import streamlit as st
import datetime, json, os

try:
    from openai import OpenAI
except:
    OpenAI = None

st.set_page_config(layout="wide")
st.markdown("<style>.block-container {padding-top:10px;}</style>", unsafe_allow_html=True)

st.title("💎 Diamond System V15 - FINAL")

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
    try:
        if os.path.exists("data.json"):
            with open("data.json","r",encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return {"data":{}, "notes":{}, "customers":[]}

saved = load()

# ===== INIT =====
if "data" not in st.session_state:
    st.session_state.data = saved.get("data",{})
if "notes" not in st.session_state:
    st.session_state.notes = saved.get("notes",{})
if "customers" not in st.session_state:
    st.session_state.customers = saved.get("customers",[])

for acc in accounts:
    st.session_state.data.setdefault(acc,[])
    st.session_state.notes.setdefault(acc,"")

# ===== SAVE =====
def save():
    with open("data.json","w",encoding="utf-8") as f:
        json.dump({
            "data":st.session_state.data,
            "notes":st.session_state.notes,
            "customers":st.session_state.customers
        },f,ensure_ascii=False)

# ===== IMPORT CHATGPT STYLE =====
def import_text(txt):
    current = None
    content = ""

    for line in txt.split("\n"):

        line = line.strip()

        if line in accounts:
            current = line

        elif "Nội dung:" in line:
            content = line.replace("Nội dung:","").strip()

        elif "Ghi chú:" in line and current:
            note = line.replace("Ghi chú:","").strip()

            st.session_state.data[current].append({
                "date":str(datetime.date.today()),
                "content":content
            })

            st.session_state.notes[current] = note

    save()

# ===== TABS =====
tabs = st.tabs(accounts + [
"📥 Nhập","🔥 Chốt","📈 Follow","🎯 Khách","🧠 AI Điều hành","💰 CRM"
])

# ===== DISPLAY =====
for i, acc in enumerate(accounts):
    with tabs[i]:
        st.subheader(acc)
        st.info(st.session_state.notes[acc])

        for item in st.session_state.data[acc]:
            st.write(item)

# ===== IMPORT =====
with tabs[len(accounts)]:
    txt = st.text_area("Dán lịch kiểu ChatGPT")

    if st.button("🔥 Xử lý"):
        import_text(txt)
        st.success("Đã phân loại đúng tab")

# ===== CHỐT =====
with tabs[len(accounts)+1]:
    msg = st.text_area("Tin nhắn khách")

    if st.button("Chốt"):
        if client:
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role":"user","content":f"Chốt sale: {msg}"}]
            )
            st.success(res.choices[0].message.content)

# ===== FOLLOW =====
with tabs[len(accounts)+2]:
    msg = st.text_area("Follow")

    if st.button("Gợi ý"):
        if client:
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role":"user","content":f"Follow up: {msg}"}]
            )
            st.success(res.choices[0].message.content)

# ===== KHÁCH =====
with tabs[len(accounts)+3]:

    if st.button("Chọn khách dễ chốt"):
        if client and st.session_state.customers:
            text = ", ".join(st.session_state.customers)

            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role":"user","content":f"Chọn khách dễ chốt: {text}"}]
            )

            st.success(res.choices[0].message.content)

# ===== AI ĐIỀU HÀNH =====
with tabs[len(accounts)+4]:

    if st.button("🔥 Hôm nay làm gì?"):

        if client:
            data = json.dumps(st.session_state.data, ensure_ascii=False)
            notes = json.dumps(st.session_state.notes, ensure_ascii=False)

            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role":"user",
                    "content":f"""
Dữ liệu:
{data}

Ghi chú:
{notes}

Đề xuất hành động hôm nay
"""
                }]
            )

            st.success(res.choices[0].message.content)

# ===== CRM =====
with tabs[len(accounts)+5]:

    name = st.text_input("Tên khách")

    if st.button("Thêm"):
        st.session_state.customers.append(name)
        save()

    for c in st.session_state.customers:
        st.write("👤",c)
