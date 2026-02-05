import streamlit as st
import requests
from PIL import Image
import io
import time

# --- 1. CORE AUTH (SISTEM TOLARANSI TINGGI) ---
try:
    API_TOKEN = st.secrets["GITHUB_TOKEN"]
    TEXT_MODEL = "https://models.inference.ai.azure.com/chat/completions"
    IMAGE_MODEL = "https://api-inference.huggingface.co/models/Lykon/Pony-Diffusion-V6-XL"
except Exception:
    st.error("TOKEN GHOIB! PASANG DI SECRETS!")
    st.stop()

# --- 2. ENGINE LOGIC: DEEPSEEK-R1 (COT) DENGAN SISTEM ANTI-BLOCK ---
def get_apex_logic(u_input, has_img=False):
    headers = {"Authorization": f"Bearer {API_TOKEN.strip()}", "Content-Type": "application/json"}
    
    # Perintah Tajam & Fokus Proyek
    sys_msg = "You are ApexMini. Project focused. Sharp instinct. Strictly use Chain-of-Thought reasoning. Indonesian."
    if has_img:
        sys_msg += " Analyze the attached images for the project formulation."

    payload = {
        "messages": [{"role": "system", "content": sys_msg}, {"role": "user", "content": u_input}],
        "model": "DeepSeek-R1", "temperature": 0.6
    }
    
    # Teknik Brutal: Retry sampai 5 kali untuk tembus Rate Limit
    for attempt in range(5):
        try:
            res = requests.post(TEXT_MODEL, headers=headers, json=payload, timeout=60)
            if res.status_code == 200:
                full = res.json()['choices'][0]['message']['content']
                if "</think>" in full:
                    p = full.split("</think>")
                    return p[0].replace("<think>", "").strip(), p[1].strip()
                return None, full
            elif res.status_code == 429:
                time.sleep(attempt + 1) # Jeda makin lama tiap gagal
                continue
        except: continue
    return None, "Sistem GitHub Limit (429). Tunggu 10 detik lalu kirim ulang."

def generate_apex_visual(p):
    headers = {"Authorization": f"Bearer {API_TOKEN.strip()}"}
    try:
        # Tambahkan quality tag agar tidak berantakan
        res = requests.post(IMAGE_MODEL, headers=headers, 
                            json={"inputs": f"score_9, score_8_up, masterpiece, detailed, {p}"}, timeout=120)
        return res.content if res.status_code == 200 else None
    except: return None

# --- 3. UI STYLE: BLACK & RED (RAMPING & STABIL) ---
st.set_page_config(page_title="ApexMini", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #050505 !important; }
    div[data-testid="stChatInput"] {
        position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%);
        width: 90% !important; max-width: 500px !important;
        background: #111 !important; border: 1px solid #333 !important;
        border-radius: 20px !important;
    }
    footer, header, [data-testid="stHeader"] { visibility: hidden; }
    .hero { text-align: center; padding: 20px 0; border-bottom: 2px solid #FF0000; margin-bottom: 30px; }
    .hero h1 { color: #FF0000; font-size: 2.5rem; font-weight: 900; letter-spacing: 5px; margin: 0; }
    .cot-box { background: #0A0A0A; border-left: 3px solid #FF0000; padding: 15px; color: #888; font-size: 0.85rem; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. SESSION & MEDIA CONTROL ---
if "messages" not in st.session_state: st.session_state.messages = []
if "up_key" not in st.session_state: st.session_state.up_key = 0

with st.sidebar:
    st.markdown("### 📎 PROJECT MEDIA")
    files = st.file_uploader("Upload Foto Proyek", type=['png','jpg','jpeg'], 
                             accept_multiple_files=True, key=f"f_{st.session_state.up_key}")
    if files:
        if st.button("🗑️ Reset Media"):
            st.session_state.up_key += 1; st.rerun()

# --- 5. CHAT DISPLAY (SISTEM LINEAR - ANTI CRASH) ---
st.markdown('<div class="hero"><h1>APEXMINI</h1></div>', unsafe_allow_html=True)

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        # Tampilkan foto user secara vertikal (Anti Column-Error)
        if "imgs" in m:
            for img in m["imgs"]: st.image(img, width=280)
        
        # Tampilkan CoT DeepSeek-R1
        if m.get("cot"):
            with st.expander("Proses Berpikir (CoT)", expanded=False):
                st.markdown(f'<div class="cot-box">{m["cot"]}</div>', unsafe_allow_html=True)
        
        st.markdown(m["content"])
        
        # Tampilkan Visual Proyek
        if m.get("v_res"):
            st.image(m["v_res"], caption="Hasil Visual Proyek", use_container_width=True)

# --- 6. ACTION (FULL POWER) ---
if prompt := st.chat_input("Tanya ApexMini..."):
    has_img = True if files else False
    # Pre-process image to avoid rerun issues
    curr_imgs = [Image.open(f) for f in files] if files else []
    
    st.session_state.messages.append({"role": "user", "content": prompt, "imgs": curr_imgs})
    
    with st.chat_message("assistant"):
        with st.spinner("ApexMini sedang merumuskan..."):
            cot, ans = get_apex_logic(prompt, has_img=has_img)
            
            if cot:
                with st.expander("Thinking...", expanded=True):
                    st.markdown(f'<div class="cot-box">{cot}</div>', unsafe_allow_html=True)
            st.markdown(ans)
        
        v_data = None
        if any(x in prompt.lower() for x in ["buat", "gambar", "visual", "render"]):
            with st.status("🚀 Merender Visual Proyek...", expanded=True) as status:
                v_data = generate_apex_visual(ans)
                if v_data:
                    st.image(v_data, use_container_width=True)
                    status.update(label="Visual Selesai!", state="complete")
                else: status.update(label="Gagal Render", state="error")
        
        st.session_state.messages.append({"role": "assistant", "content": ans, "cot": cot, "v_res": v_data})
        st.session_state.up_key += 1 # Auto reset uploader
    st.rerun()
