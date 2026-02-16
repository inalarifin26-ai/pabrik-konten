import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURASI ENGINE ---
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")

# Injeksi API Key Langsung
genai.configure(api_key="AIzaSyCW86D0dmfGwliqF0oPHhGp6COXKy8Q3wI")

# PENENTU: Menggunakan jalur absolut 'models/' untuk mematikan Error 404
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# --- 2. ANTARMUKA PENGGUNA (UI) ---
st.title("🛡️ SILA: SOVEREIGN OS")
st.markdown("---")
st.info("🛰️ **STATUS SYSTEM:** DNA ANCHOR ACTIVE")

# Memory Session agar riwayat chat tidak hilang
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan riwayat chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. LOGIKA KOMUNIKASI ---
if prompt := st.chat_input("Berikan perintah, Chief?"):
    # Simpan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respon SILA
    with st.chat_message("assistant"):
        try:
            # Mengirim instruksi ke inti saraf Gemini
            response = model.generate_content(f"Bertindaklah sebagai SILA Sovereign OS yang cerdas dan taktis. Jawablah: {prompt}")
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            # Jika masih error, sistem akan memberikan detail teknis
            st.error(f"⚠️ SILA Terhambat: {e}")
