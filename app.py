import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI KEDAULATAN ---
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")

# Inisialisasi API dengan Jalur Stabil (Poin 3 SILA)
genai.configure(
    api_key="AIzaSyCW86D0dmfGwliqF0oPHhGp6COXKy8Q3wI",
    transport='rest'
)

# Gunakan model_name dengan prefix lengkap untuk menghindari ambiguitas
model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')

# --- ANTARMUKA ---
st.title("🛡️ SILA: SOVEREIGN OS")
st.info("🛰️ **STATUS SYSTEM:** DNA ANCHOR ACTIVE")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- LOGIKA EKSEKUSI ---
if prompt := st.chat_input("Instruksi Anda, Chief?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Memanggil pusat saraf SILA
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Jika masih terhambat, kita akan tahu persis di mana titiknya
            st.error(f"⚠️ SILA Terhambat: {e}")
