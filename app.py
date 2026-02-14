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

# Inisialisasi riwayat di memori aplikasi
if 'history' not in st.session_state:
    st.session_state.history = []

# 3. SISTEM LOGIN & SIDEBAR
user_id = st.text_input("Masukkan ID User Anda", value="user_01")

if user_id:
    user_ref = db.collection('user').document(user_id)
    doc = user_ref.get()

    if doc.exists:
        user_data = doc.to_dict()
        saldo = user_data.get('saldo', 0)
        
        st.sidebar.title(f"💰 Saldo: {saldo} Poin")
        st.sidebar.write(f"👤 User ID: {user_id}")
        
        # Fitur Isi Ulang
        with st.sidebar.expander("➕ Isi Ulang Saldo"):
            tambah = st.number_input("Jumlah Poin", min_value=100, step=100)
            if st.button("Beli Poin Sekarang"):
                new_saldo = saldo + tambah
                user_ref.update({'saldo': new_saldo})
                st.success(f"Berhasil! Saldo sekarang: {new_saldo}")
                st.rerun()
        
        st.sidebar.divider()
        st.sidebar.info(f"Model Aktif: {target_model}")

        # --- HALAMAN UTAMA ---
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("📝 Buat Konten Baru")
            topik = st.text_area("Apa ide kontenmu?", placeholder="Contoh: Caption promo baju lebaran...")
            
            if st.button("Proses Konten (50 Poin)"):
                if not topik:
                    st.warning("Isi dulu idenya ya!")
                elif saldo >= 50:
                    with st.spinner('AI sedang bekerja...'):
                        try:
                            response = model.generate_content(topik)
                            hasil_ai = response.text
                            
                            # Simpan ke riwayat sesi
                            st.session_state.history.append({"topik": topik, "hasil": hasil_ai})
                            
                            # Update Saldo
                            new_saldo = int(saldo) - 50
                            user_ref.update({'saldo': new_saldo})
                            st.rerun() # Refresh agar saldo langsung berkurang di tampilan
                        except Exception as e:
                            st.error(f"Gagal: {e}")
                else:
                    st.error("Saldo habis!")

            # Tampilkan Hasil Terbaru Jika Ada
            if st.session_state.history:
                st.markdown("---")
                st.subheader("✨ Hasil Terkini:")
                st.write(st.session_state.history[-1]["hasil"])
                st.balloons()

        with col2:
            st.subheader("📜 Riwayat Sesi")
            if not st.session_state.history:
                st.write("Belum ada riwayat.")
            else:
                for i, item in enumerate(reversed(st.session_state.history)):
                    with st.expander(f"Konten {len(st.session_state.history)-i}: {item['topik'][:20]}..."):
                        st.write(item['hasil'])
                
                if st.button("🗑️ Hapus Riwayat"):
                    st.session_state.history = []
                    st.rerun()
    else:
        st.error("User ID tidak ditemukan.")
