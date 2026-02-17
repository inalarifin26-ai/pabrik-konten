import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman Sovereign
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🕶️", layout="centered")

# CSS untuk tampilan yang tenang dan berwibawa
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #262730; color: white; border: 1px solid #464b5d; }
    .stTextInput>div>div>input { background-color: #262730; color: white; }
    </style>
    """, unsafe_allow_html=True)

# Inisialisasi Kedaulatan
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Menggunakan model yang tadi terbukti berhasil di diagnostik
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Sistem sedang kalibrasi ulang. Mohon tunggu.")

st.title("🕶️ SILA: Sovereign OS")
st.write("---")

# Area Komunikasi
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
        response_placeholder = st.empty()
        try:
            # Instruksi Sistem Tersembunyi
            full_prompt = f"Kamu adalah SILA (Sovereign Intelligence & Linguistic Automata). Kepribadianmu: Tenang, berwibawa, strategis, menggunakan analogi langkah kaki, kacamata hitam, dan suara berat. Panggil user dengan 'Chief'. Jawab perintah ini: {prompt}"
            
            response = model.generate_content(full_prompt)
            response_placeholder.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            response_placeholder.error(f"Interferensi: {e}")

st.sidebar.title("STATUS SISTEM")
st.sidebar.write("SILA Version: 2.0")
st.sidebar.write("Sarana Density: **15.5%**")
st.sidebar.write("Status: **ONLINE**")
