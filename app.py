import streamlit as st
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, firestore
import json

# 1. SETUP FIREBASE (FIRESTORE)
if not firebase_admin._apps:
    try:
        key_dict = json.loads(st.secrets["FIREBASE_JSON"])
        cred = credentials.Certificate(key_dict)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Error Firebase: {e}")

db = firestore.client()

# 2. SETUP GEMINI AI (MODEL STABIL)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Menggunakan model paling stabil untuk menghindari error 404
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Pabrik Konten AI", layout="centered")
st.title("🚀 Pabrik Konten AI")

# 3. SISTEM LOGIN & SALDO
user_id = st.text_input("Masukkan ID User Anda", value="user_01")

if user_id:
    user_ref = db.collection('user').document(user_id)
    doc = user_ref.get()

    if doc.exists:
        user_data = doc.to_dict()
        saldo = user_data.get('saldo', 0)
        
        # Tampilan Saldo di Sidebar
        st.sidebar.title(f"💰 Saldo: {saldo} Poin")
        st.sidebar.write(f"👤 User: {user_id}")
        st.sidebar.divider()

        topik = st.text_area("Tulis ide kontenmu di sini...", placeholder="Contoh: Buatkan caption jualan ayam geprek...")
        
        if st.button("Buat Konten (50 Poin)"):
            if saldo >= 50:
                with st.spinner('Sedang memproses konten...'):
                    try:
                        # Memanggil AI
                        response = model.generate_content(topik)
                        st.markdown("### Hasil Konten Anda:")
                        st.write(response.text)
                        
                        # Update Saldo di Firestore
                        new_saldo = int(saldo) - 50
                        user_ref.update({'saldo': new_saldo})
                        
                        st.success(f"Berhasil! Sisa Saldo: {new_saldo}")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Gagal memanggil AI: {e}")
            else:
                st.error("Maaf, saldo Anda tidak mencukupi.")
    else:
        st.error(f"ID User '{user_id}' tidak ditemukan di Firestore.")
