import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURASI ENGINE ---
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")

# Injeksi API Key Langsung (Tanpa hambatan Secrets)
genai.configure(api_key="AIzaSyCW86D0dmfGwliqF0oPHhGp6COXKy8Q3wI")

# PENENTU: Jalur absolut dengan tanda kutip ganda untuk menembus error 404
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# --- 2. ANTARMUKA PENGGUNA (UI) ---
st.title("🛡️ SILA: SOVEREIGN OS")
st.markdown("---")
st.info("🛰️ **STATUS SYSTEM:** DNA ANCHOR ACTIVE")

# Memory Session agar obrolan tidak terputus
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan riwayat percakapan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. LOGIKA OPERASI ---
if prompt := st.chat_input("Apa perintah Anda, Chief?"):
    # Simpan input user ke memori
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respon Otomatis SILA
    with st.chat_message("assistant"):
        try:
            # Mengirim data ke pusat saraf Gemini 1.5 Flash
            response = model.generate_content(f"Bertindaklah sebagai SILA Sovereign OS yang cerdas. Jawablah: {prompt}")
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            # Laporan jika jalur masih terhambat
            st.error(f"⚠️ SILA Terhambat: {e}")
