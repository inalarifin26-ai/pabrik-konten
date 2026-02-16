import streamlit as st
import google.generativeai as genai

# --- CONFIG ---
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")

# Masukkan API KEY BARU Chief di sini
#
genai.configure(api_key="AIzaSyDN6n3p9xSj2PCj6-ZSCr9cCDIt5h7sAjA")

# Gunakan model tanpa tambahan parameter rumit
model = genai.GenerativeModel('gemini-1.5-flash')

# --- UI ---
st.title("🛡️ SILA: SOVEREIGN OS")
st.info("🛰️ **STATUS SYSTEM:** DNA ANCHOR ACTIVE")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAT ---
if prompt := st.chat_input("Apa perintah Anda, Chief?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Panggilan langsung ke saraf pusat
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"⚠️ Terjadi kendala: {e}")
