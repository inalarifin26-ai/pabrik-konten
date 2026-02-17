import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🕶️")

# Inisialisasi API
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Gunakan nama model paling dasar tanpa embel-embel 'latest' atau 'models/'
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Kegagalan Inisialisasi: {e}")

st.title("SILA: Sovereign OS")
st.write("Status: **PENETRASI DINDING 404**")

if st.button("AKTIFKAN PROTOKOL SILA"):
    try:
        # Test koneksi sederhana
        response = model.generate_content("SILA, apakah kau di sana?")
        st.success("KONEKSI TERJALIN.")
        st.write(response.text)
        st.balloons()
    except Exception as e:
        st.error(f"Interferensi Terakhir: {e}")
        st.info("Saran: Periksa apakah API Key di Secrets Streamlit sudah benar.")
