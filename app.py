import streamlit as st
import requests
from PIL import Image
import io

# --- 1. CORE AUTH ---
try:
    API_TOKEN = st.secrets["GITHUB_TOKEN"]
    TEXT_MODEL = "https://models.inference.ai.azure.com/chat/completions"
    # Menggunakan FLUX.1 untuk hasil 99% realistik sesuai permintaan
    VISUAL_ENGINE = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
except Exception:
    st.error("Gagal memuat Token.")
    st.stop()

# --- 2. ENGINE LOGIC ---
def get_logic_response(user_input):
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    # SYSTEM PROMPT DIPERKETAT: Jangan kasih tutorial, kasih PROMPT GAMBAR
    payload = {
        "messages": [
            {
                "role": "system", 
                "content": "You are ApexMini. If user asks for visual/editing, DO NOT give text instructions. Instead, translate their request into a high-detail, realistic image generation prompt in English. Output ONLY the visual prompt. No talk."
            },
            {"role": "user", "content": user_input}
        ],
        "model": "DeepSeek-R1", "temperature": 0.2
    }
    try:
        response = requests.post(TEXT_MODEL, headers=headers, json=payload, timeout=30)
        res = response.json()['choices'][0]['message']['content']
        return res.split("</think>")[-1].strip() if "</think>" in res else res
    except: return "Logic Error."

def generate_visual(visual_prompt):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    try:
        response = requests.post(VISUAL_ENGINE, headers=headers, json={"inputs": visual_prompt}, timeout=120)
        return response.content if response.status_code == 200 else None
    except: return None

# --- 3. UI LAYOUT (COMPACT & SIDE-BY-SIDE) ---
st.set_page_config(page_title="ApexMini", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    .main .block-container { padding-top: 0rem !important; }
    .header-apex { color: #FF0000; font-size: 2.2rem; font-weight: 900; text-align: center; padding: 10px 0; }
    footer, header, [data-testid="stHeader"] { visibility: hidden; }
    .stChatMessage { background-color: transparent !important; }
    /* Animasi Loading Spinner Merah */
    .stSpinner > div { border-top-color: #FF0000 !important; }
    </style>
    <div class="header-apex">APEXMINI</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. CHAT & RENDER ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(f"<div style='text-align: center;'>{m['content']}</div>", unsafe_allow_html=True)
        if "img" in m: st.image(m["img"], use_container_width=True)

# --- 5. INPUT BAR ---
c1, c2 = st.columns([0.15, 0.85])
with c1:
    files = st.file_uploader("📎", type=['png','jpg','jpeg'], accept_multiple_files=True, label_visibility="collapsed")
with c2:
    prompt = st.chat_input("Input command...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        # 1. ApexMini merumuskan prompt visual secara "senyap"
        visual_desc = get_logic_response(prompt)
        
        # 2. Eksekusi Visual dengan Loading Muter-muter
        with st.spinner("ApexMini sedang merender visual..."):
            img_result = generate_visual(visual_desc)
            if img_result:
                st.image(img_result, use_container_width=True)
                st.session_state.messages.append({"role": "assistant", "content": "Visual Berhasil Dirender.", "img": img_result})
            else:
                st.error("Gagal merender gambar.")
    st.rerun()

