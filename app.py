# 2. BRIDGE: KONEKSI API STUDIO (EKSPERIMEN BYPASS 404)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # TAKTIK BARU: Gunakan nama model lengkap dengan prefiks 'models/'
    # Ini seringkali berhasil menembus error 404 di server Streamlit
    try:
        model = genai.GenerativeModel('models/gemini-1.0-pro')
    except Exception as e:
        st.error(f"Gagal Inisialisasi Model: {e}")
else:
    st.error("⚠️ API Key tidak terdeteksi di Vault Secrets!")
    st.stop()
