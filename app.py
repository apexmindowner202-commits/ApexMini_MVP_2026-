# NO 1-3: IMPORT (OTAK DASAR)
import streamlit as st
import requests
import json

# NO 5-20: FUNGSI KONEKSI OPENROUTER (JALUR BELAKANG PROFESIONAL)
def call_apex_engine(user_input):
    endpoint = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://apexmini.ai", 
        "X-Title": "ApexMini MVP 2026"
    }
    payload = {
        "model": "openrouter/auto", 
        "messages": [{"role": "user", "content": user_input}]
    }
    response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
    return response.json()['choices'][0]['message']['content']

# NO 22-DST: TAMPILAN ANTARMUKA (USER VERSION)
st.set_page_config(page_title="ApexMind Mini MVP", layout="centered")
st.title("🤖 ApexMind Chatbot Engine")

with st.expander("📸 Lampirkan Foto Proyek / Kode"):
    uploaded_file = st.file_uploader("Pilih gambar", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Visual Terdeteksi", use_column_width=True)

user_query = st.text_area("Masukan Instruksi User:", placeholder="Tuliskan di sini...")

if st.button("PROSES SEKARANG"):
    if user_query:
        with st.spinner("ApexMind sedang menganalisa..."):
            # DISINI KITA PANGGIL FUNGSI NOMOR 5 TADI!
            jawaban = call_apex_engine(user_query)
            st.markdown("### 🏛️ Hasil Analisa")
            st.write(jawaban)
    else:
        st.error("Peringatan: Input tidak boleh kosong!")



