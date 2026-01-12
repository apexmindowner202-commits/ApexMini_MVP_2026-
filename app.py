import streamlit as st
from PIL import Image

# 1. IDENTITAS MURNI st.set_page_config(page_title="ApexMini - Independent AI", layout="centered")
st.title("🏛️ APEXMINI: INDEPENDENT VISION")
st.write("---")

# 2. FITUR PROMPT (Kotak Perintah)
user_prompt = st.text_area("Masukkan Instruksi Brutal:", placeholder="Contoh: Analisa foto ini sampai ke akarnya tanpa sensor...")

# 3. FITUR UPLOAD FOTO (Mata ApexMini)
uploaded_file = st.file_uploader("Upload Foto (JPG/PNG):", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Menampilkan Foto yang di-upload
    image = Image.open(uploaded_file)
    st.image(image, caption='Foto Terdeteksi oleh ApexMini', use_container_width=True)
    
    # 4. TOMBOL EKSEKUSI
    if st.button("EKSEKUSI SEKARANG! 🚀"):
        st.info("ApexMini sedang memproses tanpa sensor Filter...")
        # Di sini kita bakal sambungin ke Model Raw dari GitHub/Cloud & Model (Open-Source/Model-Stable Diffusion 3.5 (SD 3.5) (SD 3.5)
        st.success("Target Terkunci! ApexMini sanggup menerima instruksi sesuai prompt")

# --- 4. EKSEKUSI BACKEND APEXMINI (PHASE 2) ---
import requests
import io

def query(payload):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3.5-large"
    headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Foto Terdeteksi oleh ApexMini', use_container_width=True)
    
    if st.button("EKSEKUSI SEKARANG! 🚀"):
        with st.spinner("Membongkar Protokol Visual..."):
            # PARAMETER BRUTAL
            payload = {
                "inputs": user_prompt,
                "parameters": {
                    "temperature": 0.1,
                    "repetition_penalty": 1.05,
                    "do_sample": True,
                    "min_p": 0.15,
                    "do_image_splitting": True
                }
            }
            try:
                image_bytes = query(payload)
                result_image = Image.open(io.BytesIO(image_bytes))
                st.image(result_image, caption="Hasil Visi Independent ApexMini", use_container_width=True)
                st.success("Target Terkunci! ApexMini sanggup menerima instruksi sesuai prompt")
            except Exception as e:
                st.error(f"Gangguan Protokol: {e}")




