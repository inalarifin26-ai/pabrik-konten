import streamlit as st
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, firestore
import json
from datetime import datetime

# --- 1. SETUP FIREBASE & GEMINI ---
if not firebase_admin._apps:
    try:
        key_dict = json.loads(st.secrets["FIREBASE_JSON"])
        cred = credentials.Certificate(key_dict)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Error Firebase: {e}")
db = firestore.client()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="NOFA FACTORY | AI Studio", layout="wide")

# --- 2. AI STUDIO CUSTOM CSS ---
st.markdown("""
    <style>
    /* Font & Background */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #fcfcfc; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #eee; padding-top: 2rem; }
    
    /* Card UI */
    .stat-card {
        background: white; padding: 1.5rem; border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        border-bottom: 4px solid #fbbf24; margin-bottom: 1rem;
    }
    
    /* Button AI Studio Look */
    .stButton>button {
        width: 100%; background-color: #fbbf24; color: #000;
        font-weight: 700; border: none; border-radius: 8px;
        padding: 0.6rem; transition: all 0.3s;
    }
    .stButton>button:hover { background-color: #f59e0b; transform: translateY(-2px); }
    
    /* Text Area */
    .stTextArea textarea { border-radius: 10px; border: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.markdown("<h1 style='text-align: center; color: #fbbf24;'>🏭 NOFA</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; font-size: 0.8rem;'>V.2.0 - AI CONTENT ENGINE</p>", unsafe_allow_html=True)
st.sidebar.divider()

menu = ["Login", "Daftar Akun Baru", "Profile & Referral", "Beli Koin"]
choice = st.sidebar.selectbox("🚀 NAVIGASI", menu)

today_date = datetime.now().strftime("%Y-%m-%d")

# --- 4. LOGIKA DAFTAR ---
if choice == "Daftar Akun Baru":
    st.markdown("## 📝 New Creator Registration")
    col1, col2 = st.columns([1, 1])
    with col1:
        new_user = st.text_input("Username ID")
        ref_by = st.text_input("Referral Code (Optional)")
        if st.button("Create Account"):
            user_ref = db.collection('user').document(new_user)
            if user_ref.get().exists:
                st.error("ID already taken!")
            else:
                user_ref.set({
                    'saldo': 250, 'terakhir_akses': today_date,
                    'level': 1, 'referred_by': ref_by if ref_by else None,
                    'total_komisi': 0
                })
                st.success("Account Created! Please Login.")

# --- 5. LOGIKA LOGIN & DASHBOARD ---
elif choice == "Login":
    st.markdown("## 🔑 Studio Access")
    user_id = st.text_input("Enter your Creator ID", value="")
    
    if user_id:
        user_ref = db.collection('user').document(user_id)
        doc = user_ref.get()

        if doc.exists:
            user_data = doc.to_dict()
            saldo = user_data.get('saldo', 0)
            
            # SIDEBAR STATS
            st.sidebar.markdown(f"""
                <div class="stat-card">
                    <p style='margin:0; font-size:0.8rem; color:gray;'>CURRENT BALANCE</p>
                    <h2 style='margin:0; color:#fbbf24;'>🪙 {saldo} Poin</h2>
                </div>
            """, unsafe_allow_html=True)
            
            # MAIN STUDIO
            st.markdown(f"### 🤖 Welcome back, {user_id}!")
            topik = st.text_area("What's on your mind? (AI will craft the content for you)", height=150)
            
            col_a, col_b = st.columns([1, 4])
            with col_a:
                if st.button("⚡ GENERATE"):
                    if saldo >= 50:
                        with st.spinner('AI is cooking your content...'):
                            response = model.generate_content(topik)
                            st.session_state.hasil = response.text
                            user_ref.update({'saldo': saldo - 50})
                            st.rerun()
                    else:
                        st.error("Insufficent Balance!")
            
            if 'hasil' in st.session_state:
                st.divider()
                st.markdown("### ✨ AI Generated Result")
                st.info(st.session_state.hasil)
                st.caption("Content saved to vault automatically.")
        else:
            st.error("User ID not found.")

# --- 6. PROFILE & REFERRAL (AI STUDIO STYLE) ---
elif choice == "Profile & Referral":
    st.markdown("## 👤 Creator Hub")
    user_id_check = st.text_input("Verify ID to see stats")
    if user_id_check:
        u_doc = db.collection('user').document(user_id_check).get()
        if u_doc.exists:
            d = u_doc.to_dict()
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"<div class='stat-card'><b>Referral Level</b><br><h2>⭐ {d.get('level', 1)}</h2></div>", unsafe_allow_html=True)
            with col2:
                # Logika komisi progresif
                komisi = 5 if d.get('level', 1) == 1 else 20
                st.markdown(f"<div class='stat-card'><b>Commision Rate</b><br><h2>📈 {komisi}%</h2></div>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<div class='stat-card'><b>Total Earnings</b><br><h2>💰 Rp {d.get('total_komisi', 0)}</h2></div>", unsafe_allow_html=True)
            
            st.success(f"Your Referral Code: **{user_id_check}**")

# --- 7. PRICELIST ---
elif choice == "Beli Koin":
    st.markdown("## 🪙 Fuel Your Creativity")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='stat-card'><h3>Starter</h3><p>150 Poin</p><h4>Rp 15.000</h4></div>", unsafe_allow_html=True)
        st.button("Buy Starter", key="b1")
    with col2:
        st.markdown("<div class='stat-card'><h3>Pro</h3><p>600 Poin</p><h4>Rp 50.000</h4></div>", unsafe_allow_html=True)
        st.button("Buy Pro", key="b2")
    with col3:
        st.markdown("<div class='stat-card'><h3>Enterprise</h3><p>1.500 Poin</p><h4>Rp 100.000</h4></div>", unsafe_allow_html=True)
        st.button("Buy Enterprise", key="b3")
