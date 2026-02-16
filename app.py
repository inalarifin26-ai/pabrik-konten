import streamlit as st
import requests
import json

st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")
st.title("🛡️ SILA: SOVEREIGN OS")

try:
    kunci_api = st.secrets["GOOGLE_API_KEY"]
    # JALUR BYPASS: Menghindari library genai dan langsung ke URL utama
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={kunci_api}"
    
    st.success("✅ DNA Stabil: Jalur Bypass Aktif")

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
            # Request manual ke server Google
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                teks_balasan = response.json()['candidates'][0]['content']['parts'][0]['text']
                st.markdown(teks_balasan)
                st.session_state.messages.append({"role": "assistant", "content": teks_balasan})
            else:
                st.error(f"⚠️ Gangguan Pusat: {response.text}")

except Exception as e:
    st.error(f"⚠️ Masalah Logistik: {e}")
