import streamlit as st
import google.generativeai as genai

# --- DNA ANCHOR: KUNCI LANGSUNG ---
# Pastikan tidak ada spasi tambahan di dalam tanda kutip ini
genai.configure(api_key="AIzaSyCW86D0dmfGwliqF0oPHhGp6COXKy8Q3wI")

# --- INISIALISASI MESIN FLASH ---
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🛡️ SILA: SOVEREIGN OS")
st.info("Status: SISTEM AKTIF - MENUNGGU PERINTAH CHIEF")

# Kolom Input
prompt = st.chat_input("Apa instruksi Anda, Chief?")

if prompt:
    with st.chat_message("user"):
        st.write(prompt)
    
    try:
        # Proses Analisis
        response = model.generate_content(prompt)
        with st.chat_message("assistant"):
            st.write(response.text)
    except Exception as e:
        st.error(f"SILA Terhambat: {e}")
