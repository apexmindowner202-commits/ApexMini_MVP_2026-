import streamlit as st
import requests
import json

st.title("Chatbot OpenRouter via Requests (No OpenAI Lib)")

try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
    st.success("API key OK! ✅")
except KeyError:
    st.error("API key gak kebaca. Cek Secrets di Cloud.")
    st.stop()

# Init messages
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ketik..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full = ""

        # Payload OpenRouter
        payload = {
            "model": "meta-llama/llama-3.3-70b-instruct",  # atau model open-source lain
            "messages": st.session_state.messages,
            "stream": True,
            "temperature": 0.7
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://your-app-url.com",  # optional, biar masuk leaderboard
            "X-Title": "My Indie Chatbot"
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            stream=True
        )

        if response.status_code != 200:
            st.error(f"Error {response.status_code}: {response.text}")
        else:
            for line in response.iter_lines():
                if line:
                    decoded = line.decode('utf-8')
                    if decoded.startswith("data: "):
                        data = decoded[6:]
                        if data == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data)
                            content = chunk['choices'][0]['delta'].get('content', '')
                            if content:
                                full += content
                                placeholder.markdown(full + "▌")
                        except:
                            pass
            placeholder.markdown(full)

    st.session_state.messages.append({"role": "assistant", "content": full})



