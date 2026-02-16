import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")

# Kunci API Langsung
genai.configure(api_key="AIzaSyCW86D0dmfGwliqF0oPHhGp6COXKy8Q3wI")

# JALUR ABSOLUT: Mengunci model agar tidak tersesat ke v1beta (Penyebab 404)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# --- 2. INTERFACE ---
st.title("🛡️ SILA: SOVEREIGN OS")
st.markdown("---")
st.info("🛰️ **STATUS SYSTEM:** DNA ANCHOR ACTIVE")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. LOGIC ---
if prompt := st.chat_input("Apa instruksi Anda, Chief?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Mengirim perintah ke pusat saraf
            response = model.generate_content(f"Bertindaklah sebagai SILA Sovereign OS. Jawablah: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"⚠️ SILA Terhambat: {e}")
