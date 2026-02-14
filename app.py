import streamlit as st
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, firestore
import json

# 1. SETUP FIREBASE
if not firebase_admin._apps:
    try:
        key_dict = json.loads(st.secrets["FIREBASE_JSON"])
        cred = credentials.Certificate(key_dict)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Error Firebase: {e}")
db = firestore.client()

# 2. SETUP GEMINI (AUTO-DETECT MODEL)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
target_model = next((m for m in available_models if 'flash' in m), available_models[0])
model = genai.GenerativeModel(target_model)

# Konfigurasi tampilan halaman
st.set_page_config(page_title="Pabrik Konten AI", layout="wide")
st.title("🚀 Pabrik Konten AI - Pro Edition")

# 3. SISTEM LOGIN & SIDEBAR
user_id = st.text_input("Masukkan ID User Anda", value="user_01")

if user_id:
    user_ref = db.collection('user').document(user_id)
    doc = user_ref.get()

    if doc.exists:
        user_data = doc.to_dict()
        saldo = user_data.get('saldo', 0)
        
        # --- TAMPILAN SIDEBAR ---
        st.sidebar.title(f"💰 Saldo: {saldo} Poin")
        st.sidebar.write(f"👤 User ID: {user_id}")
        
        # Fitur Isi Ulang Saldo
        with st.sidebar.expander("➕ Isi Ulang Saldo"):
            tambah = st.number_input("Jumlah Poin", min_value=100, step=100)
            if st.button("Beli Poin Sekarang"):
                new_saldo = saldo + tambah
                user_ref.update({'saldo': new_saldo})
                st.success(f"Saldo ditambah! Sisa: {new_saldo}")
                st.rerun()
        
        st.sidebar.divider()
        st.sidebar.info(f"Model: {target_model}")

        # --- HALAMAN UTAMA ---
        # Gunakan kolom agar lebih rapi
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("📝 Buat Konten")
            topik = st.text_area("Apa yang ingin kamu buat?", placeholder="Contoh: Caption jualan baju...")
            
            if st.button("Proses (50 Poin)"):
                if not topik:
                    st.warning("Silakan isi ide kontennya dulu!")
                elif saldo >= 50:
                    with st.spinner('AI sedang meracik konten...'):
                        try:
                            response = model.generate_content(topik)
                            hasil = response.text
                            st.markdown("---")
                            st.subheader("✨ Hasil Konten:")
                            st.write(hasil)
                            
                            # Update Saldo ke Firestore
                            new_saldo = int(saldo) - 50
                            user_ref.update({'saldo': new_saldo})
                            st.success(f"Saldo dipotong 50. Sisa: {new_saldo}")
                            st.balloons()
                        except Exception as e:
                            st.error(f"Error AI: {e}")
                else:
                    st.error("Saldo kamu habis!")

        with col2:
            st.subheader("💡 Tips")
            st.info("Hasil konten AI ini bisa langsung kamu copy-paste ke Instagram atau TikTok!")

    else:
        st.error(f"User '{user_id}' tidak ditemukan.")
