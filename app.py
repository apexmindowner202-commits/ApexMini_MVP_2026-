import streamlit as st
import requests
import json
import base64
from io import BytesIO
from PIL import Image  # pip install pillow

st.title("Chatbot OpenRouter + Edit Foto Independen")

try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
    st.success("API key OK! ✅")
except KeyError:
    st.error("API key gak kebaca. Cek Secrets.")
    st.stop()

# Sidebar untuk pilih model multimodal
model = st.sidebar.selectbox("Pilih Model (untuk edit foto pakai multimodal)", [
    "black-forest-labs/flux.2-pro", 
    "black-forest-labs/flux.2-flex",
    "google/gemini-3-pro-image-preview",  # atau yang tersedia di openrouter.ai/models
    "meta-llama/llama-3.3-70b-instruct"   # fallback text-only
])

# Init messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan history (text + gambar kalau ada)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if isinstance(msg["content"], str):
            st.markdown(msg["content"])
        elif isinstance(msg["content"], list):  # untuk multimodal
            for part in msg["content"]:
                if part["type"] == "text":
                    st.markdown(part["text"])
                elif part["type"] == "image_url":
                    st.image(part["image_url"]["url"])

# Upload foto untuk edit
uploaded_file = st.file_uploader("Upload foto untuk di-edit (opsional)", type=["jpg", "png", "jpeg"])
image_base64 = None
if uploaded_file:
    img = Image.open(uploaded_file)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    st.image(img, caption="Foto yang diupload", width=300)

if prompt := st.chat_input("Ketik prompt (misal: 'edit foto ini jadi hitam putih' atau chat biasa)"):
    # Bangun messages baru
    user_content = [{"type": "text", "text": prompt}]
    if image_base64:
        user_content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{image_base64}"}
        })
    
    st.session_state.messages.append({"role": "user", "content": user_content})
    
    with st.chat_message("user"):
        st.markdown(prompt)
        if image_base64:
            st.image(uploaded_file, width=200)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""
        generated_images = []

        payload = {
            "model": model,
            "messages": st.session_state.messages,
            "stream": True,
            "temperature": 0.7
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://your-streamlit-app.com",
            "X-Title": "Foto Edit Chatbot"
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
                            delta = chunk['choices'][0]['delta']
                            # Text content
                            if 'content' in delta:
                                content = delta['content']
                                full_text += content
                                placeholder.markdown(full_text + "▌")
                            # Image generation (kalau model support)
                            if 'images' in delta and delta['images']:
                                for img_data in delta['images']:
                                    if 'url' in img_data:
                                        generated_images.append(img_data['url'])
                                        st.image(img_data['url'], caption="Hasil edit/generate")
                        except:
                            pass
            placeholder.markdown(full_text)
            # Simpan images kalau ada
            if generated_images:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_text,
                    "images": generated_images  # optional simpan
                })
            else:
                st.session_state.messages.append({"role": "assistant", "content": full_text})



