import streamlit as st
import google.generativeai as genai

# --- SETTING DASAR ---
st.set_page_config(page_title="NOFA Factory", layout="wide")

# --- KONEKSI MESIN AI (ANTI ERROR) ---
# Menggunakan model terbaru agar tidak NotFound
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Inisialisasi status login agar menu tidak hilang
if 'step' not in st.session_state:
    st.session_state.step = "login"

# --- FUNGSI PROSES KONTEN ---
def proses_ai(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Gagal memanggil AI: {e}")
        return None

# --- LOGIKA TAMPILAN ---

# 1. HALAMAN STUDIO ACCESS (Pintu Depan)
if st.session_state.step == "login":
    st.title("🔑 Studio Access")
    creator_id = st.text_input("Enter your Creator ID", value="user_01")
    st.subheader(f"🤖 Welcome back, {creator_id}!")
    
    input_user = st.text_area("Apa yang ingin Anda buat hari ini?")
    
    if st.button("⚡ GENERATE"):
        with st.spinner("Menghubungkan ke Neural Network..."):
            hasil = proses_ai(input_user)
            if hasil:
                st.session_state.hasil = hasil
                st.session_state.step = "dashboard"
                st.rerun()

# 2. HALAMAN DASHBOARD (Pusat Produksi)
else:
    st.markdown("### 🧬 NOFA FACTORY V1.0.42")
    
    # Navigasi Bawah yang Manajer harapkan
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 HOME", "📝 PRODUKSI", "🎨 EDITOR", "📚 GUDANG"])
    
    with tab1:
        st.success("✅ Konten Berhasil Dibuat!")
        st.write(st.session_state.hasil)
        
    with tab2:
        st.subheader("Input Produksi")
        st.write("Siapkan bahan baku konten lo di sini.")
        st.button("Sosial Media")
        st.button("Artikel/Blog")
        
    with tab3:
        st.subheader("Art Engine")
        st.write("Modul editor sedang sinkronisasi...")
        
    with tab4:
        st.subheader("Neural Vault")
        st.write("Semua aset Anda tersimpan di sini.")

    if st.button("⬅️ Kembali ke Studio"):
        st.session_state.step = "login"
        st.rerun()
