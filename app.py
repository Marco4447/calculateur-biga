import streamlit as st
import math

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Biga MYPIZZATEACHER - Expert", layout="centered")

# STYLE CSS SOMBRE ET PROFESSIONNEL
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #E0E0E0; }
    .main-title { text-align: center; color: #FF8C00; font-family: 'Helvetica', sans-serif; font-size: 2.8rem; font-weight: 800; margin-top: -40px; }
    div[data-testid="stMetric"] { background-color: #1E1E1E; border: 1px solid #333; padding: 15px; border-radius: 12px; }
    [data-testid="stMetricValue"] { color: #FF8C00 !important; font-weight: bold; font-size: 1.6rem !important; }
    section[data-testid="stSidebar"] { background-color: #1A1A1A; border-right: 1px solid #333; }
    .info-box { background-color: #262730; border-left: 5px solid #FF8C00; padding: 15px; border-radius: 5px; margin-top: 10px; }
    .alert-box { background-color: #443311; border-left: 5px solid #FFD700; padding: 15px; border-radius: 5px; margin-top: 10px; }
    .expert-card { background-color: #1E1E1E; border: 1px solid #FF8C00; padding: 20px; border-radius: 10px; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🔥 Biga MYPIZZATEACHER</h1>', unsafe_allow_html=True)

# 2. PARAMÈTRES (SIDEBAR)
with st.sidebar:
    st.header("⚙️ Réglages")
    with st.expander("Poids du pâton", expanded=True):
        nb_patons = st.number_input("Nombre de pâtons", value=1, min_value=1)
        poids_cible = st.number_input("Poids d'un pâton fini (g)", value=1000, step=10)
    
    with st.expander("🧪 Ratios & Config Biga", expanded=False):
        hydra_totale = st.slider("Hydratation totale de l'empattement", 50, 100, 56)
        sel_pct = st.slider("Sel (%)", 0.0, 5.0, 2.5, step=0.1)
        huile_pct = st.slider("Huile (%)", 0.0, 10.0, 3.0, step=0.1)
        pct_biga_farine = st.slider("% de Biga à utiliser dans l'empattement total", 10, 100, 20)

    with st.expander("🌡️ Températures & Friction", expanded=True):
        t_amb_biga = st.number_input("Temp. Ambiante J-1 (Biga) (°C)", value=20)
        t_amb_p2 = st.number_input("Temp. Ambiante Jour J (°C)", value=20)
        t_far = st.number_input("Temp. Farine (°C)", value=20)
        friction_biga = 2.0 
        t_v1 = st.number_input("Temps V1 (min)", value=18)
        t_v2 = st.number_input("Temps V2 (min)", value=2)
        friction_p2 = (t_v1 * 0.5) + (t_v2 * 1.3)

# 3. MOTEUR DE CALCUL
ratio_total = 1 + (hydra_totale/100) + (sel_pct/100) + (huile_pct/100) + ((pct_biga_farine/100) * 0.01)
farine_totale = (nb_patons * poids_cible) / ratio_total
poids_total_kilos = (nb_patons * poids_cible) / 1000

# PHASE 1
p_far_biga = farine_totale * (pct_biga_farine / 100)
p_eau_biga = p_far_biga * 0.44
p_lev_biga = p_far_biga * 0.01 
t_eau_biga = 55 - (t_amb_biga + t
