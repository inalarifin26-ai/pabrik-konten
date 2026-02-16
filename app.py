import streamlit as st
import google.generativeai as genai

# --- DNA ANCHOR: BYPASS MODE ---
# Kunci ditanam langsung untuk menghindari kemacetan menu Secrets
genai.configure(api_key="AIzaSyCW86D0dmfGwliqF0oPHhGp6COXKy8Q3wI")

# --- INISIALISASI MESIN FLASH LATEST ---
# Menggunakan 'latest' untuk menembus error 404 versi v1beta
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🛡️ SILA: SOVEREIGN OS")
st.info("STATUS: DNA ANCHOR ACTIVE")

# Input Perintah
prompt = st.chat_input("Apa instruksi Anda, Chief?")

if prompt:
    with st.chat_message("user"):
        st.write(prompt)
    
    try:
        # Proses Analisis sebagai SILA
        response = model.generate_content(f"Bertindaklah sebagai SILA Sovereign OS. Berikan analisis tajam untuk perintah ini: {prompt}")
        with st.chat_message("assistant"):
            st.write(response.text)
    except Exception as e:
        st.error(f"SILA Terhambat: {e}")
