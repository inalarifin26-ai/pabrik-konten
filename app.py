import streamlit as st
import google.generativeai as genai
from google.api_core import client_options

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="SILA Sovereign OS",
    page_icon="🛡️",
    layout="centered"
)

# --- 2. KONFIGURASI API (PROTOKOL KEDAULATAN) ---
# Pastikan masukkan API Key BARU Anda di bawah ini
API_KEY = "MASUKKAN_API_KEY_BARU_DI_SINI"

# Memaksa sistem menggunakan jalur v1 (Menghindari Error 404 Jalur Beta)
options = client_options.ClientOptions(api_version='v1')

genai.configure(
    api_key=API_KEY,
    transport='rest',
    client_options=options
)

# Inisialisasi Model Gemini 1.5 Flash secara eksplisit
model = genai.GenerativeModel('models/gemini-1.5-flash')

# --- 3. ANTARMUKA PENGGUNA (UI) ---
st.title("🛡️ SILA: SOVEREIGN OS")
st.markdown("---")
st.info("🛰️ **STATUS SYSTEM:** PANGKALAN BARU AKTIF")

# Inisialisasi Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan Riwayat Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. LOGIKA KOMUNIKASI ---
if prompt := st.chat_input("Ketik perintah Anda di sini, Chief..."):
    # Tampilkan pesan User
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respon SILA
    with st.chat_message("assistant"):
        try:
            # Mengirim permintaan ke pusat saraf
            response = model.generate_content(prompt)
            
            if response.text:
                full_response = response.text
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.warning("⚠️ Sinyal diterima tapi tidak ada balasan teks.")
                
        except Exception as e:
            # Menangkap error tanpa merusak tampilan (Anti-Tembok Merah)
            st.error(f"⚠️ Gangguan Jaringan: {e}")
            st.code("Saran: Pastikan API Key benar dan lakukan Reboot di Dashboard Streamlit.")
