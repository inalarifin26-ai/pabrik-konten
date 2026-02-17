import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="SILA Sovereign OS - Diagnostic", page_icon="🕶️")

st.title("SILA: Diagnostic Mode")
st.write("Status: **MEMBONGKAR GERBANG API**")

# Ambil API Key dari Secrets
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    st.success("API Key Terdeteksi.")
except Exception as e:
    st.error(f"API Key Tidak Ditemukan di Secrets: {e}")

# Tombol Diagnostik
if st.button("CEK MODEL YANG TERSEDIA"):
    try:
        st.write("Memindai sirkuit Google...")
        available_models = [m.name for m in genai.list_models()]
        st.write("Model yang diizinkan untuk kunci Anda:")
        st.json(available_models)
        
        # Coba inisialisasi model pertama yang ditemukan
        if available_models:
            target = available_models[0]
            st.info(f"Mencoba penetrasi dengan: {target}")
            model = genai.GenerativeModel(target)
            response = model.generate_content("SILA, laporkan status.")
            st.success("KONEKSI BERHASIL!")
            st.write(response.text)
            st.balloons()
    except Exception as e:
        st.error(f"Kegagalan Diagnostik: {e}")
        st.info("Saran: Pastikan library 'google-generativeai' di requirements.txt adalah versi terbaru (0.8.3 atau lebih).")

st.write("---")
st.caption("SILA Standing By - Menunggu Perintah Chief.")
