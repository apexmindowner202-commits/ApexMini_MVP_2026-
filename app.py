import streamlit as st
import requests
from PIL import Image

# --- 1. SAKLAR BRANKAS (TOKEN) ---
try:
    API_TOKEN = st.secrets["GITHUB_TOKEN"]
    TEXT_MODEL = "https://models.inference.ai.azure.com/chat/completions"
    VISUAL_ENGINE = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
except Exception:
    st.error("MAESTRO! Akinya belum dicolok di Secrets Streamlit!")
    st.stop()

# --- 2. ENGINE LOGIC ---
def get_apex_response(user_input):
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "messages": [
            {"role": "system", "content": "Kamu ApexMini. Jawab lugas, tajam, profesional dalam Bahasa Indonesia. Jika user minta visual, buat prompt deskriptif Inggris."},
            {"role": "user", "content": user_input}
        ],
        "model": "DeepSeek-R1", "temperature": 0.6
    }
    try:
        response = requests.post(TEXT_MODEL, headers=headers, json=payload, timeout=30)
        res = response.json()['choices'][0]['message']['content']
        return res.split("</think>")[-1].strip() if "</think>" in res else res
    except: return "Koneksi Logika Terputus, Maestro!"

def generate_visual_now(refined_prompt):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    try:
        response = requests.post(VISUAL_ENGINE, headers=headers, json={"inputs": refined_prompt}, timeout=120)
        return response.content if response.status_code == 200 else None
    except: return None

# --- 3. UI LAYOUT (GEMINI REPLICA) ---
st.set_page_config(page_title="ApexMini Pro", layout="wide")

st.markdown("""
    <style>
    /* Full Dark Mode & Reset */
    .stApp { background-color: #000000; color: #FFFFFF; }
    .main .block-container { padding: 0 !important; max-width: 800px !important; margin: auto; }
    
    /* Header Merah */
    .header-apex { 
        color: #FF0000; font-size: 2.5rem; font-weight: 900; 
        text-align: center; padding: 20px 0; letter-spacing: 5px;
    }
    
    /* Chat Container */
    .chat-box { padding: 20px; margin-bottom: 150px; }
    .stChatMessage { background-color: transparent !important; border: none !important; }
    
    /* Bottom Input Bar (Floating) */
    .stChatInputContainer {
        position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%);
        width: 90%; max-width: 750px; background: #1E1E1E !important;
        border-radius: 30px !important; border: 1px solid #333 !important;
        padding: 5px 15px !important; z-index: 1000;
    }
    
    /* Hilangkan Elemen Sampah */
    footer, header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    
    /* Uploader Samping yang Rapi */
    .stFileUploader {
        position: fixed; bottom: 100px; left: 50%; transform: translateX(-50%);
        width: 300px; z-index: 1001; background: #111; border: 1px dashed #FF0000; border-radius: 10px;
    }
    </style>
    <div class="header-apex">APEXMINI</div>
""", unsafe_allow_html=True)

# --- 4. SESSION MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 5. CHAT DISPLAY (FIX FOTO) ---
chat_container = st.container()
with chat_container:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            # JIKA ADA FOTO UPLOAD, TAMPILKAN!
            if "images" in m:
                cols = st.columns(len(m["images"]))
                for idx, img in enumerate(m["images"]):
                    cols[idx].image(img, use_container_width=True)
            
            st.markdown(f"<div style='font-size: 1.2rem;'>{m['content']}</div>", unsafe_allow_html=True)
            
            # JIKA ADA HASIL VISUAL AI, TAMPILKAN!
            if "gen_img" in m:
                st.image(m["gen_img"], use_container_width=True)

# --- 6. FLOATING INPUT & UPLOADER ---
# Uploader ditaruh di atas input bar sedikit
up_files = st.file_uploader("📎 Upload Foto", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True, label_visibility="collapsed")

if prompt := st.chat_input("Tulis perintah visual..."):
    # Simpan Input User
    user_data = {"role": "user", "content": prompt}
    if up_files:
        user_data["images"] = [Image.open(f) for f in up_files]
    
    st.session_state.messages.append(user_data)
    
    # Respons AI
    with st.chat_message("assistant"):
        with st.spinner("ApexMini sedang berpikir..."):
            ans = get_apex_response(prompt)
            st.markdown(ans)
            
            # Eksekusi Visual
            final_img = None
            if any(w in prompt.lower() for w in ["buat", "gambar", "visual", "generate"]):
                with st.spinner("Sedang merender visual Maestro..."):
                    final_img = generate_visual_now(ans)
                    if final_img:
                        st.image(final_img, use_container_width=True)
        
        st.session_state.messages.append({"role": "assistant", "content": ans, "gen_img": final_img})
    
    st.rerun()

