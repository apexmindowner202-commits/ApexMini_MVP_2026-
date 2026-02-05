import streamlit as st
import requests

# --- STANDAR UI INTERNASIONAL (APEXMINI) ---
st.set_page_config(
    page_title="ApexMini - Project Intelligence",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS Profesional: Lebar Pas, Send Button Kanan, Clean Interface
st.markdown("""
    <style>
    .block-container {max-width: 850px; padding-top: 2rem;}
    .stTextInput input {border-radius: 10px; border: 1px solid #d1d1e9;}
    section[data-testid="stSidebar"] {width: 300px !important;}
    .stChatFloatingInputContainer {background-color: transparent;}
    /* Warna Hijau ChatGPT untuk Tombol Kirim */
    div.stButton > button {
        background-color: #10a37f;
        color: white;
        border-radius: 5px;
        width: 100%;
        font-weight: bold;
    }
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER PROYEK ---
st.title("ApexMini")
st.caption("Advanced CoT Reasoning | DeepSeek-R1 | Pony V6 XL Logic")

# --- KONEKSI TOKEN GITHUB (POWERED BY GITHUB MODELS) ---
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", "")

# --- FITUR MULTI-UPLOAD FOTO (ANTI-KORUPSI) ---
# Ditempatkan di area utama agar tidak terpotong sistem Streamlit
with st.expander("📂 Lampirkan Aset/Foto Proyek", expanded=True):
    uploaded_files = st.file_uploader(
        "Upload beberapa foto untuk analisis visual", 
        accept_multiple_files=True, 
        type=['png', 'jpg', 'jpeg'],
        key="apex_uploader"
    )

# --- ENGINE PENALARAN (DEEPSEEK R1 - CoT) ---
def get_apexmini_logic(user_input):
    if not GITHUB_TOKEN:
        st.error("Sistem Error: GITHUB_TOKEN tidak terdeteksi di Secrets.")
        return None
    
    url = "https://models.inference.ai.azure.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "DeepSeek-R1",
        "messages": [
            {
                "role": "system", 
                "content": (
                    "You are ApexMini. Execute advanced Chain-of-Thought (CoT) reasoning. "
                    "Focus on complex mathematical formulations and high-precision project analysis. "
                    "Maintain professional, sharp, and concise output. No conversational filler. "
                    "Address the user's intent directly with expert-level technical accuracy."
                )
            },
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.6
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"API Error: {str(e)}"

# --- ENGINE VISUAL (PONY V6 XL LOGIC VIA SDXL) ---
def generate_pony_visual(refined_prompt):
    url = "https://models.inference.ai.azure.com/images/generations"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Pony V6 XL Style Prompting: Garis Keras & Fotorealistik
    enhanced_prompt = f"score_9, score_8_up, masterpiece, photorealistic, 8k resolution, highly detailed, {refined_prompt}"
    
    payload = {
        "model": "stability-ai/sdxl",
        "prompt": enhanced_prompt,
        "n": 1,
        "size": "1024x1024"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()['data'][0]['url']
    except Exception as e:
        return None

# --- MANAJEMEN CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- INPUT & EKSEKUSI ---
if prompt := st.chat_input("Input rumusan proyek..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Tahap 1: Penalaran Mendalam (CoT)
        with st.spinner("ApexMini Analyzing..."):
            reasoning_output = get_apexmini_logic(prompt)
            if reasoning_output:
                st.markdown(reasoning_output)
                st.session_state.messages.append({"role": "assistant", "content": reasoning_output})
                
                # Tahap 2: Eksekusi Visual (Jika Relevan)
                visual_triggers = ['visual', 'gambar', 'render', 'foto', 'desain']
                if any(x in prompt.lower() for x in visual_triggers):
                    with st.spinner("Generating Pony V6 XL Visual..."):
                        image_url = generate_pony_visual(reasoning_output[:400])
                        if image_url:
                            st.image(image_url, caption="ApexMini Visual Output | Photorealistic Engine")
