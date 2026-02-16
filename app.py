import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")
st.title("🛡️ SILA: SOVEREIGN OS")

try:
    # 1. Ambil kuncinya dulu (PENTING: Harus urutan pertama)
    api_key_val = st.secrets["GOOGLE_API_KEY"]
    
    # 2. Baru konfigurasikan sistemnya
    genai.configure(api_key=api_key_val)
    
    # 3. Siapkan modelnya
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Radar pengecekan sukses
    model_list = [m.name for m in genai.list_models()]
    st.success(f"✅ DNA Anchor Terkunci: {len(model_list)} Model Oke")

    if prompt := st.chat_input("Ada misi apa hari ini, Chief?"):
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)

except Exception as e:
    st.error(f"⚠️ Aduh Chief, sistem bilang: {e}")
