import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")

# Injeksi Kunci API Langsung
genai.configure(api_key="AIzaSyCW86D0dmfGwliqF0oPHhGp6COXKy8Q3wI")

# Inisialisasi Model dengan Jalur Lengkap (Solusi Error 404)
# Menambahkan 'models/' memastikan server tidak mencari di jalur yang salah
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# --- UI INTERFACE ---
st.title("🛡️ SILA: SOVEREIGN OS")
st.markdown("---")
st.info("🛰️ **STATUS SYSTEM:** DNA ANCHOR ACTIVE")

# Memory Session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- LOGIKA OPERASI ---
if prompt := st.chat_input("Apa instruksi Anda, Chief?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Instruksi Protokol SILA
            response = model.generate_content(f"Bertindaklah sebagai SILA Sovereign OS. Berikan jawaban taktis untuk: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"⚠️ SILA Terhambat: {e}")
