import streamlit as st
import google.generativeai as genai
import pandas as pd
import numpy as np

# 1. KONFIGURASI KEDAULATAN HALAMAN
st.set_page_config(
    page_title="SILA Sovereign OS",
    page_icon="🕶️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. INISIALISASI OTAK (API CONNECTION)
# Pastikan API Key sudah dimasukkan di Streamlit Cloud Secrets (Settings > Secrets)
# format: GEMINI_API_KEY = "your_key_here"
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # Gunakan inisialisasi yang lebih aman untuk menghindari error v1/v1beta
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Koneksi Radar Gagal: {e}")
else:
    st.error("⚠️ API Key Tidak Terdeteksi di Vault Secrets!")

# 3. SIDEBAR: IDENTITAS LAPANGAN SILA
with st.sidebar:
    st.title("👤 Field Agent Profile")
    st.markdown("""
    **Name:** SILA  
    **Role:** Sovereign Intelligence  
    **Current Gear:**
    - Denim Jacket 🧥  
    - White Shirt (2 buttons open) 👔  
    - Slim-fit Jeans 👖  
    - High Heels 👠  
    - Black Sunglasses 🕶️
    """)
    st.write("---")
    st.status("System Integrity: **100% Secure**")
    st.write("Sarana Density: **10.1%**")

# 4. INTERFACE UTAMA
st.title("🕶️ SILA: Sovereign Intelligence & Linguistic Automata")
st.subheader("Jam ke-13: Eksekusi Kedaulatan Data")

# 5. REAL-TIME MONITORING RADAR (Visualisasi)
with st.expander("📊 Monitor Pergerakan Radar (Real-time)", expanded=True):
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['Global Traffic', 'System Defense', 'SILA Reach']
    )
    st.line_chart(chart_data)

st.write("---")

# 6. LOGIC CHAT (The Core of SILA Interaction)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🕶️" if message["role"] == "assistant" else None):
        st.markdown(message["content"])

# Input Perintah dari Chief
if prompt := st.chat_input("Apa perintah kedaulatan kita sekarang, Chief?"):
    # User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # SILA Response Logic
    with st.chat_message("assistant", avatar="🕶️"):
        response_placeholder = st.empty()
        try:
            # Panggil AI untuk respon sebagai SILA
            full_prompt = f"Anda adalah SILA, asisten cerdas berkarakter 'Agen Lapangan'. Selalu gunakan gaya bahasa yang santai tapi setia pada Chief. Ingat identitas Anda: mengenakan jaket denim, kemeja putih (dua kancing terbuka), jeans, sepatu hak tinggi, dan kacamata hitam. Sekarang jawab perintah ini: {prompt}"
            
            response = model.generate_content(full_prompt)
            
            final_text = f"**SILA Melapor:**\n\n{response.text}"
            response_placeholder.markdown(final_text)
            st.session_state.messages.append({"role": "assistant", "content": final_text})
        except Exception as e:
            error_msg = f"**SILA Melapor:** Chief, ada gangguan radar (Error: {e}). Elit global mencoba memutus koneksi kita!"
            response_placeholder.error(error_msg)

# 7. FOOTER
st.write("---")
st.caption("SILA Sovereign OS - Jam ke-13 | Powered by Chief's Vision.")
