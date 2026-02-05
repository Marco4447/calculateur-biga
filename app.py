import streamlit as st

# 1. CONFIGURATION
st.set_page_config(page_title="Biga MYPIZZATEACHER", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #E0E0E0; }
    .main-title { text-align: center; color: #FF8C00; font-family: 'Helvetica', sans-serif; font-size: 2.5rem; font-weight: 800; }
    .sub-title { text-align: center; color: #BBBBBB; font-style: italic; margin-bottom: 2rem; }
    div[data-testid="stMetric"] { background-color: #1E1E1E; border: 1px solid #333; padding: 15px; border-radius: 10px; }
    [data-testid="stMetricValue"] { color: #FF8C00 !important; }
    section[data-testid="stSidebar"] { background-color: #1A1A1A; }
    </style>
    """, unsafe_allow_html=True)

# TITRE MIS À JOUR
st.markdown('<h1 class="main-title">🔥 Biga MYPIZZATEACHER</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Logiciel de calcul haute précision</p>', unsafe_allow_html=True)

# 2. PARAMÈTRES (SIDEBAR)
with st.sidebar:
    st.header("⚙️ Base Recette")
    farine_totale = st.number_input("Farine Totale (g)", value=1000, step=100)
    hydra_totale_pct = st.slider("Hydratation Totale (%)", 50, 100, 56)
    
    st.divider()
    st.subheader("🛠️ Configuration Biga")
    pct_biga_farine = st.slider("% Biga (sur Farine Totale)", 10, 100, 20)
    
    # RÈGLE STRICTE : Si Biga = 100%, alors Eau = 55%. Sinon 44%.
    if pct_biga_farine == 100:
        pct_biga_eau = 55
    else:
        pct_biga_eau = 44
    
    pct_biga_levure = 1 # 1% de la farine totale

    st.divider()
    st.subheader("🧂 Phase 2 (Rafraîchissement)")
    sel_pct = st.slider("Sel (%)", 0.0, 5.0, 2.5, step=0.1)
    huile_pct = st.slider("Huile (%)", 0.0, 10.0, 3.0, step=0.1)

# 3. MOTEUR DE CALCUL (LOGIQUE MARCO)
# Phase 1 : Biga (Calculée sur la farine totale)
poids_farine_biga = farine_totale * (pct_biga_farine / 100)
poids_eau_biga = farine_totale * (pct_biga_eau / 100)
poids_levure_biga = farine_totale * (pct_biga_levure / 100)

# Phase 2 : Rafraîchissement
farine_a_ajouter = farine_totale - poids_farine_biga
eau_totale_cible = farine_totale * (hydra_totale_pct / 100)
eau_a_ajouter = eau_totale_cible - poids_eau_biga
poids_sel = farine_totale * (sel_pct / 100)
poids_huile =
