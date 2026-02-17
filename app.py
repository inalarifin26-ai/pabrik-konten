import streamlit as st
import google.generativeai as genai

# BRIDGE: KONEKSI KE MESIN MASA DEPAN
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # KITA PAKAI HASIL SCAN TADI: 
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
else:
    st.error("API Key Hilang, Chief!")
    st.stop()

# TES KONEKSI
if st.button("AKTIFKAN SILA 2.0"):
    try:
        response = model.generate_content("Lapor status, SILA!")
        st.success(f"RESPON BERHASIL: {response.text}")
    except Exception as e:
        st.error(f"Interferensi Terakhir: {e}")
