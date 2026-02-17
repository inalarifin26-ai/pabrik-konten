import streamlit as st
import google.generativeai as genai

# Inisialisasi API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # EKSPERIMEN BARU: Cek daftar model yang tersedia di server lo
    st.write("### 🛡️ Scanning Available Models...")
    try:
        available_models = [m.name for m in genai.list_models()]
        st.write("Model yang dikenali sistem lo:", available_models)
    except Exception as e:
        st.error(f"Gagal Scan: {e}")
