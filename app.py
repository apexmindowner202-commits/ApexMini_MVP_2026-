import streamlit as st
import streamlit_authenticator as stauth

# --- MARKAS BESAR APEXMINI 2026 (REVISI TOTAL) ---
st.set_page_config(page_title="ApexMini Visual Markas", page_icon="🛡️", layout="wide")

nama_pengguna = ['maestro']
kata_sandi = ['ApexMini2026']
sandi_hash = ['$2b$12$6k5YF.C1jDRErM9W3fXpA.mE8M6hL6E5vV6y5f5Y5f5Y5f5Y5f5Y5'] 

konfigurasi = {
    'credentials': {'usernames': {nama_pengguna[0]: {'name': 'Pemilik Maestro', 'password': sandi_hash[0]}}},
    'cookie': {'expiry_days': 30, 'key': 'apexmini_secret', 'name': 'apexmini_auth'}
}

otentikator = stauth.Authenticate(konfigurasi['credentials'], konfigurasi['cookie']['name'], konfigurasi['cookie']['key'], konfigurasi['cookie']['expiry_days'])

try:
    nama, status, username = otentikator.login('Login Markas ApexMini', 'main')
except:
    nama, status, username = otentikator.login('main')

if status:
    otentikator.logout('Keluar Markas', 'sidebar')
    st.title(f"🛡️ Markas Visual Maestro: {nama} 🏛️")
    st.write("### Status: **NALAR DEWA & REVISI ALA CHEF 2010 AKTIF** 🟢")
    st.divider()
    
    # 📸 FITUR 100 FOTO (MATA DEWA)
    st.subheader("📸 SUNTIK DATA VISUAL (SANGGUP 100 FOTO!)")
    suntikan_foto = st.file_uploader("Seret Foto Elu ke Sini, Maestro :", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
    
    if suntikan_foto:
        cols = st.columns(3)
        for i, foto in enumerate(suntikan_foto):
            with cols[i % 3]:
                st.image(foto, caption=f"Objek ke-{i+1}", use_container_width=True)
        st.success(f"✅ {len(suntikan_foto)} Foto Berhasil Masuk Radar Nalar Dewa!")
        
    st.divider()
    
    # ✍️ PROMPT KERAMAT KOKO JAYA (JALUR STRATEGI)
    st.subheader("✍️ SUNTIK PROMPT KERAMAT KOKO JAYA")
    prompt_koko = st.text_area("Masukkan Instruksi Strategi 12 Ronde / Nalar Matematika Dewa :", height=150)
    
    if any(chr(i) in prompt_koko for i in range(0x0590, 0x05FF)):
        st.error("AKSES DITOLAK!! BAHASA PENJAJAH TERDETEKSI!!")
    else:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 EKSEKUSI VEO BRUTAL (PRIMARAGA 94)"):
                st.balloons()
                st.info("Merestorasi Visual Era 94... Seni 12 Ronde Aktif!")
        with col2:
            # --- REVISI ALA CHEF 2009-2010 ---
            if st.button("🍳 RESTORASI ALA CHEF 2009-2010"):
                st.snow()
                st.warning("Sinkronisasi Audio Original & Teknik Masak Era Emas!")

    st.divider()
    st.markdown("### 🧬 Nalar Matematika Dewa: **SIAGA SATU** 🥊")
    st.write("Fokus pada Presisi Hollywood dan Originalitas Tokoh!")

elif status == False:
    st.error('Password Salah!')
elif status == None:
    st.warning('Masukkan Kunci Akses Markas.')
# --- 🏛️ INTEGRASI JANTUNG APEXMINI (TAMBAHAN MAESTRO) ---
st.write("---")
st.subheader("🛰️ KONEKSI BRANKAS RAHASIA")

try:
    # Memanggil API KEY yang nanti Elu Save di Streamlit Secrets
    MAESTRO_KEY = st.secrets["OPENSOURCE_API_KEY"]
    st.success("✅ JALUR MENUJU BRANKAS TERDETEKSI!")
except Exception:
    MAESTRO_KEY = None
    st.warning("⚠️ JALUR BRANKAS BELUM TERPASANG DI SEMBELIT!")

# FITUR EKSEKUSI API (HANYA MUNCUL KALAU LOGIN BERHASIL)
if status:
    st.write("### 🧨 EKSEKUSI OPEN-SOURCE ENGINE")
    if st.button("🚀 AKTIFKAN KEKUATAN API"):
        if MAESTRO_KEY:
            st.info(f"ApexMini Berhasil Mengakses Brankas! Siap Hajar Prompt: {prompt_koko}")
        else:
            st.error("Gagal! Si Sembelit belum dikasih API KEY di menu Secrets-nya!") 
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
    
    # 4. TOMBOL EKSEKUSI (Hajar!)
    if st.button("EKSEKUSI SEKARANG! 🚀"):
        st.info("ApexMini sedang memproses tanpa interupsi protokol...")
        # Di sini kita bakal sambungin ke Model Raw dari GitHub/Cloud & Model Open-Source/Model-Stable Diffusion 3.5 (SD 3.5) (SD 3.5)
        st.success("Target Terkunci! ApexMini sanggup menerima instruksi  sesuai prompt")
        
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
print(decoded[0])from transformers import pipeline

# Inisialisasi pipeline peringkasan
summarizer = pipeline("summarization", model="Github/bart-large-cnn")

ARTICLE_TO_SUMMARIZE = """
Kecerdasan Buatan (AI) open source adalah AI yang kode sumbernya tersedia secara publik, sehingga siapa pun dapat mengakses, memodifikasi, dan mendistribusikannya secara bebas. Hal ini berbeda dengan AI proprietary yang dikembangkan dan dimiliki oleh perusahaan tertentu. Keuntungan menggunakan AI open source termasuk penghematan biaya, transparansi kode, dan dukungan komunitas yang aktif secara global. Banyak model open source seperti Llama dan Mistral kini bersaing ketat dengan model komersial dalam berbagai tugas seperti pengkodean dan penalaran.
"""

# Hasilkan ringkasan
summary = summarizer(ARTICLE_TO_SUMMARIZE, max_length=50, min_length=25, do_sample=False)
print(summary[0]['summary_text'])

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
