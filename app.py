import streamlit as st
import requests
from PIL import Image

# --- 1. CORE AUTHENTICATION ---
try:
    API_TOKEN = st.secrets["GITHUB_TOKEN"]
    TEXT_MODEL = "https://models.inference.ai.azure.com/chat/completions"
    VISUAL_ENGINE = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
except Exception:
    st.error("Authentication Error: GITHUB_TOKEN missing.")
    st.stop()

# --- 2. ENGINE LOGIC (STRICT & PRECISE) ---
def get_text_response(prompt):
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "messages": [
            {
                "role": "system", 
                "content": "You are ApexMini. Answer in Indonesian. If the user requests a visual, generate a high-detail English descriptive prompt for the image engine. Output the final answer only, hide <think> tags."
            },
            {"role": "user", "content": prompt}
        ],
        "model": "DeepSeek-R1", 
        "temperature": 0.6
    }
    try:
        response = requests.post(TEXT_MODEL, headers=headers, json=payload, timeout=30)
        res = response.json()['choices'][0]['message']['content']
        return res.split("</think>")[-1].strip() if "</think>" in res else res
    except:
        return "System Error: Failed to process text logic."

def generate_visual_now(refined_prompt):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    try:
        response = requests.post(VISUAL_ENGINE, headers=headers, json={"inputs": refined_prompt}, timeout=120)
        return response.content if response.status_code == 200 else None
    except:
        return None

# --- 3. UI LAYOUT (COMPACT DARK MODE) ---
st.set_page_config(page_title="ApexMini", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    .main .block-container { padding-top: 0.5rem !important; max-width: 750px !important; }
    .header-apex { color: #FF0000; font-size: 2.2rem; font-weight: 900; text-align: center; margin-bottom: 10px; padding-top: 5px; letter-spacing: 2px; }
    footer, header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    .stChatMessage { background-color: transparent !important; margin-top: -20px !important; }
    .chat-text { text-align: center; font-size: 1.1rem; }
    .stSpinner > div { border-top-color: #FF0000 !important; width: 40px !important; height: 40px !important; }
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
        st.markdown(f"<div class='chat-text'>{m['content']}</div>", unsafe_allow_html=True)
        if "generated_img" in m:
            st.image(m["generated_img"], use_container_width=True)

# --- 6. INPUT AREA (SIDE-BY-SIDE) ---
c1, c2 = st.columns([0.15, 0.85])
with c1:
    up_files = st.file_uploader("📎", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True, label_visibility="collapsed")
with c2:
    prompt = st.chat_input("Enter command...")

if prompt:
    user_entry = {"role": "user", "content": prompt}
    if up_files:
        user_entry["images"] = [Image.open(f) for f in up_files]
    st.session_state.messages.append(user_entry)
    
    with st.chat_message("assistant"):
        # Process Logic
        ans = get_text_response(prompt)
        st.markdown(f"<div class='chat-text'>{ans}</div>", unsafe_allow_html=True)
        
        # Process Visual
        gen_img = None
        if any(w in prompt.lower() for w in ["buat", "gambar", "visual", "generate", "render"]):
            with st.spinner("Processing visual..."):
                gen_img = generate_visual_now(ans)
                if gen_img:
                    st.image(gen_img, use_container_width=True)
        
        asst_entry = {"role": "assistant", "content": ans}
        if gen_img: asst_entry["generated_img"] = gen_img
        st.session_state.messages.append(asst_entry)
    
    st.rerun()


