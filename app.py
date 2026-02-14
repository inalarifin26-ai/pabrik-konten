import streamlit as st
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, firestore
import json

# 1. SETUP FIREBASE FIRESTORE
if not firebase_admin._apps:
    try:
        key_dict = json.loads(st.secrets["FIREBASE_JSON"])
        cred = credentials.Certificate(key_dict)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Error Konfigurasi Secrets: {e}")

db = firestore.client()

# 2. SETUP GEMINI AI
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Pabrik Konten AI", layout="centered")
st.title("🚀 Pabrik Konten AI")

# 3. SISTEM LOGIN & SALDO
user_id = st.text_input("Masukkan ID User Anda", placeholder="Contoh: user_01")

if user_id:
    # Mengambil dokumen dari koleksi 'user'
    user_ref = db.collection('user').document(user_id)
    doc = user_ref.get()

    if doc.exists:
        user_data = doc.to_dict()
        saldo = user_data.get('saldo', 0)
        
        # Tampilan Sidebar
        st.sidebar.subheader(f"👤 User: {user_id}")
        st.sidebar.title(f"💰 Saldo: {saldo} Poin")
        st.sidebar.divider()
        st.sidebar.write("Gunakan poinmu untuk membuat konten AI berkualitas.")

        # Area Kerja AI
        topik = st.text_area("Apa yang ingin kamu buat hari ini?", placeholder="Contoh: Buatkan caption Instagram tentang jualan sepatu...")
        
        if st.button("Buat Konten (Biaya: 50 Poin)"):
            if saldo >= 50:
                with st.spinner('Sedang memproses konten...'):
                    try:
                        response = model.generate_content(topik)
                        st.markdown("### Hasil Konten Anda:")
                        st.write(response.text)
                        
                        # Update saldo di Firestore
                        new_saldo = saldo - 50
                        user_ref.update({'saldo': new_saldo})
                        
                        st.success(f"Berhasil! Saldo terpotong 50. Sisa: {new_saldo}")
                        st.balloons()
                        # Refresh halaman untuk update saldo di sidebar
                        st.button("Update Saldo Baru")
                    except Exception as e:
                        st.error(f"Gagal memanggil AI: {e}")
            else:
                st.error("Maaf, saldo Anda tidak cukup untuk membuat konten.")
    else:
        st.error(f"ID User '{user_id}' tidak ditemukan. Pastikan penulisan sudah benar.")
else:
    st.info("Silakan masukkan ID User di kolom atas untuk melihat saldo dan mulai menggunakan AI.")
