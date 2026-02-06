import streamlit as st
import requests

# 1. IDENTITAS APEXMINI (WAJIB MERAH & TEGAS)
st.set_page_config(page_title="ApexMini", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .apex-title { color: #FF0000; font-size: 40px; font-weight: 900; letter-spacing: 2px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="apex-title">ApexMini</h1>', unsafe_allow_html=True)

# 2. FITUR UPLOAD FOTO (YANG TADI HILANG)
with st.sidebar:
    st.markdown("<h2 style='color:white;'>📂 PROJECT ASSETS</h2>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Lampirkan foto proyek...", accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            st.image(file, caption=file.name, width=200)

# 3. KONEKSI KE DEEPSEEK-R1 & PONY V6 XL
TOKEN = st.secrets["GITHUB_TOKEN"]

def get_apex_response(prompt):
    url = "https://models.inference.ai.azure.com/chat/completions"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    # Identitas Komunitas Open Source (Sesuai Pesanan Maestro)
    payload = {
        "messages": [
            {"role": "system", "content": "Identity: Open Source Community. Focus: High-level coding & visual logic. No reasoning output."},
            {"role": "user", "content": prompt}
        ],
        "model": "deepseek-r1" # Logika R1 CoT
    }
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=60)
        return res.json()['choices'][0]['message']['content'].split("</think>")[-1].strip()
    except:
        return "⚠️ Sistem Sembelit/Limit. Tunggu 10 detik."

# 4. CHAT INTERFACE (SESUAI VIDEO VS CODE)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ketik rumusan atau instruksi visual...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        response = get_apex_response(user_input)
        st.write(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
