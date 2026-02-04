import streamlit as st
import requests
from PIL import Image
import io

# --- 1. CORE AUTHENTICATION ---
try:
    API_TOKEN = st.secrets["GITHUB_TOKEN"]
    R1_URL = "https://models.inference.ai.azure.com/chat/completions"
    PONY_URL = "https://api-inference.huggingface.co/models/Lykon/Pony-Diffusion-V6-XL"
except Exception:
    st.error("Authentication Error: Token missing in Secrets.")
    st.stop()

# --- 2. DEEPSEEK-R1 ENGINE (WITH VISIBLE CoT) ---
def get_r1_response(user_input):
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "messages": [
            {
                "role": "system", 
                "content": "You are ApexMini. Driven by DeepSeek-R1 with Chain-of-Thought (CoT). Always show your reasoning clearly. For visuals, create high-tier Pony Diffusion V6 XL prompts (score_9, score_8_up, rating_explicit). Answer in Indonesian."
            },
            {"role": "user", "content": user_input}
        ],
        "model": "DeepSeek-R1",
        "temperature": 0.7
    }
    try:
        response = requests.post(R1_URL, headers=headers, json=payload, timeout=60)
        if response.status_code == 200:
            full_res = response.json()['choices'][0]['message']['content']
            
            # Memisahkan CoT (Think) dan Answer
            if "</think>" in full_res:
                parts = full_res.split("</think>")
                thought = parts[0].replace("<think>", "").strip()
                answer = parts[1].strip()
                return thought, answer
            return None, full_res
        return None, f"Error: {response.status_code}"
    except:
        return None, "Connection Lost."

# --- 3. PONY V6 XL VISUAL ENGINE ---
def generate_pony(prompt_desc):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    payload = {"inputs": f"score_9, score_8_up, score_7_up, rating_explicit, {prompt_desc}"}
    try:
        response = requests.post(PONY_URL, headers=headers, json=payload, timeout=120)
        return response.content if response.status_code == 200 else None
    except:
        return None

# --- 4. UI LAYOUT (CLEAN & CENTERED) ---
st.set_page_config(page_title="ApexMini Pro", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    .main .block-container { padding: 1rem !important; max-width: 800px !important; margin: auto; }
    .header-title { color: #FF0000; font-size: 2.2rem; font-weight: 900; text-align: center; margin-bottom: 1rem; }
    .thought-process { background-color: #1A1A1A; border-left: 3px solid #FF0000; padding: 10px; font-style: italic; color: #AAAAAA; font-size: 0.9rem; margin-bottom: 10px; }
    footer, header, [data-testid="stHeader"] { visibility: hidden; }
    </style>
    <div class="header-title">APEXMINI</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 5. CHAT DISPLAY ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if "thought" in m and m["thought"]:
            with st.expander("Lihat Proses Berpikir (CoT)..."):
                st.markdown(f"<div class='thought-process'>{m['thought']}</div>", unsafe_allow_html=True)
        st.markdown(m["content"])
        if "gen_img" in m:
            st.image(m["gen_img"], use_container_width=True)

# --- 6. INPUT AREA ---
with st.sidebar:
    st.write("### APEXMINI VVIP")
    up_files = st.file_uploader("Lampiran", type=['png','jpg','jpeg'], accept_multiple_files=True)

if prompt := st.chat_input("Input command..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        # STEP 1: R1 + CoT
        with st.spinner("R1 sedang menalar (CoT)..."):
            thought, ans = get_r1_response(prompt)
            
            if thought:
                with st.expander("Proses Berpikir Berhasil...", expanded=True):
                    st.markdown(f"<div class='thought-process'>{thought}</div>", unsafe_allow_html=True)
            
            st.markdown(ans)
            
            # STEP 2: PONY RENDER
            gen_img = None
            if any(w in prompt.lower() for w in ["buat", "gambar", "visual", "render"]):
                with st.spinner("Pony V6 sedang merender..."):
                    gen_img = generate_pony(ans)
                    if gen_img:
                        st.image(gen_img, use_container_width=True)
        
        st.session_state.messages.append({"role": "assistant", "content": ans, "thought": thought, "gen_img": gen_img})
    
    st.rerun()

