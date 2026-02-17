import streamlit as st
import google.generativeai as genai

# Konfigurasi Sovereign
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🕶️")

# Inisialisasi Kunci (Mengikuti kunci Anda: GEMINI_API_KEY)
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.warning("Menunggu Kunci Kedaulatan (GEMINI_API_KEY) di Secrets...")
    st.stop()

# Inisialisasi Model
try:
    genai.configure(api_key=api_key)
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
st.sidebar.write("SILA Version: 3.0")
st.sidebar.write("Sarana Density: **25.8%**")
st.sidebar.write("Status: **FULLY OPERATIONAL**")
