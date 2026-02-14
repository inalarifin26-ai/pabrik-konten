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

# 2. SETUP GEMINI (AUTO-DETECT)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
target_model = next((m for m in available_models if 'flash' in m), available_models[0])
model = genai.GenerativeModel(target_model)

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
        
        # Fitur Baru: Tambah Saldo (Simulasi)
        with st.sidebar.expander("➕ Isi Ulang Saldo"):
            tambah = st.number_input("Jumlah Poin", min_value=100, step=100)
            if st.button("Beli Poin Sekarang"):
                new_saldo = saldo + tambah
                user_ref.update({'saldo': new_saldo})
                st.success(f"Saldo berhasil ditambah! Silakan refresh.")
                st.rerun()
        
        st.sidebar.divider()
        st.sidebar.info(f"Model Aktif: {target_model}")

        # --- HALAMAN UTAMA ---
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("📝 Buat Konten Baru")
            topik = st.text_area("Apa yang ingin kamu buat hari ini?", placeholder="Contoh: Caption jualan baju lebaran...")
            
            if st.button("Proses Konten (Biaya: 50 Poin)"):
                if saldo >= 50:
                    with st.spinner('AI sedang meracik konten terbaik...'):
                        try:
                            response = model.generate_content(topik)
                            hasil = response.text
                            st.markdown("### ✨ Hasil Konten:")
                            st.write(hasil)
                            
                            # Update Saldo
                            new_saldo = int(saldo) - 50
                            user_ref.update({'saldo': new_saldo})
                            
                            # Simpan ke Riwayat (Opsional: simpan ke Firestore jika mau permanen)
                            st.success(f"Selesai! Saldo dipotong 50. Sisa: {new_saldo}")
                            st.balloons()
                        except Exception as e:
                            st.error(f"Terjadi kendala: {e}")
                else:
                    st.error("Yah, saldo kamu habis. Yuk isi ulang di samping!")

        with col2:
            st.subheader("📜 Tips Cepat")
            st.info("Gunakan kata kunci yang spesifik seperti 'lucu', 'formal', atau 'singkat' agar hasil AI lebih memuaskan.")

    else:
        st.error(f"User '{user_id}' tidak terdaftar di database.")
