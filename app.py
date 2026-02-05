import streamlit as st
import requests
from PIL import Image
import io

# --- 1. SAKLAR BRANKAS ---
try:
    API_TOKEN = st.secrets["GITHUB_TOKEN"]
    R1_URL = "https://models.inference.ai.azure.com/chat/completions"
    PONY_URL = "https://api-inference.huggingface.co/models/Lykon/Pony-Diffusion-V6-XL"
except Exception:
    st.error("Token GITHUB_TOKEN tidak ditemukan di Secrets!")
    st.stop()

# --- 2. ENGINE LOGIC (R1 + CoT) ---
def get_r1_response(user_input):
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "messages": [
            {"role": "system", "content": "You are ApexMini R1. Always use Chain-of-Thought reasoning. Final answer in Indonesian. For visuals, create high-quality Pony Diffusion V6 XL prompts (score_9, score_8_up, rating_explicit)."},
            {"role": "user", "content": user_input}
        ],
        "model": "DeepSeek-R1", "temperature": 0.6
    }
    try:
        response = requests.post(R1_URL, headers=headers, json=payload, timeout=60)
        if response.status_code == 200:
            full_res = response.json()['choices'][0]['message']['content']
            if "</think>" in full_res:
                parts = full_res.split("</think>")
                return parts[0].replace("<think>", "").strip(), parts[1].strip()
            return None, full_res
        elif response.status_code == 429: return None, "LIMIT"
        return None, f"Error: {response.status_code}"
    except: return None, "OFFLINE"

def generate_pony_visual(prompt_desc):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    p_input = f"score_9, score_8_up, score_7_up, rating_explicit, {prompt_desc}"
    try:
        res = requests.post(PONY_URL, headers=headers, json={"inputs": p_input}, timeout=120)
        return res.content if res.status_code == 200 else None
    except: return None

# --- 3. UI LAYOUT (RESPONSIVE & COMPACT) ---
st.set_page_config(page_title="ApexMini Pro", layout="centered") # Kunci di tengah agar tidak melar

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    .header-title { color: #FF0000; font-size: 1.8rem; font-weight: 900; text-align: center; margin-bottom: 10px; }
    
    /* Container Chat agar tidak meluas ke samping & tombol send jadi dekat */
    .main .block-container { max-width: 550px !important; padding-bottom: 150px !important; }

    /* Input Bar Melayang & Ramping (Khas Gemini/ChatGPT) */
    div[data-testid="stChatInput"] {
        position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
        width: 90% !important; max-width: 500px !important;
        border-radius: 25px !important; background-color: #1E1E1E !important;
        border: 1px solid #333 !important; z-index: 1000;
    }

    .thought-box { background: #111; border-left: 2px solid #FF0000; padding: 10px; color: #888; font-size: 0.85rem; }
    footer, header, [data-testid="stHeader"] { visibility: hidden; }
    .stChatMessage { margin-bottom: 15px !important; }
    </style>
    <div class="header-title">APEXMINI</div>
""", unsafe_allow_html=True)

# --- 4. SESSION MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 5. CHAT DISPLAY ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if m.get("thought"):
            with st.expander("Proses Berpikir (CoT)"):
                st.markdown(f"<div class='thought-box'>{m['thought']}</div>", unsafe_allow_html=True)
        st.markdown(m["content"])
        if m.get("gen_img") is not None:
            st.image(m["gen_img"], use_container_width=True)

# --- 6. INPUT & EXECUTION ---
with st.sidebar:
    st.markdown("### 📎 MEDIA")
    up_files = st.file_uploader("Upload", type=['png','jpg','jpeg'], accept_multiple_files=True, label_visibility="collapsed")

if prompt := st.chat_input("Ketik perintah... (↩️ untuk baris baru)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        thought, ans = get_r1_response(prompt)
        
        if ans == "LIMIT":
            st.warning("Limit tercapai, Maestro. Tunggu sebentar.")
        else:
            if thought:
                with st.expander("Thinking...", expanded=True):
                    st.markdown(f"<div class='thought-box'>{thought}</div>", unsafe_allow_html=True)
            st.markdown(ans)
            
            gen_img = None
            if any(w in prompt.lower() for w in ["buat", "gambar", "visual", "render"]):
                with st.spinner("Pony V6 Rendering..."):
                    gen_img = generate_pony_visual(ans)
                    if gen_img:
                        st.image(gen_img, use_container_width=True)
            
            st.session_state.messages.append({
                "role": "assistant", "content": ans, "thought": thought, "gen_img": gen_img
            })
    st.rerun()

