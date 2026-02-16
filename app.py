import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")
st.title("🛡️ SILA: SOVEREIGN OS")

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Pakai nama lengkap 'models/...' agar tidak kena 404 v1beta
    model = genai.GenerativeModel(
        model_name='models/gemini-1.5-flash',
        system_instruction="Anda SILA, partner casual Chief. Bicara santai tapi sopan."
    )
    
    # Radar pengecekan
    model_list = [m.name for m in genai.list_models()]
    st.success(f"✅ DNA Anchor Terkunci: {len(model_list)} Model Oke")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ada misi apa hari ini, Chief?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            # Cara panggil yang paling mendasar tanpa embel-embel
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    st.error(f"⚠️ Masalah: {e}")
