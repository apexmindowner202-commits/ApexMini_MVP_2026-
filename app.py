import streamlit as st
import requests
from PIL import Image
import io

# --- 1. AUTHENTICATION ---
try:
    # Mengambil akses token dari sistem secrets
    API_TOKEN = st.secrets["GITHUB_TOKEN"]
    TEXT_MODEL_URL = "https://models.inference.ai.azure.com/chat/completions"
    IMAGE_MODEL_URL = "https://api-inference.huggingface.co/models/Lykon/Pony-Diffusion-V6-XL"
except Exception:
    st.error("Error: GITHUB_TOKEN not found in Secrets.")
    st.stop()

# --- 2. CORE LOGIC ---
def get_text_response(user_input):
    headers = {
        "Authorization": f"Bearer {API_TOKEN.strip()}",
        "Content-Type": "application/json",
        "User-Agent": "ApexMini-v2"
    }
    payload = {
        "messages": [
            {"role": "system", "content": "You are ApexMini R1. Provide CoT reasoning. Answer in Indonesian. For visual requests, create detailed Pony Diffusion V6 XL prompts."},
            {"role": "user", "content": user_input}
        ],
        "model": "DeepSeek-R1",
        "temperature": 0.6
    }
    try:
        response = requests.post(TEXT_MODEL_URL, headers=headers, json=payload, timeout=60)
        if response.status_code == 200:
            result = response.json()['choices'][0]['message']['content']
            if "</think>" in result:
                parts = result.split("</think>")
                return parts[0].replace("<think>", "").strip(), parts[1].strip()
            return None, result
        elif response.status_code == 429:
            return None, "Rate limit reached. Please wait a moment."
        return None, f"API Error: {response.status_code}"
    except:
        return None, "Connection error."

def generate_image(prompt_text):
    headers = {"Authorization": f"Bearer {API_TOKEN.strip()}"}
    payload = {"inputs": f"score_9, score_8_up, {prompt_text}"}
    try:
        response = requests.post(IMAGE_MODEL_URL, headers=headers, json=payload, timeout=120)
        return response.content if response.status_code == 200 else None
    except:
        return None

# --- 3. INTERFACE CONFIGURATION ---
st.set_page_config(page_title="ApexMini", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    [data-testid="stSidebar"] { 
        position: fixed; top: 0; left: 0; z-index: 9999;
        background-color: rgba(0,0,0,0.95) !important; width: 280px !important;
    }
    .hero-container { text-align: center; padding: 60px 0; }
    .hero-title { color: #FF0000; font-size: 3rem; font-weight: 900; letter-spacing: 4px; }
    .hero-desc { color: #666; font-size: 1.1rem; }
    
    div[data-testid="stChatInput"] {
        position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%);
        width: 95% !important; max-width: 650px !important;
        border-radius: 30px !important; background: #1A1A1A !important;
        border: 1px solid #333 !important;
    }
    footer, header, [data-testid="stHeader"] { visibility: hidden; position: absolute; }
    .thought-container { background: #111; border-left: 3px solid #FF0000; padding: 15px; color: #999; font-size: 0.9rem; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. INITIAL VIEW ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    st.markdown("""
        <div class="hero-container">
            <div class="hero-title">APEXMINI</div>
            <p class="hero-desc">Powered by DeepSeek-R1 & Pony V6 XL</p>
            <p style="color:#444;">Tanyakan apa saja...</p>
        </div>
    """, unsafe_allow_html=True)

# --- 5. CHAT HISTORY ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("thought"):
            with st.expander("Reasoning Process"):
                st.markdown(f"<div class='thought-container'>{msg['thought']}</div>", unsafe_allow_html=True)
        st.markdown(msg["content"])
        if msg.get("image"):
            st.image(msg["image"], use_container_width=True)

# --- 6. ATTACHMENT ---
with st.sidebar:
    st.markdown("### Media Upload")
    files = st.file_uploader("Upload images", type=['png','jpg','jpeg'], accept_multiple_files=True)

# --- 7. EXECUTION ---
if user_query := st.chat_input("Tanya ApexMini..."):
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    with st.chat_message("assistant"):
        thought, answer = get_text_response(user_query)
        
        if thought:
            with st.expander("Thinking...", expanded=True):
                st.markdown(f"<div class='thought-container'>{thought}</div>", unsafe_allow_html=True)
        
        st.markdown(answer)
        
        img_data = None
        if any(keyword in user_query.lower() for keyword in ["buat", "gambar", "visual", "render", "generate"]):
            with st.spinner("Generating Visual..."):
                img_data = generate_image(answer)
                if img_data:
                    st.image(img_data, use_container_width=True)
                else:
                    st.error("Visual generation failed.")
        
        st.session_state.messages.append({
            "role": "assistant", 
            "content": answer, 
            "thought": thought, 
            "image": img_data
        })
    st.rerun()

