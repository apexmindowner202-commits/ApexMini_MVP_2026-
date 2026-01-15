import streamlit as st

import requests

import json



# --- 1. MESIN UTAMA (OTAK LLAMA 3 FREE) ---

def call_apex_engine(user_input):

    endpoint = "https://openrouter.ai/api/v1/chat/completions"

    headers = {

        "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",

        "Content-Type": "application/json"

    }

    payload = {

        "model": "meta-llama/llama-3-8b-instruct:free", 

        "messages": [{"role": "user", "content": user_input}]

    }

    

    try:

        response = requests.post(endpoint, headers=headers, data=json.dumps(payload))

        res_json = response.json()

        if 'choices' in res_json:

            return res_json['choices'][0]['message']['content']

        else:

            return f"API Error: {res_json.get('error', 'Cek Koneksi atau Secrets!')}"

    except Exception as e:

        return f"System Error: {str(e)}"



# --- 2. TAMPILAN ANTARMUKA (WAJAH APEXMINI) ---

st.set_page_config(page_title="ApexMini MVP", page_icon="🦾")

st.title("🦾 ApexMini MVP 2026")

st.write("Sistem AI Sinkronisasi Magnetik")



# Input Teks

user_query = st.text_input("Input Pertanyaan:", "")



# Tombol Eksekusi

if st.button("Proses Ke Apex Engine"):

    if user_query:

        with st.spinner("Proses analisa..."):

            jawaban = call_apex_engine(user_query)

            st.success("Hasil Analisa:")

            st.write(jawaban)

    else:

        st.warning("Silakan isi pertanyaan terlebih dahulu.")



# Fitur Upload Foto

uploaded_file = st.file_uploader("Upload Foto (Maksimal 2 Foto):", type=["jpg", "png", "jpeg"])

if uploaded_file:

    st.image(uploaded_file, caption="File Terunggah", use_container_width=True)

    st.info("Analisa visual akan diaktifkan setelah sistem inti stabil.")



