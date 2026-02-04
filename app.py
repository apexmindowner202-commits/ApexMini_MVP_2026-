import streamlit as st
import requests

# --- 1. CORE CONFIGURATION ---
try:
    API_TOKEN = st.secrets["GITHUB_TOKEN"]
    ENDPOINT = "https://models.inference.ai.azure.com/chat/completions"
except Exception:
    st.error("Authentication Error: GITHUB_TOKEN not configured.")
    st.stop()

# --- 2. ENGINE LOGIC (DEEPSEEK R1) ---
def execute_apexmini(user_input):
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "messages": [
            {"role": "system", "content": "You are ApexMini. Precise, professional AI. Identity: Open Source Community Project."},
            {"role": "user", "content": user_input}
        ],
        "model": "DeepSeek-R1",
        "temperature": 0.6
    }
    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload, timeout=30)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"System Error: {str(e)}"

# --- 3. UI DESIGN (DARK APEX) ---
st.set_page_config(page_title="ApexMini", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    .header-apexmini { color: #FF0000; font-size: 2.5rem; font-weight: 800; text-align: center; padding: 50px 0; letter-spacing: 2px; }
    footer, header {visibility: hidden;}
    .stChatMessage { background-color: #111111; border: 1px solid #222; border-radius: 10px; }
    </style>
    <div class="header-apexmini">APEXMINI</div>
""", unsafe_allow_html=True)

# --- 4. CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Enter formula or prompt..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        res = execute_apexmini(prompt)
        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})    



