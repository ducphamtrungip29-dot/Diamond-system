import streamlit as st

st.title("💎 Diamond System V2")

comment = st.text_area("Nhập comment khách hàng:")

def score_comment(c):
    c = c.lower()
    if "giá" in c or "bao nhiêu" in c:
        return 5
    elif "inbox" in c or "ib" in c:
        return 5
    elif "đẹp" in c:
        return 3
    else:
        return 1

if comment:
    score = score_comment(comment)
    st.write("🔥 Điểm:", score)