
 import streamlit as st
import requests
import base64
from PIL import Image
import io

# --- 1. CORE CONFIGURATION ---
try:
    API_TOKEN = st.secrets["GITHUB_TOKEN"]
    # Endpoint untuk Teks (DeepSeek R1)
    TEXT_ENDPOINT = "https://models.inference.ai.azure.com/chat/completions"
    # Endpoint untuk Visual (Hugging Face / Stable Diffusion)
    # Sesuaikan dengan API yang Maestro gunakan untuk Illustrious/Pony
    IMAGE_API_URL = "https://api-inference.huggingface.co/models/Lykon/Pony-Diffusion-V6-XL" 
except Exception:
    st.error("Authentication Error: API Tokens not configured in Secrets.")
    st.stop()

# --- 2. ENGINE LOGIC ---

# Fungsi Logika Teks & Matematika
def execute_logic(prompt):
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "messages": [
            {"role": "system", "content": "You are ApexMini. Specialist in math and visual prompting. Identity: Open Source Community."},
            {"role": "user", "content": prompt}
        ],
        "model": "DeepSeek-R1",
        "temperature": 0.6
    }
    try:
        response = requests.post(TEXT_ENDPOINT, headers=headers, json=payload, timeout=30)
        return response.json()['choices'][0]['message']['content']
    except: return "System Error on Logic Engine."

# Fungsi Eksekusi Visual (Multi-Image Support & Generation)
def generate_visual(prompt):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    try:
        response = requests.post(IMAGE_API_URL, headers=headers, json={"inputs": prompt}, timeout=60)
        return response.content
    except: return None

# --- 3. PROFESSIONAL UI DESIGN ---
st.set_page_config(page_title="ApexMini Pro", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    .header-apexmini { color: #FF0000; font-size: 2.5rem; font-weight: 800; text-align: center; padding: 40px 0; letter-spacing: 2px; }
    footer, header {visibility: hidden;}
    .stChatMessage { background-color: #0c0c0c; border: 1px solid #1a1a1a; border-radius: 15px; }
    </style>
    <div class="header-apexmini">APEXMINI</div>
""", unsafe_allow_html=True)

# --- 4. CHAT & VISUAL INTERFACE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display history
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])
        if "images" in chat:
            cols = st.columns(len(chat["images"]))
            for idx, img in enumerate(chat["images"]):
                cols[idx].image(img, use_container_width=True)

# Input Area (Teks & Multi-Photo)
with st.container():
    uploaded_files = st.file_uploader("Upload reference photos...", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True, label_visibility="collapsed")
    prompt = st.chat_input("Enter your prompt for visual or math formulation...")

if prompt:
    current_chat = {"role": "user", "content": prompt}
    if uploaded_files:
        current_chat["images"] = [Image.open(f) for f in uploaded_files]
    
    st.session_state.chat_history.append(current_chat)
    
    # Jalankan tampilan user
    with st.chat_message("user"):
        st.markdown(prompt)
        if uploaded_files:
            cols = st.columns(len(uploaded_files))
            for i, f in enumerate(uploaded_files): cols[i].image(f, use_container_width=True)

    # Jalankan Respons Assistant
    with st.chat_message("assistant"):
        # 1. Dapatkan Perumusan Teks/Logika
        response_text = execute_logic(prompt)
        st.markdown(response_text)
        
        # 2. Jika prompt mengandung perintah visual, hasilkan gambar
        if any(word in prompt.lower() for word in ["buat", "gambar", "visual", "generate", "design"]):
            with st.spinner("Generating high-fidelity visual..."):
                img_bytes = generate_visual(response_text) # Gunakan CoT dari R1 untuk prompt visual
                if img_bytes:
                    st.image(img_bytes, caption="ApexMini Visual Output", use_container_width=True)

        st.session_state.chat_history.append({"role": "assistant", "content": response_text})       



