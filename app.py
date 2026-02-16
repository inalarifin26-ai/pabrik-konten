import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI KEAMANAN ---
try:
    # Mengambil kunci dari brankas Secrets yang baru saja Chief isi
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("⚠️ DNA Anchor Error: Cek konfigurasi Secrets Anda.")
    st.stop()

# --- INISIALISASI MODEL STABIL ---
# Menggunakan gemini-1.5-flash untuk menghindari error 'NotFound'
model = genai.GenerativeModel('gemini-1.5-flash')

# --- ANTARMUKA SILA ---
st.set_page_config(page_title="SILA: SOVEREIGN OS")
st.title("🛡️ SILA: SOVEREIGN OS")
st.markdown("**Status:** DNA ANCHOR ACTIVE | **Model:** Gemini 1.5 Flash")
st.write("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Perintah Anda, Chief?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Perintah sistem untuk mengaktifkan Why Filter
        system_instruction = f"Anda adalah SILA, asisten Sovereign OS. Gunakan Why Filter untuk menganalisis: {prompt}"
        response = model.generate_content(system_instruction)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
