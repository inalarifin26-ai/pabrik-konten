import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")
st.title("🛡️ SILA: SOVEREIGN OS")

try:
    # Ambil kunci dari Secrets
    api_key = st.secrets["GOOGLE_API_KEY"]
    
    # Paksa konfigurasi ke Jalur Stabil (v1)
    genai.configure(api_key=api_key, transport='rest')
    
    # KUNCI UTAMA: Tambahkan api_version='v1' di sini
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        generation_config={"api_version": "v1"} 
    )
    
    # Cek model lagi untuk memastikan
    model_list = [m.name for m in genai.list_models()]
    st.success(f"✅ DNA Anchor Terkunci: {len(model_list)} Model Oke")

    if prompt := st.chat_input("Instruksi, Chief?"):
        # Kita panggil dengan cara yang paling standar
        response = genai.ChatSession(model=model).send_message(prompt)
        st.write(response.text)

except Exception as e:
    st.error(f"⚠️ Masalah: {e}")
