import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import time
import re
import uuid

# --- 1. SİSTEM AYARLARI ---
st.set_page_config(page_title="Baho Elite v2", layout="wide")

# CSS: Karanlık Mod ve Gold Detaylar (Performans Odaklı)
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #0e1117; color: #ffffff; }
    .stButton>button { border-radius: 8px; height: 3em; transition: 0.3s; font-weight: bold; }
    .glass-card { background: rgba(255, 255, 255, 0.03); padding: 20px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1); }
</style>
""", unsafe_allow_html=True)

# --- 2. YARDIMCI FONKSİYONLAR (MOTOR) ---
def send_email(receiver_email, unique_id):
    try:
        msg = MIMEText(f"Baho Elite v2 Sistemine Kaydınız Alınmıştır.\n\nKontrol Kodunuz: {unique_id}\n\nBu kod ile bilgilerinizi güncelleyebilir ve sıralamanızı takip edebilirsiniz.")
        msg['Subject'] = 'ASHB Tayin Kontrol Kodunuz'
        msg['From'] = st.secrets["gmail_user"]
        msg['To'] = receiver_email
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(st.secrets["gmail_user"], st.secrets["gmail_password"])
            server.sendmail(st.secrets["gmail_user"], receiver_email, msg.as_string())
        return True
    except Exception as e:
        st.error(f"Mail Hatası: {e}")
        return False

# --- 3. SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = 'Landing'

# --- 4. HAYALET ADMİN (GİZLİ URL) ---
if st.query_params.get("admin") == "evet":
    with st.sidebar:
        st.subheader("🔑 Admin Yetkilendirme")
        if st.text_input("Şifre", type="password") == st.secrets["admin_password"]:
            if st.button("🛠️ PANELİ AÇ"): 
                st.session_state.page = 'Admin'
                st.rerun()

# --- 5. SAYFA İÇERİKLERİ ---

def show_landing():
    st.markdown('<div class="glass-card"><h1 style="text-align:center; color:#d4af37;">🏛️ ASHB TAYİN SİMÜLASYONU 2026</h1><p style="text-align:center;">Liyakat esaslı veri tabanı ve analiz platformu</p></div>', unsafe_allow_html=True)
    st.write(" ")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✨ İlk Kayıt"): 
            st.session_state.page = 'Warning'
            st.rerun()
    with col2:
        if st.button("🔄 Veri Güncelle"): 
            st.session_state.page = 'Update'
            st.rerun()
    with col3:
        if st.button("📊 Analiz Sayfası"): 
            st.session_state.page = 'Analysis'
            st.rerun()

def show_admin():
    st.title("🛠️ Yönetim Paneli")
    if st.button("⬅️ Ana Sayfaya Dön"):
        st.session_state.page = 'Landing'
        st.rerun()
    
    tab1, tab2, tab3 = st.tabs(["📝 İçerik Yönetimi", "🏘️ Şehir & Kontenjan", "📊 Veri İndirme"])
    with tab1:
        st.info("Buradan sitedeki duyuru ve metinleri güncelleyebilirsiniz.")
    with tab3:
        st.download_button("📥 Tüm Verileri Excel (CSV) Olarak İndir", data="ID,Email,Puan\n1,test@test.com,55.4", file_name="tayin_listesi.csv")

# --- 6. ANA YÖNLENDİRİCİ ---
if st.session_state.page == 'Landing': show_landing()
elif st.session_state.page == 'Admin': show_admin()
elif st.session_state.page == 'Warning':
    st.warning("Bu platform resmi bir kurum sitesi değildir.")
    if st.button("Okudum, Devam Et"):
        st.session_state.page = 'Form'
        st.rerun()
elif st.session_state.page == 'Form':
    st.subheader("Kayıt Formu")
    email = st.text_input("E-posta Adresiniz")
    if st.button("Kaydı Tamamla"):
        u_id = str(uuid.uuid4())[:8].upper()
        if send_email(email, u_id):
            st.success(f"Kayıt başarılı! Kontrol kodunuz e-posta adresinize gönderildi: {u_id}")
            time.sleep(2)
            st.session_state.page = 'Landing'
            st.rerun()
