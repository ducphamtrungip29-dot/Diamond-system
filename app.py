import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("💎 Diamond System V4")

text = st.text_area("📥 Dán comment (mỗi dòng 1 comment):", height=200)

def score_comment(c):
    c = c.lower()
    if "giá" in c or "bao nhiêu" in c:
        return 5, "🔥 Khách hỏi giá"
    elif "inbox" in c or "ib" in c:
        return 5, "🔥 Khách quan tâm"
    elif "đẹp" in c:
        return 3, "🙂 Khách khen"
    else:
        return 1, "❄️ Khách lạnh"

if st.button("🚀 Phân tích ngay", use_container_width=True):

    if text.strip() == "":
        st.warning("⚠️ Chưa nhập dữ liệu")
    else:
        lines = text.split("\n")

        data = []

        for line in lines:
            score, label = score_comment(line)
            data.append({
                "Comment": line,
                "Phân loại": label,
                "Điểm": score
            })

        df = pd.DataFrame(data)

        st.subheader("🔥 Bảng kết quả:")
        st.dataframe(df, use_container_width=True)

        vip = df[df["Điểm"] >= 5]

        st.subheader("💰 Khách tiềm năng:")
        st.dataframe(vip, use_container_width=True)