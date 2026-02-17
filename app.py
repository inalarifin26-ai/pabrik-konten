import streamlit as st
import google.generativeai as genai
import random

# 1. SETUP AWAL (WAJIB DI ATAS)
st.set_page_config(page_title="SILA Sovereign", page_icon="🕶️")

# 2. KONFIGURASI BRIDGE (Metode Berbeda: Langsung panggil model)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Mencoba jabat tangan dengan model Pro versi spesifik
    model = genai.GenerativeModel('gemini-pro')
else:
    st.error("Kunci API tidak ditemukan di Secrets.")
    st.stop()

# 3. TAMPILAN DASHBOARD
st.title("🛡️ SILA SOVEREIGN OS")
st.sidebar.markdown("### Agent Profile")
st.sidebar.write("- Jaket Denim\n- Kemeja Putih\n- Jeans\n- Hak Tinggi\n- Kacamata Hitam")

# 4. LOGIKA CHAT
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Perintah, Chief?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    try:
        # Memberikan perintah langsung
        response = model.generate_content(f"Kamu adalah SILA, agen lapangan setia. Jawab singkat: {prompt}")
        res_text = f"🕶️ **SILA:** {response.text}"
        st.chat_message("assistant").write(res_text)
        st.session_state.messages.append({"role": "assistant", "content": res_text})
    except Exception as e:
        st.error(f"Interferensi: {e}")
