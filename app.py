import streamlit as st
import google.generativeai as genai
from google.api_core import client_options

# --- KONFIGURASI TOTAL ---
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")

# INI SOLUSINYA: Memaksa API menggunakan versi 'v1' (Bukan v1beta)
options = client_options.ClientOptions(api_version='v1')

genai.configure(
    api_key="AIzaSyCW86D0dmfGwliqF0oPHhGp6COXKy8Q3wI",
    transport='rest',
    client_options=options # Mengunci jalur agar tidak 404 lagi
)

# Panggil nama model secara bersih sesuai saran SILA poin 2
model = genai.GenerativeModel('gemini-1.5-flash')

# --- ANTARMUKA ---
st.title("🛡️ SILA: SOVEREIGN OS")
st.info("🛰️ **STATUS SYSTEM:** DNA ANCHOR ACTIVE")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- LOGIKA ---
if prompt := st.chat_input("Instruksi Anda, Chief?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Menggunakan jalur v1 yang sudah dipaksa di atas
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Jika masih error, ini akan menampilkan jalur mana yang gagal
            st.error(f"⚠️ Jalur Masih Terhambat: {e}")
