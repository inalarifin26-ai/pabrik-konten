import streamlit as st
import google.generativeai as genai

# --- AKTIVASI LANGSUNG (BYPASS SECRETS) ---
API_KEY = "AIzaSyCW86D0dmfGwliqF0oPHhGp6COXKy8Q3wI"
genai.configure(api_key=API_KEY)

# --- INISIALISASI MODEL ---
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🛡️ SILA: SOVEREIGN OS")
st.write("Status: DNA ANCHOR ACTIVE (Bypass Mode)")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Perintah Anda, Chief?"):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Respon AI
    response = model.generate_content(f"Analisis sebagai SILA: {prompt}")
    with st.chat_message("assistant"):
        st.write(response.text)
    st.session_state.chat_history.append({"role": "assistant", "content": response.text})
