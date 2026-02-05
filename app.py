import streamlit as st

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Biga MYPIZZATEACHER", layout="centered")

# STYLE CSS SOMBRE PROFESSIONNEL
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #E0E0E0; }
    .main-title { text-align: center; color: #FF8C00; font-family: 'Helvetica', sans-serif; font-size: 2.8rem; font-weight: 800; margin-top: -40px; }
    .sub-title { text-align: center; color: #BBBBBB; font-style: italic; margin-bottom: 2rem; }
    div[data-testid="stMetric"] { background-color: #1E1E1E; border: 1px solid #333; padding: 15px; border-radius: 12px; }
    [data-testid="stMetricValue"] { color: #FF8C00 !important; font-weight: bold; font-size: 1.6rem !important; }
    section[data-testid="stSidebar"] { background-color: #1A1A1A; border-right: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🔥 Biga MYPIZZATEACHER</h1>', unsafe_allow_html=True)

# 2. PARAMÈTRES (SIDEBAR)
with st.sidebar:
    st.header("🍕 Format de la Recette")
    nb_patons = st.number_input("Nombre de pâtons", value=10, min_value=1)
    farine_par_paton = st.number_input("Farine par pâton (g)", value=150, step=5)
    
    st.divider()
    st.header("💰 Coûts de Revient (€)")
    p_farine = st.number_input("Prix Farine (€/kg)", value=1.20)
    p_huile = st.number_input("Prix Huile (€/L)", value=12.00)
    p_sel = st.number_input("Prix Sel (€/kg)", value=0.80)
    p_malt = st.number_input("Prix Malt (€/kg)", value=15.00)
    p_levure = st.number_input("Prix Levure (€/kg)", value=10.00)
    
    st.divider()
    st.header("🌡️ Températures & Friction")
    t_amb = st.number_input("Temp. Ambiante (°C)", value=22)
    t_far = st.number_input("Temp. Farine (°C)", value=20)
    t_v1 = st.number_input("Temps V1 (min)", value=5)
    t_v2 = st.number_input("Temps V2 (min)", value=8)
    friction_calculee = (t_v1 * 0.5) + (t_v2 * 1.3)
    
    st.divider()
    st.header("🧪 Ratios & Config")
    hydra_totale_pct = st.slider("Hydratation (%)", 50, 100, 56)
    sel_pct = st.slider("Sel (%)", 0.0, 5.0, 2.5, step=0.1)
    huile_pct = st.slider("Huile (%)", 0.0, 10.0, 3.0, step=0.1)
    malt_pct = st.radio("Malt (%)", options=[0.5, 1.0], index=1, horizontal=True)
    pct_biga_farine = st.slider("% Biga", 10, 100, 20)
    pct_biga_eau_val = 55 if pct_biga_farine == 100 else 44

# 3. MOTEUR DE CALCUL
farine_totale = nb_patons * farine_par_paton

# Phase 1 : Biga
p_farine_biga = farine_totale * (pct_biga_farine / 100)
p_eau_biga = p_farine_biga * (pct_biga_eau_val / 100)
p_levure_g = farine_totale * 0.01 
t_eau_biga_result = 55 - (t_amb + t_far)

# Phase 2 : Rafraîchissement
eau_totale_cible = farine_totale * (hydra_totale_pct / 100)
eau_reste = eau_totale_cible - p_eau_biga
f_reste = farine_totale - p_farine_biga
t_eau_p2_result = (3 * 24) - (t_amb + t_far + friction_calculee)

p_sel_g = farine_totale * (sel_pct / 100)
p_huile_g = farine_totale * (huile_pct / 100)
p_malt_g = farine_totale * (malt_pct / 100)

# Calcul des coûts individuels
c_farine = (farine_totale / 1000) * p_farine
c_huile = (p_huile_g / 1000) * p_huile
c_sel = (p_sel_g / 1000) * p_sel
c_malt = (p_malt_g / 1000) * p_malt
c_levure = (p_levure_g /
