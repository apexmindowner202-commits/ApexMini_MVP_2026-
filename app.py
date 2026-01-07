import streamlit as st
import streamlit_authenticator as stauth

# --- PAKU BUMI BETON APEXMINI ---
st.set_page_config(page_title="ApexMini Private HQ", page_icon="🛡️")

# Data Owner (Hanya Elu!)
names = ['Maestro Owner']
usernames = ['maestro']
passwords = ['ApexMini2026'] # Ini kunci masuk Elu nanti!

hashed_passwords = stauth.Hasher(passwords).generate()

config = {
    'credentials': {
        'usernames': {
            usernames[0]: {'name': names[0], 'password': hashed_passwords[0]}
        }
    },
    'cookie': {'expiry_days': 30, 'key': 'apexmini_secret', 'name': 'apexmini_auth'}
}

authenticator = stauth.Authenticate(
    config['credentials'], config['cookie']['name'], 
    config['cookie']['key'], config['cookie']['expiry_days']
)

# Tampilkan Form Login
name, authentication_status, username = authenticator.login('Login Markas ApexMini', 'main')

if authentication_status == False:
    st.error('Password Salah! Akses Ditolak.')
elif authentication_status == None:
    st.warning('Masukkan Kunci Akses untuk Masuk ke Markas Privat.')
elif authentication_status:
    # --- ISI MARKAS PRIVAT ELU ---
    authenticator.logout('Keluar Markas', 'sidebar')
    st.title(f'Selamat Datang, {name}! 🏛️')
    st.write("### ApexMini Status: **LIVE & PRIVAT** 🟢")
    st.success("Sesuai janji, ide gila Hollywood Elu aman di sini. Protokol najong gak bisa masuk!")
