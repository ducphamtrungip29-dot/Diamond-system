import streamlit as st

st.title("💎 Diamond System V2")

st.write("👉 Dán comment khách (mỗi dòng 1 người)")

text = st.text_area("Nhập dữ liệu:")

def score(comment):
    c = comment.lower()
    if "bao nhiêu" in c or "giá" in c:
        return 5
    if "inbox" in c:
        return 5
    if "đẹp" in c:
        return 2
    return 1

def classify(s):
    if s >= 5:
        return "🔥 VIP"
    elif s >= 2:
        return "🌱 Tiềm năng"
    else:
        return "❌ Loại"

if st.button("🚀 Phân tích"):
    lines = text.split("\n")

    results = []

    for line in lines:
        if line.strip() == "":
            continue

        s = score(line)
        c = classify(s)

        results.append({
            "Khách": line,
            "Điểm": s,
            "Phân loại": c
        })

    st.write("📊 Kết quả:")
    st.dataframe(results)