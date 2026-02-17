import streamlit as st
import google.generativeai as genai

# Konfigurasi Google API Key kamu
# Pastikan kamu sudah mengatur GOOGLE_API_KEY di environment variables
# atau masukkan langsung di sini (tidak disarankan untuk produksi)
genai.configure(api_key="YOUR_GOOGLE_API_KEY")

st.title("Aplikasi Google AI Studio dengan Streamlit")

st.write("Ini adalah contoh sederhana bagaimana menghubungkan Streamlit dengan model Gemini dari Google AI Studio.")

# Pilih model yang ingin kamu gunakan (misalnya 'gemini-pro')
model = genai.GenerativeModel('gemini-pro')

# Input dari pengguna
user_input = st.text_area("Masukkan perintah atau pertanyaan kamu:", "Ceritakan tentang Jakarta")

if st.button("Kirim"):
    if user_input:
        try:
            # Panggil model Gemini
            with st.spinner("Memproses..."):
                response = model.generate_content(user_input)
            
            st.subheader("Respon dari Gemini:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
    else:
        st.warning("Mohon masukkan perintah atau pertanyaan.")

st.write("---")
st.write("Tips:")
st.markdown("- Pastikan kamu sudah menginstal `streamlit` dan `google-generativeai`.")
st.markdown("- Ganti `'YOUR_GOOGLE_API_KEY'` dengan kunci API Google kamu yang sebenarnya.")
st.markdown("- Untuk keamanan, disarankan untuk menyimpan API Key di environment variable.")
