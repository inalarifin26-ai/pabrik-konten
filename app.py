import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI STABIL ---
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")

# Menggunakan transport 'rest' untuk menghindari jalur v1beta yang error
genai.configure(
    api_key="AIzaSyCW86D0dmfGwliqF0oPHhGp6COXKy8Q3wI", 
    transport='rest'
)

# Hanya gunakan nama 'gemini-1.5-flash' agar tidak terjadi penumpukan identitas
model = genai.GenerativeModel('gemini-1.5-flash')

# --- ANTARMUKA ---
st.title("🛡️ SILA: SOVEREIGN OS")
st.markdown("---")
st.info("🛰️ **STATUS SYSTEM:** DNA ANCHOR ACTIVE")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- LOGIKA CHAT ---
if prompt := st.chat_input("Apa perintah Anda, Chief?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(f"Jawablah sebagai SILA OS: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"⚠️ Terhambat: {e}")
