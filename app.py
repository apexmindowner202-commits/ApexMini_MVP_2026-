import streamlit as st
import requests
from PIL import Image
import io

# --- 1. CORE AUTHENTICATION ---
try:
    API_TOKEN = st.secrets["GITHUB_TOKEN"]
    TEXT_MODEL = "https://models.inference.ai.azure.com/chat/completions"
    # Menggunakan model Pony Diffusion V6 XL / Illustrious XL
    VISUAL_MODEL = "https://api-inference.huggingface.co/models/Lykon/Pony-Diffusion-V6-XL"
except Exception:
    st.error("Authentication Error: GITHUB_TOKEN tidak terdeteksi.")
    st.stop()

# --- 2. LOGIKA EKSEKUSI (TEXT & VISUAL) ---
def apex_logic(prompt):
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "messages": [
            {"role": "system", "content": "Kamu adalah ApexMini. AI profesional dari komunitas Open Source. Jawab dalam Bahasa Indonesia. Sembunyikan tag <think>."},
            {"role": "user", "content": prompt}
        ],
        "model": "DeepSeek-R1",
        "temperature": 0.6
    }
    try:
        response = requests.post(TEXT_MODEL, headers=headers, json=payload, timeout=30)
        res = response.json()['choices'][0]['message']['content']
        return res.split("</think>")[-1].strip() if "</think>" in res else res
    except: return "Error koneksi logika."

def apex_visual(refined_prompt):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    try:
        response = requests.post(VISUAL_MODEL, headers=headers, json={"inputs": refined_prompt}, timeout=60)
        return response.content if response.status_code == 200 else None
    except: return None

# --- 3. UI DESIGN (REPLIKA DARK CHATGPT) ---
st.set_page_config(page_title="ApexMini Pro", layout="centered")

st.markdown("""
    <style>
    /* Reset Padding & Background */
    .stApp { background-color: #000000; color: #FFFFFF; }
    .block-container { padding-top: 0rem !important; }
    
    /* Header Merah ApexMini Mepet */
    .header-apex { color: #FF0000; font-size: 2.2rem; font-weight: 900; text-align: center; margin-bottom: 5px; padding-top: 10px; }
    
    /* Sembunyikan Elemen Norak */
    footer, header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    
    /* Layout Foto Tengah & Rapat */
    .stChatMessage { background-color: transparent !important; margin-top: -20px !important; }
    .stChatInput { border-radius: 20px !important; background-color: #212121 !important; }
    </style>
    <div class="header-apex">APEXMINI</div>
""", unsafe_allow_html=True)

# --- 4. SESSION MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 5. CHAT DISPLAY ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if "images" in m:
            cols = st.columns(len(m["images"]))
            for idx, img in enumerate(m["images"]):
                cols[idx].image(img, use_container_width=True)
        st.markdown(f"<div style='text-align: center;'>{m['content']}</div>", unsafe_allow_html=True)

# --- 6. MULTI-UPLOAD & INPUT ---
# Komponen upload diletakkan tepat di atas input bar agar terasa terintegrasi
files = st.file_uploader("Upload", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True, label_visibility="collapsed")

if prompt := st.chat_input("Tanyakan apa saja atau minta visual..."):
    user_data = {"role": "user", "content": prompt}
    if files:
        user_data["images"] = [Image.open(f) for f in files]
    
    st.session_state.messages.append(user_data)
    st.rerun()

# --- 7. ASSISTANT PROCESSING ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        last_prompt = st.session_state.messages[-1]["content"]
        
        # Eksekusi Teks
        text_res = apex_logic(last_prompt)
        st.markdown(f"<div style='text-align: center;'>{text_res}</div>", unsafe_allow_html=True)
        
        # Eksekusi Visual Otomatis (Jika terdeteksi permintaan gambar)
        if any(w in last_prompt.lower() for w in ["buat", "gambar", "visual", "generate"]):
            with st.spinner(""):
                img = apex_visual(text_res)
                if img:
                    st.image(img, use_container_width=True)
        
        st.session_state.messages.append({"role": "assistant", "content": text_res})



