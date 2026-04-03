import streamlit as st

st.title("Word Count App")
textInput = st.text_area("Masukkan teks Anda di sini:")

if st.button("Hitung Kata"):
    words = (textInput.split())
    #masing-masing kata dipisah menggunakan split() 
    #dihitung jumlahnya menggunakan len()
    #simpan didalam dictionary 
    counts = {}

    for word in words:
        counts[word] = counts.get(word, 0) + 1

    st.subheader("Frekuensi Kata")
    st.write(counts)

    st.bar_chart(counts)
