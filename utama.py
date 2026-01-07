import streamlit as st
import streamlit_authenticator as stauth

# --- PAKU BUMI BETON APEXMINI (FIXED VERSION) ---
st.set_page_config(page_title="ApexMini Private HQ", page_icon="🛡️")

# Data User: Username: maestro | Password: ApexMini2026
config = {
    'credentials': {
        'usernames': {
            'maestro': {
                'name': 'Maestro Owner',
                'password': 'ApexMini2026'
            }
        }
    },
    'cookie': {'expiry_days': 30, 'key': 'apexmini_key', 'name': 'apexmini_cookie'}
}

# Inisialisasi Authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Render Form Login
authenticator.login()

if st.session_state["authentication_status"] is False:
    st.error('Username/password salah, Maestro!')
elif st.session_state["authentication_status"] is None:
    st.warning('Silakan masukkan kunci akses Markas Privat.')
elif st.session_state["authentication_status"]:
    authenticator.logout('Keluar Markas', 'sidebar')
    st.title(f'Selamat Datang, {st.session_state["name"]}! 🏛️')
    st.write("### ApexMini Status: **LIVE & PRIVAT** 🟢")
    st.success("Sembelit sembuh total! Ide gila Hollywood Elu AMAN!")
