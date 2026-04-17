import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import re

# --- ADMİN GİRİŞ KONTROLÜ (Hatasız Versiyon) ---
query_params = st.query_params
show_admin_field = query_params.get("admin") == "evet"

if show_admin_field:
    st.markdown("---")
    st.subheader("🔑 Hayalet Yönetici Girişi")
    pass_input = st.text_input("Şifre", type="password")
    if pass_input == st.secrets["admin_password"]:
        st.session_state.page = 'Admin'
        st.success("Tanrı Modu Aktif! Giriş yapılıyor...")
        import time
        time.sleep(1)
        st.rerun()
        
                    

            
# --- 1. TASARIM VE GÖRSEL STİL (UI/UX) ---
def apply_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        font-family: 'Inter', sans-serif;
        color: #e0e0e0;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 25px;
    }
    
    .stButton>button {
        background: rgba(163, 29, 36, 0.7);
        backdrop-filter: blur(5px);
        color: #d4af37;
        border: 1px solid #d4af37;
        padding: 12px 24px;
        border-radius: 12px;
        font-weight: bold;
        transition: 0.3s;
        width: 100%;
    }

    .stButton>button:hover {
        background: #d4af37;
        color: #a31d24;
        transform: translateY(-3px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. VERİTABANI VE İLK KURULUM ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=['id', 'email', 'unvan', 'puan', 'tercihler', 'timestamp'])
if 'page' not in st.session_state:
    st.session_state.page = 'Landing'

# --- 3. LİYAKAT ALGORİTMASI (ENGINE) ---
def placement_engine(users, quotas):
    # Puanı yüksek olan ve erken başvuran önceliklidir
    sorted_users = users.sort_values(by=['puan', 'timestamp'], ascending=[False, True])
    placed_results = {city: [] for city in quotas.keys()}
    final_data = []

    for _, user in sorted_users.iterrows():
        placed = False
        for choice in user['tercihler']:
            if choice in placed_results and len(placed_results[choice]) < quotas[choice]:
                placed_results[choice].append(user['id'])
                final_data.append({**user, 'sonuc': choice})
                placed = True
                break
        if not placed:
            final_data.append({**user, 'sonuc': 'Yerleşemedi'})
    return pd.DataFrame(final_data)

# --- 4. SAYFA FONKSİYONLARI ---
def show_landing():
    st.markdown('<div class="glass-card"><h1 style="text-align:center; color:#d4af37;">🏛️ ASHB TAYİN SİMÜLASYONU v2</h1><p style="text-align:center;">Liyakat esaslı tercih portalına hoş geldiniz.</p></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✨ İlk Kayıt"): st.session_state.page = 'Warning'
    with col2:
        if st.button("🔄 Veri Güncelle"): st.session_state.page = 'Auth'
    with col3:
        if st.button("📊 Analiz Sayfası"): st.session_state.page = 'Analysis'

def show_warning():
    st.markdown('<div class="glass-card"><h3>⚠️ ÖNEMLİ UYARI</h3><p>Bu platform resmi bir kurum sitesi değildir. Etik ilkeler gereği lütfen verilerinizi doğru giriniz. Tayin düşünmüyorsanız sistemi meşgul etmeyiniz.</p></div>', unsafe_allow_html=True)
    agree = st.checkbox("Okudum, anladım ve sorumluluğu kabul ediyorum.")
    if st.button("Devam Et ➡️"):
        if agree: st.session_state.page = 'Info'
        else: st.error("Lütfen uyarıyı onaylayın.")

def show_points():
    st.markdown('<div class="glass-card"><h3>🧮 HİZMET PUANI HESAPLAMA</h3></div>', unsafe_allow_html=True)
    mode = st.toggle("Manuel Gün Girişi Yapmak İstiyorum")
    
    if not mode:
        start_date = st.date_input("Hizmet Başlangıç Tarihi", datetime(2020, 1, 1))
        # 15 Eylül 2026 hedef tarih
        target_date = datetime(2026, 9, 15).date()
        days = (target_date - start_date).days
        st.info(f"Hesaplanan Gün Sayısı: {days}")
    else:
        days = st.number_input("Toplam Gün Sayınız", min_value=0, step=1)

    st.warning("Puanınız son aşamada hesaplanacaktır.")
    if st.button("Tercihlere Geç ➡️"):
        # Örnek katsayı: Gün * 0.005
        st.session_state.temp_puan = days * 0.005
        st.session_state.page = 'Cities'

def show_analysis():
    st.markdown('<div class="glass-card"><h2>📊 GENEL ANALİZ VE SIRALAMA</h2></div>', unsafe_allow_html=True)
    # Örnek Isı Haritası
    fig = px.choropleth(locationmode='country names', locations=['Turkey'], color=[10], color_continuous_scale="Reds")
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("Kendi branşınızdaki sıralamayı görmek için Kontrol Kodunuzu kullanın.")
    if st.button("Ana Menüye Dön"): st.session_state.page = 'Landing'

# --- 5. ANA ÇALIŞTIRICI ---
apply_theme()
if st.session_state.page == 'Landing': show_landing()
elif st.session_state.page == 'Warning': show_warning()
elif st.session_state.page == 'Points': show_points()
elif st.session_state.page == 'Analysis': show_analysis()
