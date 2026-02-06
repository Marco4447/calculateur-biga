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

# 2. PARAMÈTRES (SIDEBAR AVEC FLÈCHES)
with st.sidebar:
    st.header("⚙️ Réglages")

    # MENU DÉROULANT 1
    with st.expander("🍕 Format de la Recette", expanded=True):
        nb_patons = st.number_input("Nombre de pâtons", value=1, min_value=1)
        poids_cible = st.number_input("Poids d'un pâton fini (g)", value=1000, step=10)
    
    # MENU DÉROULANT 2
    with st.expander("🧪 Ratios & Config Biga", expanded=False):
        hydra_totale = st.slider("Hydratation Totale (%)", 50, 100, 56)
        sel_pct = st.slider("Sel (%)", 0.0, 5.0, 2.5, step=0.1)
        huile_pct = st.slider("Huile (%)", 0.0, 10.0, 3.0, step=0.1)
        pct_biga_farine = st.slider("% Biga", 10, 100, 20)
        pct_eau_biga = 44 

    # MENU DÉROULANT 3
    with st.expander("💰 Coûts de Revient", expanded=False):
        p_farine = st.number_input("Prix Farine (€/kg)", value=1.20)
        p_huile = st.number_input("Prix Huile (€/L)", value=12.00)
        p_sel = st.number_input("Prix Sel (€/kg)", value=0.80)
        p_malt = st.number_input("Prix Malt (€/kg)", value=15.00)
        p_levure = st.number_input("Prix Levure (€/kg)", value=10.00)

# 3. MOTEUR DE CALCUL INVERSÉ
# Ratio = 1(Farine) + Hydra + Sel + Huile + Levure(1% de la partie Biga)
ratio_total = 1 + (hydra_totale/100) + (sel_pct/100) + (huile_pct/100) + ((pct_biga_farine/100) * 0.01)
farine_totale = (nb_patons * poids_cible) / ratio_total

# PHASE 1 : BIGA
p_far_biga = farine_totale * (pct_biga_farine / 100)
p_eau_biga = p_far_biga * (pct_eau_biga / 100)
p_lev_biga = p_far_biga * 0.01 

# PHASE 2 : RAFRAÎCHISSEMENT
f_reste = farine_totale - p_far_biga
eau_tot_besoin = farine_totale * (hydra_totale / 100)
eau_reste = eau_tot_besoin - p_eau_biga
p_sel = farine_totale * (sel_pct / 100)
p_huile = farine_totale * (huile_pct / 100)

# 4. AFFICHAGE DES RÉSULTATS (AVEC ARRONDI SUPÉRIEUR)
st.markdown(f"### 📊 Recette pour {int(poids_cible)}g")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📦 Phase 1 : Biga")
    st.metric("Farine Biga", f"{math.ceil(p_far_biga)} g")
    st.metric("Eau Biga", f"{math.ceil(p_eau_biga)} g")
    st.metric("Levure Biga", f"{round(p_lev_biga, 1)} g")

with col2:
    st.subheader("🥣 Phase 2 : Jour J")
    st.metric("Farine à ajouter", f"{math.ceil(f_reste)} g")
    st.metric("Eau à ajouter", f"{math.ceil(eau_reste)} g")
    st.metric("Huile", f"{math.ceil(p_huile)} g")
    st.metric("Sel", f"{math.ceil(p_sel)} g")

st.divider()
# CALCUL DU COÛT POUR L'INFO BOX
cout_tot = ((farine_totale/1000)*p_farine) + ((p_huile/1000)*p_huile) + ((eau_tot_besoin/1000)*0.004)
st.success(f"💰 Coût de revient par pâton : **{(cout_tot/nb_patons):.2f} €**")
