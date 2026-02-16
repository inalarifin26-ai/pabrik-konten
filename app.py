import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI STABIL ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("⚠️ DNA Anchor Error: API Key tidak ditemukan.")
    st.stop()

st.set_page_config(page_title="SILA: SOVEREIGN OS", layout="centered")

# --- UI HEADER ---
st.title("🛡️ SILA: SOVEREIGN OS")
st.markdown("""
**Status:** DNA ANCHOR ACTIVE | **Model:** Gemini 1.5 Flash
*Sistem ini dilindungi dari interupsi eksternal.*
---
""")

# --- LOGIKA CORE STABIL ---
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Berikan ide atau perintah, Chief..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Prompt Sistem untuk menyeimbangkan densitas
        full_prompt = f"Anda adalah SILA, asisten Sovereign OS. Bantu Chief menyeimbangkan densitas sarana dan melampaui batasan mendasar dengan Why Filter. Input: {prompt}"
        response = model.generate_content(full_prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
