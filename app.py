import streamlit as st
import pandas as pd
import time
from datetime import datetime
import io

# --- 1. SİSTEM VE UI AYARLARI ---
st.set_page_config(page_title="Baho Elite v2", layout="wide")

# Modern Elite Tema (Hız İçin Optimize Edildi)
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #0f0c29, #1a1a2e); color: #e0e0e0; }
    .glass-card { background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 20px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px; }
    .stButton>button { background: rgba(212, 175, 55, 0.1); color: #d4af37; border: 1px solid #d4af37; border-radius: 10px; height: 3.5em; width: 100%; font-weight: bold; }
    .stButton>button:hover { background: #d4af37; color: #0f0c29; }
</style>
""", unsafe_allow_html=True)

# --- 2. SESSION STATE (BELLEK) YÖNETİMİ ---
if 'page' not in st.session_state: st.session_state.page = 'Landing'
if 'unvanlar' not in st.session_state: st.session_state.unvanlar = ["Psikolog", "Sosyal Çalışmacı", "Fizyoterapist"]
if 'kontenjanlar' not in st.session_state: 
    st.session_state.kontenjanlar = pd.DataFrame([
        {"Unvan": "Psikolog", "Şehir": "Ankara", "Kontenjan": 2},
        {"Unvan": "Psikolog", "Şehir": "İzmir", "Kontenjan": 1}
    ])
if 'user_data' not in st.session_state: 
    st.session_state.user_data = pd.DataFrame(columns=['ID', 'Eposta', 'Unvan', 'Puan', 'Tercihler', 'Zaman'])

# --- 3. HAYALET ADMİN GİRİŞİ ---
query_params = st.query_params
if query_params.get("admin") == "evet":
    with st.sidebar:
        st.markdown("### 🔑 Yönetici Girişi")
        pass_input = st.text_input("Şifre", type="password")
        if pass_input == st.secrets.get("admin_password", "B8!h0_E1it3*2026"):
            if st.button("🛠️ ADMİN PANELİNE GİR"):
                st.session_state.page = 'Admin'
                st.rerun()

# --- 4. SAYFA FONKSİYONLARI ---

def show_landing():
    st.markdown('<div class="glass-card"><h1 style="text-align:center; color:#d4af37;">🏛️ ASHB TAYİN SİMÜLASYONU 2026</h1></div>', unsafe_allow_html=True)
    
    # SENİN İSTEDİĞİN 3 BUTON (DOKUNULMADI)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✨ İlk Kayıt"): 
            st.session_state.page = 'Warning'
            st.rerun()
    with col2:
        if st.button("🔄 Veri Güncelle"): 
            st.session_state.page = 'Auth'
            st.rerun()
    with col3:
        if st.button("📊 Analiz Sayfası"): 
            st.session_state.page = 'Analysis'
            st.rerun()

def show_admin():
    st.title("🛠️ Yönetim Paneli (Tanrı Modu)")
    if st.button("⬅️ Ana Sayfaya Dön"):
        st.session_state.page = 'Landing'
        st.rerun()
    
    tab1, tab2, tab3 = st.tabs(["📋 Unvan Yönetimi", "📍 Şehir & Kontenjan", "💾 Veri İşlemleri"])
    
    with tab1:
        st.subheader("Yeni Unvan Ekle")
        yeni_unvan = st.text_input("Unvan Adı")
        if st.button("Unvanı Kaydet"):
            st.session_state.unvanlar.append(yeni_unvan)
            st.success(f"{yeni_unvan} başarıyla eklendi!")
    
    with tab2:
        st.subheader("Şehir ve Kontenjan Düzenleme")
        # Seçilen unvana göre filtreleme
        secilen_u = st.selectbox("Düzenlenecek Unvan", st.session_state.unvanlar)
        temp_df = st.session_state.kontenjanlar[st.session_state.kontenjanlar['Unvan'] == secilen_u]
        
        edited_df = st.data_editor(temp_df, num_rows="dynamic")
        if st.button("Kontenjanları Güncelle"):
            # Basit güncelleme mantığı
            st.session_state.kontenjanlar = pd.concat([
                st.session_state.kontenjanlar[st.session_state.kontenjanlar['Unvan'] != secilen_u],
                edited_df
            ])
            st.success("Değişiklikler kaydedildi!")

    with tab3:
        st.subheader("Verileri İndir ve Yönet")
        if not st.session_state.user_data.empty:
            csv = st.session_state.user_data.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Tüm Verileri CSV Olarak İndir", data=csv, file_name="tayin_verileri.csv", mime="text/csv")
        else:
            st.info("Henüz kayıtlı veri bulunmuyor.")

# --- 5. ANA YÖNLENDİRİCİ ---
if st.session_state.page == 'Landing':
    show_landing()
elif st.session_state.page == 'Admin':
    show_admin()
else:
    # Diğer sayfalar için taslak (Senin eski kodunla birleşecek)
    st.title(f"Sayfa: {st.session_state.page}")
    if st.button("Geri Dön"):
        st.session_state.page = 'Landing'
        st.rerun()
