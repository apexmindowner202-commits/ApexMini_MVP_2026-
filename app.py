import streamlit as st
import requests
from PIL import Image
import io
import time

# --- 1. OTENTIKASI SAKTI ---
try:
    API_TOKEN = st.secrets["GITHUB_TOKEN"]
    TEXT_MODEL = "https://models.inference.ai.azure.com/chat/completions"
    IMAGE_MODEL = "https://api-inference.huggingface.co/models/Lykon/Pony-Diffusion-V6-XL"
except Exception:
    st.error("TOKEN GITHUB TIDAK DITEMUKAN!")
    st.stop()

# --- 2. ENGINE DEEPSEEK-R1 (CHAIN-OF-THOUGHT) ---
def get_apex_response(user_input, has_images=False):
    headers = {"Authorization": f"Bearer {API_TOKEN.strip()}", "Content-Type": "application/json"}
    
    # Perintah paksa agar R1 menganalisis input + foto
    sys_prompt = "You are ApexMini. You must use Chain-of-Thought reasoning. "
    if has_images:
        sys_prompt += "User has uploaded images. Incorporate deep image analysis in your reasoning and final response. "
    sys_prompt += "Answer in Indonesian, stay sharp and precise."

    payload = {
        "messages": [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_input}
        ],
        "model": "DeepSeek-R1",
        "temperature": 0.6
    }
    
    for _ in range(3): # Anti-Error 429
        try:
            res = requests.post(TEXT_MODEL, headers=headers, json=payload, timeout=60)
            if res.status_code == 200:
                full_content = res.json()['choices'][0]['message']['content']
                # EKSTRAKSI CoT (Melihat cara mikir R1)
                if "</think>" in full_content:
                    parts = full_content.split("</think>")
                    return parts[0].replace("<think>", "").strip(), parts[1].strip()
                return None, full_content
            elif res.status_code == 429:
                time.sleep(2); continue
        except: continue
    return None, "Koneksi sibuk. Ulangi."

# --- 3. UI STYLE (RAMPING & PROFESIONAL) ---
st.set_page_config(page_title="ApexMini", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #050505 !important; }
    
    /* INPUT BAR RAMPING TENGAH */
    div[data-testid="stChatInput"] {
        position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%);
        width: 90% !important; max-width: 550px !important;
        background: #111 !important; border: 1px solid #333 !important;
        border-radius: 20px !important;
    }
    
    footer, header, [data-testid="stHeader"] { visibility: hidden; }
    .hero { text-align: center; padding: 40px 0; }
    .hero h1 { color: #FF0000; font-size: 3rem; font-weight: 900; letter-spacing: 5px; }
    .cot-box { background: #0A0A0A; border-left: 3px solid #FF0000; padding: 15px; color: #777; font-size: 0.85rem; }
    </style>
""", unsafe_allow_html=True)

# --- 4. SESSION & MEDIA ---
if "messages" not in st.session_state: st.session_state.messages = []
if "uploader_id" not in st.session_state: st.session_state.uploader_id = 0

with st.sidebar:
    st.markdown("### 📎 MEDIA ATTACHMENT")
    up_files = st.file_uploader("Upload Foto", type=['png','jpg','jpeg'], 
                                accept_multiple_files=True, 
                                key=f"up_{st.session_state.uploader_id}")
    if up_files:
        if st.button("❌ Batal / Hapus"):
            st.session_state.uploader_id += 1; st.rerun()

# --- 5. CHAT DISPLAY ---
if not st.session_state.messages:
    st.markdown('<div class="hero"><h1>APEXMINI</h1></div>', unsafe_allow_html=True)

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if "imgs" in m:
            for i in m["imgs"]: st.image(i, width=300)
        if m.get("cot"):
            with st.expander("Internal Reasoning (CoT)"):
                st.markdown(f'<div class="cot-box">{m["cot"]}</div>', unsafe_allow_html=True)
        st.markdown(m["content"])
        if m.get("v_res"): st.image(m["v_res"], use_container_width=True)

# --- 6. ACTION (PROSES TAJAM) ---
if prompt := st.chat_input("Tanya ApexMini..."):
    # Deteksi Foto
    has_img = True if up_files else False
    current_imgs = [Image.open(f) for f in up_files] if up_files else []
    
    st.session_state.messages.append({"role": "user", "content": prompt, "imgs": current_imgs})
    
    with st.chat_message("assistant"):
        with st.spinner("Berpikir Mendalam..."):
            # EXEC R1 CoT
            cot_logic, final_ans = get_apex_response(prompt, has_images=has_img)
            
            if cot_logic:
                with st.expander("Thinking...", expanded=True):
                    st.markdown(f'<div class="cot-box">{cot_logic}</div>', unsafe_allow_html=True)
            st.markdown(final_ans)
        
        # Simpan History
        st.session_state.messages.append({"role": "assistant", "content": final_ans, "cot": cot_logic})
        st.session_state.uploader_id += 1 # Reset uploader otomatis
    st.rerun()
