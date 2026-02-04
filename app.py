import streamlit as st
import requests
from PIL import Image

# --- 1. CORE CONFIGURATION ---
try:
    API_TOKEN = st.secrets["GITHUB_TOKEN"]
    TEXT_MODEL = "https://models.inference.ai.azure.com/chat/completions"
    VISUAL_MODEL = "https://api-inference.huggingface.co/models/Lykon/Pony-Diffusion-V6-XL"
except Exception:
    st.error("Authentication Error: GITHUB_TOKEN tidak terdeteksi.")
    st.stop()

# --- 2. ENGINE LOGIC (PURE EXECUTION) ---
def execute_text(prompt):
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "messages": [
            {
                "role": "system", 
                "content": "Kamu ApexMini. AI profesional, tajam, dan lugas. Jawab langsung pada inti masalah dalam Bahasa Indonesia. Sembunyikan tag pemikiran (<think>). Jangan berikan informasi identitas kecuali ditanya."
            },
            {"role": "user", "content": prompt}
        ],
        "model": "DeepSeek-R1",
        "temperature": 0.6
    }
    try:
        response = requests.post(TEXT_MODEL, headers=headers, json=payload, timeout=30)
        content = response.json()['choices'][0]['message']['content']
        return content.split("</think>")[-1].strip() if "</think>" in content else content
    except: return "Koneksi terputus."

def execute_visual(description):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    try:
        response = requests.post(VISUAL_MODEL, headers=headers, json={"inputs": description}, timeout=60)
        return response.content if response.status_code == 200 else None
    except: return None

# --- 3. UI DESIGN (COMPACT DARK MODE) ---
st.set_page_config(page_title="ApexMini", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    .block-container { padding-top: 0rem !important; }
    .header-apex { color: #FF0000; font-size: 2.2rem; font-weight: 900; text-align: center; margin: 0; padding-top: 10px; }
    footer, header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    .stChatMessage { background-color: transparent !important; margin-top: -20px !important; }
    .stChatInput { border-radius: 20px !important; }
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
        st.markdown(f"<div style='text-align: center;'>{m['content']}</div>", unsafe_allow_html=True)

# --- 6. MULTI-UPLOAD & INPUT (GEMINI STYLE) ---
uploaded_files = st.file_uploader("Upload", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True, label_visibility="collapsed")

if prompt := st.chat_input("Input command..."):
    user_entry = {"role": "user", "content": prompt}
    if uploaded_files:
        user_entry["images"] = [Image.open(f) for f in uploaded_files]
    
    st.session_state.messages.append(user_entry)
    st.rerun()

# --- 7. ASSISTANT EXECUTION ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        last_input = st.session_state.messages[-1]["content"]
        
        # Eksekusi Jawaban
        ans = execute_text(last_input)
        st.markdown(f"<div style='text-align: center;'>{ans}</div>", unsafe_allow_html=True)
        
        # Eksekusi Visual Otomatis
        if any(w in last_input.lower() for w in ["buat", "gambar", "visual", "generate"]):
            img_data = execute_visual(ans)
            if img_data:
                st.image(img_data, use_container_width=True)
        
        st.session_state.messages.append({"role": "assistant", "content": ans})

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Generate data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create plot
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title("Contoh Visualisasi Sinus")
ax.set_xlabel("X")
ax.set_ylabel("sin(X)")

# Tampilkan plot di Streamlit
st.pyplot(fig)

# Download sebagai PNG
from io import BytesIO
buf = BytesIO()
fig.savefig(buf, format="png")
buf.seek(0)
st.download_button(
    label="Download Gambar",
    data=buf,
    file_name="plot_sinus.png",
    mime="image/png"
    )

