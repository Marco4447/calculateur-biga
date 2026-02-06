import streamlit as st
import math

# 1. CONFIGURATION
st.set_page_config(page_title="Biga MYPIZZATEACHER", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #E0E0E0; }
    .main-title { text-align: center; color: #FF8C00; font-family: 'Helvetica', sans-serif; font-size: 2.8rem; font-weight: 800; margin-top: -40px; }
    div[data-testid="stMetric"] { background-color: #1E1E1E; border: 1px solid #333; padding: 15px; border-radius: 12px; }
    [data-testid="stMetricValue"] { color: #FF8C00 !important; font-weight: bold; font-size: 1.6rem !important; }
    section[data-testid="stSidebar"] { background-color: #1A1A1A; border-right: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🔥 Biga MYPIZZATEACHER</h1>', unsafe_allow_html=True)

# 2. PARAMÈTRES (SIDEBAR AVEC EXPANDERS)
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

    # DISSOCIATION DES TEMPÉRATURES
    with st.expander("🌡️ Températures & Friction", expanded=True):
        t_amb_biga = st.number_input("Temp. Ambiante J-1 (Biga) (°C)", value=22)
        t_amb_p2 = st.number_input("Temp. Ambiante Jour J (°C)", value=20)
        t_far = st.number_input("Temp. Farine (°C)", value=20)
        t_v1 = st.number_input("Temps V1 (min)", value=18)
        t_v2 = st.number_input("Temps V2 (min)", value=2)
        friction = (t_v1 * 0.5) + (t_v2 * 1.3)

    with st.expander("💰 Coûts de Revient", expanded=False):
        p_farine = st.number_input("Prix Farine (€/kg)", value=1.24)
        p_huile = st.number_input("Prix Huile (€/L)", value=12.00)
        p_sel = st.number_input("Prix Sel (€/kg)", value=0.80)
        p_malt = st.number_input("Prix Malt (€/kg)", value=9.99)
        p_levure = st.number_input("Prix Levure (€/kg)", value=10.00)

# 3. MOTEUR DE CALCUL INVERSÉ
ratio_total = 1 + (hydra_totale/100) + (sel_pct/100) + (huile_pct/100) + ((pct_biga_farine/100) * 0.01)
farine_totale = (nb_patons * poids_cible) / ratio_total

# PHASE 1 : BIGA
p_far_biga = farine_totale * (pct_biga_farine / 100)
p_eau_biga = p_far_biga * 0.44
p_lev_biga = p_far_biga * 0.01 
t_eau_biga = 55 - (t_amb_biga + t_far)

# PHASE 2 : RAFRAÎCHISSEMENT
f_reste = farine_totale - p_far_biga
eau_tot_besoin = farine_totale * (hydra_totale / 100)
eau_reste = eau_tot_besoin - p_eau_biga
p_sel_g = farine_totale * (sel_pct / 100)
p_huile_g = farine_totale * (huile_pct / 100)
# Calcul Température Eau Phase 2 (Base 72 avec Temp Jour J)
t_eau_p2 = 72 - (t_amb_p2 + t_far + friction)

# CALCUL COÛT SÉCURISÉ
c_total = ((farine_totale/1000)*p_farine) + ((p_huile_g/1000)*p_huile) + ((p_sel_g/1000)*p_sel) + ((p_lev_biga/1000)*p_levure)

# 4. AFFICHAGE DES RÉSULTATS
st.markdown(f"### 📊 Recette pour {int(poids_cible)}g")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📦 Phase 1 : Biga")
    st.metric("Farine Biga", f"{math.ceil(p_far_biga)} g")
    st.metric("Eau Biga", f"{math.ceil(p_eau_biga)} g")
    st.metric("Levure Biga", f"{round(p_lev_biga, 1)} g")
    st.metric("Temp. Eau Biga", f"{int(t_eau_biga)} °C")

with col2:
    st.subheader("🥣 Phase 2 : Jour J")
    st.metric("Farine à ajouter", f"{math.ceil(f_reste)} g")
    st.metric("Eau à ajouter", f"{math.ceil(eau_reste)} g")
    st.metric("Sel / Huile", f"{math.ceil(p_sel_g + p_huile_g)} g")
    st.metric("Temp. Eau idéale", f"{int(t_eau_p2)} °C")

st.divider()
st.success(f"💰 Coût de revient par pâton : **{(c_total/nb_patons):.2f} €** | Friction : **+{friction:.1f}°C**")
