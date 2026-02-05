import streamlit as st
import requests
from PIL import Image
import io
import time

# --- 1. CORE AUTH (CLEAN) ---
try:
    API_TOKEN = st.secrets["GITHUB_TOKEN"]
    TEXT_URL = "https://models.inference.ai.azure.com/chat/completions"
    PONY_URL = "https://api-inference.huggingface.co/models/Lykon/Pony-Diffusion-V6-XL"
except Exception:
    st.error("Missing GITHUB_TOKEN in Secrets!")
    st.stop()

# --- 2. ENGINE LOGIC (DENGAN RETRY OTOMATIS) ---
def get_text_response(user_input):
    headers = {"Authorization": f"Bearer {API_TOKEN.strip()}", "Content-Type": "application/json"}
    payload = {
        "messages": [
            {"role": "system", "content": "You are ApexMini. Internal reasoning only. Answer in Indonesian."},
            {"role": "user", "content": user_input}
        ],
        "model": "DeepSeek-R1", "temperature": 0.6
    }
    # Taktik Retry: Coba 3 kali kalau kena Error 429
    for attempt in range(3):
        try:
            res = requests.post(TEXT_URL, headers=headers, json=payload, timeout=60)
            if res.status_code == 200:
                full = res.json()['choices'][0]['message']['content']
                if "</think>" in full:
                    parts = full.split("</think>")
                    return parts[0].replace("<think>", "").strip(), parts[1].strip()
                return None, full
            elif res.status_code == 429:
                time.sleep(2) # Tunggu sebentar sebelum coba lagi
                continue
            return None, f"API Error: {res.status_code}"
        except: continue
    return None, "Sistem sibuk (Rate Limit). Coba lagi dalam 10 detik."

def generate_visual(p):
    headers = {"Authorization": f"Bearer {API_TOKEN.strip()}"}
    try:
        res = requests.post(PONY_URL, headers=headers, json={"inputs": f"score_9, score_8_up, {p}"}, timeout=120)
        return res.content if res.status_code == 200 else None
    except: return None

# --- 3. UI LAYOUT (CLEAN & CENTERED) ---
st.set_page_config(page_title="ApexMini", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: rgba(10,10,10,0.95) !important; width: 300px !important; }
    .hero-container { text-align: center; padding: 50px 0; }
    .hero-title { color: #FF0000; font-size: 3rem; font-weight: 900; letter-spacing: 5px; }
    div[data-testid="stChatInput"] {
        position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%);
        width: 95% !important; max-width: 650px !important;
        border-radius: 30px !important; background: #1A1A1A !important;
        border: 1px solid #333 !important;
    }
    footer, header, [data-testid="stHeader"] { visibility: hidden; position: absolute; }
    .thought-container { background: #111; border-left: 3px solid #FF0000; padding: 15px; color: #888; font-size: 0.9rem; }
    </style>
""", unsafe_allow_html=True)

# --- 4. DATA PERSISTENCE ---
if "messages" not in st.session_state: st.session_state.messages = []
if "uploader_key" not in st.session_state: st.session_state.uploader_key = 0

# --- 5. SIDEBAR: MEDIA CONTROL ---
with st.sidebar:
    st.markdown("### 📎 MEDIA CENTER")
    # Gunakan key dinamis agar bisa di-reset (batal upload)
    up_files = st.file_uploader("Upload Foto", type=['png','jpg','jpeg'], 
                                accept_multiple_files=True, 
                                key=f"up_{st.session_state.uploader_key}")
    
    if up_files:
        st.info(f"✅ {len(up_files)} Foto siap dikirim")
        if st.button("❌ Batal / Hapus Semua"):
            st.session_state.uploader_key += 1
            st.rerun()

# --- 6. DISPLAY ---
if not st.session_state.messages:
    st.markdown('<div class="hero-container"><div class="hero-title">APEXMINI</div><p style="color:#444;">Tanyakan apa saja...</p></div>', unsafe_allow_html=True)

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if "imgs" in m:
            cols = st.columns(len(m["imgs"]))
            for i, img in enumerate(m["imgs"]): cols[i].image(img)
        if m.get("thought"):
            with st.expander("Internal Reasoning"):
                st.markdown(f'<div class="thought-container">{m["thought"]}</div>', unsafe_allow_html=True)
        st.markdown(m["content"])
        if m.get("gen_img"): st.image(m.get("gen_img"), use_container_width=True)

# --- 7. INPUT & ACTION ---
if prompt := st.chat_input("Tanya ApexMini..."):
    # Proses Foto Sebelum Rerun
    current_imgs = [Image.open(f) for f in up_files] if up_files else []
    st.session_state.messages.append({"role": "user", "content": prompt, "imgs": current_imgs})
    
    with st.chat_message("assistant"):
        # Progress 1: Mikir
        with st.spinner("ApexMini sedang menganalisis..."):
            thought, ans = get_text_response(prompt)
            if thought:
                with st.expander("Analysis", expanded=True):
                    st.markdown(f'<div class="thought-container">{thought}</div>', unsafe_allow_html=True)
            st.markdown(ans)
        
        # Progress 2: Visual (Indikator Tengah)
        final_img = None
        if any(x in prompt.lower() for x in ["buat", "gambar", "visual"]):
            with st.status("🚀 Mengolah hasil visual...", expanded=True) as status:
                final_img = generate_visual(ans)
                if final_img:
                    st.image(final_img, use_container_width=True)
                    status.update(label="✅ Selesai!", state="complete")
                else:
                    status.update(label="❌ Gagal Render", state="error")
        
        st.session_state.messages.append({"role": "assistant", "content": ans, "thought": thought, "gen_img": final_img})
        # Reset Uploader setelah kirim
        st.session_state.uploader_key += 1
    st.rerun()
