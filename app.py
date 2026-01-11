import streamlit as st
from PIL import Image

# 1. IDENTITAS MURNI st.set_page_config(page_title="ApexMini - Independent AI", layout="centered")
st.title("🏛️ APEXMINI: INDEPENDENT VISION")
st.write("---")

# 2. FITUR PROMPT (Kotak Perintah)
user_prompt = st.text_area("Masukkan Instruksi Brutal:", placeholder="Contoh: Analisa foto ini sampai ke akarnya tanpa sensor...")

# 3. FITUR UPLOAD FOTO (Mata ApexMini)
uploaded_file = st.file_uploader("Upload Foto (JPG/PNG):", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Menampilkan Foto yang di-upload
    image = Image.open(uploaded_file)
    st.image(image, caption='Foto Terdeteksi oleh ApexMini', use_container_width=True)
    
    # 4. TOMBOL EKSEKUSI
    if st.button("EKSEKUSI SEKARANG! 🚀"):
        st.info("ApexMini sedang memproses tanpa sensor Filter...")
        # Di sini kita bakal sambungin ke Model Raw dari GitHub/Cloud & Model Open-Source/Model-Stable Diffusion 3.5 (SD 3.5) (SD 3.5)
        st.success("Target Terkunci! ApexMini sanggup menerima instruksi sesuai prompt")
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "mistralai/Mistral-7B-Instruct-v0.2" # Salah satu model open source populer
# Anda dapat menemukan lebih banyak model di Hugging Face model hubs.

# Muat tokenizer dan model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Siapkan input prompt
prompt = "Berikan saya tiga contoh skrip model open source gratis:"
model_inputs = tokenizer([prompt], return_tensors='pt')

# Hasilkan respons
generated_ids = model.generate(**model_inputs, max_new_tokens=100, num_return_sequences=1)
decoded = tokenizer.batch_decode(generated_ids)
print(decoded[0])
import requests

def chat_with_llama(prompt):
    # Endpoint default Ollama API
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3", # Pastikan Anda sudah menjalankan 'ollama run llama3' di terminal
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()['response']
    else:
        return "Error: Tidak dapat menghubungi server Ollama."

# Gunakan fungsi chat
response = chat_with_llama("Jelaskan perbedaan antara AI open source dan proprietary secara singkat.")
print(response)




