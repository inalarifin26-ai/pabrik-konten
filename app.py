import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")

# Masukkan API Key BARU Chief di sini
API_KEY = "PASTE_API_KEY_BARU_DI_SINI"

genai.configure(api_key=API_KEY)

st.title("🛡️ SILA: SOVEREIGN OS")

# FUNGSI DARURAT: Cek model apa yang tersedia di API Key ini
try:
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    st.success(f"✅ Sistem Berhasil Join! Model tersedia: {available_models}")
except Exception as e:
    st.error(f"⚠️ Gagal Cek Model: {e}")

# Inisialisasi Model secara manual dari daftar di atas
# Jika 'gemini-1.5-flash' ada di daftar, sistem pasti jalan
model = genai.GenerativeModel('gemini-1.5-flash')

if prompt := st.chat_input("Perintah Anda, Chief?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"⚠️ Masalah Teknis: {e}")
