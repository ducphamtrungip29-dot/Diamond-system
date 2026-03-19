import streamlit as st

st.set_page_config(layout="wide")

st.title("💎 Diamond System V3")

text = st.text_area("📥 Dán comment (mỗi dòng 1 comment):", height=200)

def score_comment(c):
    c = c.lower()
    if "giá" in c or "bao nhiêu" in c:
        return "🔥 Khách hỏi giá (5)"
    elif "inbox" in c or "ib" in c:
        return "🔥 Khách quan tâm (5)"
    elif "đẹp" in c:
        return "🙂 Khách khen (3)"
    else:
        return "❄️ Khách lạnh (1)"

# 👉 NÚT BẤM (QUAN TRỌNG)
if st.button("🚀 Phân tích ngay"):
    
    if text.strip() == "":
        st.warning("⚠️ Chưa nhập dữ liệu")
    else:
        lines = text.split("\n")

        st.subheader("🔥 Kết quả phân tích:")

        for line in lines:
            result = score_comment(line)
            st.write("👉", line, "→", result)