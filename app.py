import streamlit as st
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, firestore
import json

# 1. SETUP FIREBASE FIRESTORE
if not firebase_admin._apps:
    key_dict = json.loads(st.secrets["FIREBASE_JSON"])
    cred = credentials.Certificate(key_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 2. SETUP GEMINI AI
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Pabrik Konten AI")
st.title("🚀 Pabrik Konten AI")

# 3. SISTEM LOGIN & SALDO FIRESTORE
user_id = st.text_input("Masukkan ID User Anda (Contoh: user_01)")

if user_id:
    # Mengambil dokumen dari koleksi 'user'
    user_ref = db.collection('user').document(user_id)
    doc = user_ref.get()

    if doc.exists:
        user_data = doc.to_dict()
        # Mengambil field 'saldo' yang sudah bertipe number
        saldo = user_data.get('saldo', 0)
        
        st.sidebar.subheader(f"👤 User: {user_id}")
        st.sidebar.write(f"💰 Saldo: {saldo} Poin")

        topik = st.text_area("Apa yang ingin kamu buat hari ini?")
        
        if st.button("Buat Konten (Biaya: 50 Poin)"):
            if saldo >= 50:
                with st.spinner('AI sedang menulis...'):
                    response = model.generate_content(topik)
                    st.success("Konten Berhasil Dibuat!")
                    st.write(response.text)
                    
                    # Update saldo otomatis di Firestore
                    user_ref.update({'saldo': saldo - 50})
                    st.info(f"Saldo dipotong 50. Sisa saldo: {saldo - 50}")
                    st.balloons()
            else:
                st.error("Saldo tidak cukup!")
    else:
        st.error(f"ID User '{user_id}' tidak ditemukan di koleksi 'user' Firestore.")
        
        if st.button("Buat Konten (Biaya: 50 Poin)"):
            if saldo >= 50:
                with st.spinner('AI sedang menulis konten untukmu...'):
                    try:
                        # Proses AI
                        response = model.generate_content(f"Buatlah konten sosial media yang menarik tentang: {topik}")
                        st.success("Konten Berhasil Dibuat!")
                        st.write(response.text)
                        
                        # Potong Saldo di Firebase
                        new_saldo = saldo - 50
                        ref.update({'saldo': new_saldo})
                        st.info(f"Saldo dipotong 50. Sisa saldo: {new_saldo}")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Terjadi kesalahan AI: {e}")
            else:
                st.error("Saldo tidak cukup! Silakan hubungi admin untuk Top-up.")
    else:
        st.error("ID User tidak ditemukan. Pastikan sudah terdaftar di database.")
else:
    st.info("Silakan masukkan ID User di kolom atas untuk mulai.")
