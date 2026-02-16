import streamlit as st
import google.generativeai as genai # Pastikan baris ini ada di paling atas!

st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")
st.title("🛡️ SILA: SOVEREIGN OS")

try:
    # 1. Pastikan genai benar-benar ada
    if 'genai' in globals() or 'genai' in locals():
        kunci = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=kunci)
        
        # 2. Pakai model yang paling stabil biar nggak 404
        model = genai.GenerativeModel('gemini-pro')
        
        st.success("✅ Sistem Mengenali DNA: Semua Oke")
    else:
        st.error("❌ Library 'genai' hilang dari radar!")

except Exception as e:
    st.error(f"⚠️ Masalah Logistik: {e}")
