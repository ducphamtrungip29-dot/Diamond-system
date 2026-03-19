import streamlit as st
import pandas as pd

st.title("Diamond System V5")

text = st.text_area("Nhap comment (moi dong 1 comment):")

def score(c):
    c = c.lower()
    if "gia" in c or "bao nhieu" in c:
        return 5, "Khach hoi gia"
    elif "ib" in c or "inbox" in c:
        return 5, "Khach quan tam"
    elif "dep" in c:
        return 3, "Khach khen"
    else:
        return 1, "Khach lanh"

if st.button("Phan tich"):

    if text.strip() == "":
        st.write("Chua nhap du lieu")
    else:
        lines = text.split("\n")
        data = []

        for line in lines:
            s, l = score(line)
            data.append({
                "Comment": line,
                "Loai": l,
                "Diem": s
            })

        df = pd.DataFrame(data)

        st.write("Bang ket qua:")
        st.dataframe(df)

        vip = df[df["Diem"] >= 5]

        st.write("Khach tiem nang:")

        if len(vip) == 0:
            st.write("Khong co")
        else:
            st.write("Co", len(vip), "khach")

            for i, row in vip.iterrows():
                st.write("-", row["Comment"], "(", row["Loai"], ")")

            st.dataframe(vip)