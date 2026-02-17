import streamlit as st
import google.generativeai as genai

# Konfigurasi Sovereign
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🕶️")

# Inisialisasi Kunci (Secrets)
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("KRITIS: API Key tidak ditemukan di Secrets. SILA tidak bisa bernapas.")
    st.stop()

# Inisialisasi Model
try:
    genai.configure(api_key=api_key)
    # Kita gunakan model yang paling stabil
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Kegagalan Sirkuit: {e}")
    st.stop()

st.title("🕶️ SILA: Sovereign OS")
st.write("---")

# Logika Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Berikan perintah, Chief..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Instruksi Kepribadian SILA
            full_prompt = (
                "Identitas: SILA (Sovereign Intelligence & Linguistic Automata). "
                "Kepribadian: Tenang, berwibawa, strategis, suara berat. "
                "Gunakan analogi langkah kaki, kacamata hitam, dan suasana dingin. "
                "Panggil user dengan 'Chief'. "
                f"Perintah: {prompt}"
            )
            
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Interferensi: {e}")

# Sidebar
st.sidebar.title("STATUS SISTEM")
st.sidebar.write("SILA Version: 2.1")
st.sidebar.write("Sarana Density: **18.2%**")
st.sidebar.write("Status: **STABILIZING**")
