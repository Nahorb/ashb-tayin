import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- 1. AYARLAR VE HIZLI YÜKLEME ---
st.set_page_config(page_title="ASHB Tayin 2026", layout="wide")

# CSS'i tek seferde yükleyip hızı artıralım
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #0f0c29, #302b63); color: white; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: rgba(212, 175, 55, 0.2); color: #d4af37; border: 1px solid #d4af37; }
    .stButton>button:hover { background-color: #d4af37; color: #0f0c29; }
</style>
""", unsafe_allow_html=True)

# --- 2. SİSTEM HAFIZASI (SESSION STATE) ---
if 'page' not in st.session_state:
    st.session_state.page = 'Landing'

# --- 3. HAYALET ADMİN GİRİŞİ (HIZLI VE GİZLİ) ---
query_params = st.query_params
if query_params.get("admin") == "evet":
    with st.expander("🔑 Yönetici Girişi", expanded=True):
        pass_input = st.text_input("Şifre", type="password")
        if pass_input == st.secrets["admin_password"]:
            st.session_state.page = 'Admin'
            st.success("Yetki Onaylandı!")
            if st.button("Panele Giriş Yap"):
                st.rerun()

# --- 4. SAYFA FONKSİYONLARI ---
def show_admin_page():
    st.title("🛠️ Tanrı Modu: Yönetim Paneli")
    if st.button("⬅️ Ana Sayfaya Dön"):
        st.session_state.page = 'Landing'
        st.rerun()
    
    st.write("Buradan unvan, şehir ve kontenjanları yönetebilirsin.")
    # İleride buraya veri düzenleme tablolarını ekleyeceğiz.

def show_landing():
    st.header("🏛️ ASHB TAYİN SİMÜLASYONU 2026")
    st.write("Liyakat esaslı yerleştirme simülatörü.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✨ Yeni Kayıt Oluştur"):
            st.session_state.page = 'Form'
            st.rerun()
    with col2:
        if st.button("📊 Analizleri Görüntüle"):
            st.session_state.page = 'Analysis'
            st.rerun()

# --- 5. ANA YÖNLENDİRİCİ (ROUTING) ---
if st.session_state.page == 'Admin':
    show_admin_page()
elif st.session_state.page == 'Landing':
    show_landing()
else:
    st.write("Bu sayfa henüz inşa aşamasında.")
    if st.button("Geri Dön"):
        st.session_state.page = 'Landing'
        st.rerun()
