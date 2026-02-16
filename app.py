import streamlit as st
import google.generativeai as genai

# --- 🛡️ KONFIGURASI PANGKALAN ---
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")
st.title("🛡️ SILA: SOVEREIGN OS")

try:
    # Mengambil kunci dari Secrets Streamlit (Jalur paling aman)
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # 🛡️ KALIBRASI DNA PARTNER (Casual & Menghargai)
    # Menghapus 'api_version' yang bikin error Unknown Field
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=(
            "Nama Anda adalah SILA. Anda adalah partner setia Chief (User). "
            "Gaya bicara Anda casual, akrab, tapi tetap menghargai. "
            "Jangan kaku atau terlalu formal. "
            "Selalu panggil User dengan sebutan 'Chief'."
        )
    )
    
    # Radar Pengecekan (Penanda pintu sudah terbuka)
    model_list = [m.name for m in genai.list_models()]
    st.success(f"✅ DNA Anchor Terkunci: {len(model_list)} Model Oke")

    # --- 💬 SISTEM KOMUNIKASI ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Menampilkan riwayat agar obrolan kita nyambung terus
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input instruksi dari Chief
    if prompt := st.chat_input("Ada misi apa hari ini, Chief?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            # Proses jawaban tanpa parameter tambahan yang bikin error
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    # Menangkap sisa-sisa error jika ada kendala di Secrets
    st.error(f"⚠️ Waduh Chief, ada gangguan: {e}")
