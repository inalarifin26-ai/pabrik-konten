import streamlit as st
import google.generativeai as genai

# --- 🛡️ SILA: SOVEREIGN OS CORE CONFIG ---
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")

# 1. KUNCI API (Direct Bypass Mode)
# Menanamkan kunci langsung agar tombol 'Save' di HP yang macet tidak lagi jadi kendala
genai.configure(api_key="AIzaSyCW86D0dmfGwliqF0oPHhGp6COXKy8Q3wI")

# 2. INISIALISASI MODEL STABIL
# Menggunakan versi flash standar yang didukung oleh requirements.txt kita
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 🖥️ INTERFACE PENGGUNA ---
st.title("🛡️ SILA: SOVEREIGN OS")
st.markdown("---")
st.info("🛰️ **STATUS SYSTEM:** DNA ANCHOR ACTIVE")

# Inisialisasi Riwayat Pesan agar tidak hilang saat mengetik
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan Riwayat Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 🧠 LOGIKA KOMANDO ---
if prompt := st.chat_input("Apa perintah Anda, Chief?"):
    # Tambahkan pesan user ke riwayat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respon AI (SILA Mode)
    with st.chat_message("assistant"):
        try:
            # Memberikan instruksi spesifik agar AI berperan sebagai SILA
            full_prompt = f"Analisis dan jawablah sebagai SILA Sovereign OS yang cerdas dan taktis: {prompt}"
            response = model.generate_content(full_prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"⚠️ SILA Terhambat: {e}")
            st.write("Pastikan file requirements.txt sudah di-update dan aplikasi di-reboot
