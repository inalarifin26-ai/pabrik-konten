import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURASI SESUAI SARAN SILA ---
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")

# Menggunakan transport='rest' untuk memastikan jalur stabil (Poin 3 SILA)
genai.configure(
    api_key="AIzaSyCW86D0dmfGwliqF0oPHhGp6COXKy8Q3wI", 
    transport='rest'
)

# Hanya menggunakan nama 'gemini-1.5-flash' untuk menghindari penumpukan (Poin 2 SILA)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. ANTARMUKA PENGGUNA ---
st.title("🛡️ SILA: SOVEREIGN OS")
st.markdown("---")
st.info("🛰️ **STATUS SYSTEM:** DNA ANCHOR ACTIVE")

# Memory Session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render Percakapan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. LOGIKA OPERASI ---
if prompt := st.chat_input("Apa perintah Anda, Chief?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Memanggil respon taktis
            response = model.generate_content(f"Bertindaklah sebagai SILA Sovereign OS. Jawablah: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Menampilkan detail jika masih ada hambatan
            st.error(f"⚠️ SILA Terhambat: {e}")
