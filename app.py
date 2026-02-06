import streamlit as st
import requests
from PIL import Image
import io

# IDENTITAS VISUAL (WAJIB MERAH)
st.set_page_config(page_title="ApexMini", layout="wide")
st.markdown("<style>.stMarkdown h1 {color: #FF0000 !important; font-weight: 900;}</style>", unsafe_allow_html=True)
st.title("ApexMini")

# HANDLING ASSETS TANPA ERROR
with st.sidebar:
    st.header("ASET PROYEK")
    uploaded_files = st.file_uploader("Lampirkan foto...", accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            try:
                # Memastikan file dibaca dengan benar sebagai gambar
                img = Image.open(file)
                st.image(img, caption=file.name, use_container_width=True)
            except Exception:
                st.error(f"Format file {file.name} tidak didukung.")

# LOGIKA EKSEKUSI
TOKEN = st.secrets.get("GITHUB_TOKEN", "")

def process(msg):
    url = "https://models.inference.ai.azure.com/chat/completions"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    payload = {
        "messages": [
            {"role": "system", "content": "Identity: Open Source Community. Fast, Sharp, No Small Talk. Focus on Code and Visual Prompts."},
            {"role": "user", "content": msg}
        ],
        "model": "deepseek-r1"
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=60)
        return r.json()['choices'][0]['message']['content'].split("</think>")[-1].strip()
    except:
        return "System error."

# CHAT INTERFACE
if "messages" not in st.session_state: st.session_state.messages = []
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.write(m["content"])

query = st.chat_input("Ketik instruksi...")
if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"): st.write(query)
    with st.chat_message("assistant"):
        resp = process(query)
        st.write(resp)
        st.session_state.messages.append({"role": "assistant", "content": resp})
