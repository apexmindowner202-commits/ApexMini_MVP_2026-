import streamlit as st
import requests
import json

# ==========================================
# APEXMINI CORE ENGINE - OPENROUTER SECURITY
# ==========================================

def apex_core_connection(user_prompt):
    """
    Fungsi teknis untuk enkripsi dan koneksi 
    langsung ke OpenRouter API Endpoint.
    """
    endpoint = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://apexmini.ai", # Identitas Proyek
        "X-Title": "ApexMini MVP 2026"
    }
    
    payload = {
        "model": "openrouter/auto", # Jalur Open Source Otomatis
        "messages": [{"role": "user", "content": user_prompt}]
    }
    
    # Eksekusi Koneksi Tanpa Ambigu
    response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
    return response.json()





  

    

<div id="chat-box"></div>

<div class="input-area">
    <button id="upload-btn">+</button> <input type="text" id="user-prompt" placeholder=""> <button id="send-btn">Send</button>
</div>



