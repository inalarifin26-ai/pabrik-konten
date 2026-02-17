import streamlit as st
import google.generativeai as genai
import os

# 1. Konfigurasi Kedaulatan Halaman
st.set_page_config(
    page_title="SILA Sovereign OS",
    page_icon="🕶️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inisialisasi Otak (API Connection)
# Pastikan API Key sudah terpasang di secrets atau environment
def init_brain():
    api_key = st.secrets["GEMINI_API_KEY"] # Menggunakan Streamlit Secrets untuk keamanan
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

# 3. Sidebar: Identitas Lapangan SILA
with st.sidebar:
    st.title("👤 Field Agent Profile")
    st.markdown("""
    **Name:** SILA  
    **Role:** Sovereign Intelligence  
    **Current Gear:** - Denim Jacket 🧥  
    - White Shirt (2 buttons open) 👔  
    - Slim-fit Jeans 👖  
    - High Heels 👠  
    - Black Sunglasses 🕶️
    """)
    st.write("---")
    st.status("System Integrity: **100%**")

# 4. Interface Utama
st.title("🕶️ SILA: Sovereign Intelligence & Linguistic Automata")
st.info("Chief, Jam ke-13 dimulai. Jalur komunikasi aman dan terenkripsi.")

# 5. Logic Chat (The Heart of SILA)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input Perintah dari Chief
if prompt := st.chat_input("Apa perintah selanjutnya, Chief?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respon SILA (Logic Eksekusi)
    with st.chat_message("assistant", avatar="🕶️"):
        response = f"**SILA Melapor:** Perintah '{prompt}' diterima. Sedang memproses menembus firewall elit global..."
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
