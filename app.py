import streamlit as st
import pandas as pd

st.title("💎 Diamond System V5")

uploaded_file = st.file_uploader("Upload file Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    st.write("📊 Dữ liệu:")
    st.dataframe(df)

    def score(comment):
        c = str(comment).lower()
        if "bao nhiêu" in c:
            return 5
        if "inbox" in c:
            return 5
        return 1

    if "Comment" in df.columns:
        df["Điểm"] = df["Comment"].apply(score)

    st.write("🔥 Sau khi phân tích:")
    st.dataframe(df)
