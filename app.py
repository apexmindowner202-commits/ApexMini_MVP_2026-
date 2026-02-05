import streamlit as st
import requests
from PIL import Image
import io

# --- 1. CORE AUTH ---
try:
    API_TOKEN = st.secrets["GITHUB_TOKEN"]
    R1_URL = "https://models.inference.ai.azure.com/chat/completions"
    PONY_URL = "https://api-inference.huggingface.co/models/Lykon/Pony-Diffusion-V6-XL"
except Exception:
    st.error("Token GITHUB_TOKEN Missing!")
    st.stop()

# --- 2. LOGIC ENGINE ---
def get_r1_response(user_input):
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "messages": [{"role": "system", "content": "You are ApexMini R1. Use CoT. Indonesian answer. Detailed Pony V6 XL prompt for visuals."},
                    {"role": "user", "content": user_input}],
        "model": "DeepSeek-R1", "temperature": 0.6
    }
    try:
        res = requests.post(R1_URL, headers=headers, json=payload, timeout=60)
        if res.status_code == 200:
            full = res.json()['choices'][0]['message']['content']
            if "</think>" in full:
                parts = full.split("</think>")
                return parts[0].replace("<think>", "").strip(), parts[1].strip()
            return None, full
        return None, f"Error {res.status_code}"
    except: return None, "Koneksi Terputus"

def generate_pony(p):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    try:
        res = requests.post(PONY_URL, headers=headers, json={"inputs": f"score_9, score_8_up, {p}"}, timeout=120)
        return res.content if res.status_code == 200 else None
    except: return None

# --- 3. UI LAYOUT (KUNCI KEBEBASAN) ---
st.set_page_config(page_title="ApexMini", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Full Black Mode */
    .stApp { background-color: #000000; color: #FFFFFF; }
    
    /* Maksa Chat Jadi LEGA */
    .main .block-container {
        max-width: 100% !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 2rem !important;
    }

    /* Bikin Sidebar Jadi Tipis & Gak Makan Tempat */
    section[data-testid="stSidebar"] {
        width: 250px !important;
        background-color: #111 !important;
    }

    /* Header Apex */
    .header-apex {
        color: #FF0000; font-size: 2rem; font-weight: 900;
        text-align: center; margin-bottom: 2rem;
    }

    /* Input Bar Ramping & Tombol Send Dekat */
    div[data-testid="stChatInput"] {
        position: fixed; bottom: 20px;
        left: 50%; transform: translateX(-50%);
        width: 95% !important; max-width: 600px !important;
        border-radius: 30px !important;
        background-color: #1A1A1A !important;
        border: 1px solid #333 !important;
    }

    /* Sembunyikan Elemen Gangguan */
    footer, header, [data-testid="stHeader"] { visibility: hidden; position: absolute; }
    
    .thought-box { background: #111; border-left: 3px solid #FF0000; padding: 10px; color: #888; font-size: 0.85rem; }
    </style>
    <div class="header-apex">APEXMINI</div>
""", unsafe_allow_html=True)

# --- 4. SESSION & DISPLAY ---
if "messages" not in st.session_state: st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if m.get("thought"):
            with st.expander("Reasoning"):
                st.markdown(f"<div class='thought-box'>{m['thought']}</div>", unsafe_allow_html=True)
        st.markdown(m["content"])
        if m.get("gen_img"): st.image(m["gen_img"])

# --- 5. INPUT & MEDIA ---
with st.sidebar:
    st.markdown("### 📎 MEDIA")
    up = st.file_uploader("Upload", type=['png','jpg','jpeg'], accept_multiple_files=True, label_visibility="collapsed")

if prompt := st.chat_input("Ketik perintah... (↩️ Spasi/Enter)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        thought, ans = get_r1_response(prompt)
        if thought:
            with st.expander("Thinking...", expanded=True):
                st.markdown(f"<div class='thought-box'>{thought}</div>", unsafe_allow_html=True)
        st.markdown(ans)
        
        img = None
        if any(w in prompt.lower() for w in ["buat", "gambar", "visual"]):
            with st.spinner("Pony V6 Rendering..."):
                img = generate_pony(ans)
                if img: st.image(img)
        
        st.session_state.messages.append({"role": "assistant", "content": ans, "thought": thought, "gen_img": img})
    st.rerun()

