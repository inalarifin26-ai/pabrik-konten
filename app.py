import streamlit as st
import google.generativeai as genai

# Konfigurasi Dasar
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")
st.title("🛡️ SILA: SOVEREIGN OS")

# Ambil kunci dari Secrets (Menghindari 400 API_KEY_INVALID)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Radar pengecekan model
    model_list = [m.name for m in genai.list_models()]
    st.success(f"✅ DNA Anchor Terkunci: {len(model_list)} Model Terdeteksi")
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if prompt := st.chat_input("Instruksi Anda, Chief?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            
except Exception as e:
    st.error(f"⚠️ Sistem Terhambat: {e}")
    st.info("Pastikan GOOGLE_API_KEY sudah dimasukkan di menu 'Secrets' Streamlit.")
