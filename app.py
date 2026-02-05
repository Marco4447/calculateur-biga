import streamlit as st

# 1. CONFIGURATION
st.set_page_config(page_title="Biga MYPIZZATEACHER", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #E0E0E0; }
    .main-title { text-align: center; color: #FF8C00; font-family: 'Helvetica', sans-serif; font-size: 2.8rem; font-weight: 800; margin-top: -40px; }
    .sub-title { text-align: center; color: #BBBBBB; font-style: italic; margin-bottom: 2rem; }
    div[data-testid="stMetric"] { background-color: #1E1E1E; border: 1px solid #333; padding: 20px; border-radius: 12px; }
    [data-testid="stMetricValue"] { color: #FF8C00 !important; font-weight: bold; }
    [data-testid="stMetricLabel"] { color: #AAAAAA !important; }
    section[data-testid="stSidebar"] { background-color: #1A1A1A; border-right: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🔥 Biga MYPIZZATEACHER</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Calculateur de précision MYPIZZATEACHER</p>', unsafe_allow_html=True)

# 2. PARAMÈTRES (SIDEBAR)
with st.sidebar:
    st.header("🍕 Base de Farine")
    nb_patons = st.number_input("Nombre de pâtons", value=10, min_value=1)
    farine_par_paton = st.number_input("Farine par pâton (g)", value=150, step=10)
    
    st.divider()
    st.header("🧪 Ratios Recette")
    hydra_totale_pct = st.slider("Hydratation Totale (%)", 50, 100, 56)
    sel_pct = st.slider("Sel (%)", 0.0, 5.0, 2.5, step=0.1)
    huile_pct = st.slider("Huile (%)", 0.0, 10.0, 3.0, step=0.1)
    
    # Choix exclusif entre 0.5% et 1% pour le malt
    malt_pct = st.radio("Malt / Sucre (%)", options=[0.5, 1.0], index=1, horizontal=True)
    
    st.divider()
    st.header("🛠️ Config Biga")
    pct_biga_farine = st.slider("% Biga (sur Farine Totale)", 10, 100, 100)
    
    # RÈGLE MARCO : Si Biga 100% -> Hydra 55%. Sinon 44%.
    pct_biga_eau = 55 if pct_biga_farine == 100 else 44
    pct_biga_levure = 1

# 3. MOTEUR DE CALCUL (LOGIQUE FARINE TOTALE DIRECTE)
# La farine totale est la base de tout
farine_totale = nb_patons * farine_par_paton

# Phase 1 : Biga (calculée sur la farine totale)
p_farine_biga = farine_totale * (pct_biga_farine / 100)
p_eau_biga = farine_totale * (pct_biga_eau / 100)
p_levure_biga = farine_totale * (pct_biga_levure / 100)

# Phase 2 : Rafraîchissement
f_reste = farine_totale - p_farine_biga
eau_totale_cible = farine_totale * (hydra_totale_pct / 100)
eau_reste = eau_totale_cible - p_eau_biga
p_sel = farine_totale * (sel_pct / 100)
p_huile = farine_totale * (huile_pct / 100)
p_malt = farine_totale * (malt_pct / 100)

# 4. AFFICHAGE DES RÉSULTATS
st.markdown(f"### 📊 Pour {nb_patons} pâtons (Base {farine_totale}g farine)")
st.write(f"Configuration : Biga **{pct_biga_farine}%** | Eau Biga **{pct_biga_eau}%**")

c1, c2 = st.columns(2)
with c1:
    st.subheader("📦 Phase 1 : Biga (J-1)")
    st.metric("Farine Biga", f"{int(p_farine_biga)} g")
    st.metric("Eau Biga", f"{int(p_eau_biga)} g")
    st.metric("Levure (1%)", f"{int(p_levure_biga)} g")

with c2:
    st.subheader("🥣 Phase 2 : Jour J")
    st.metric("Farine à ajouter", f"{int(max(0, f_reste))} g")
    st.metric("Eau à ajouter", f"{int(eau_reste)} g")
    st.metric("Sel & Huile", f"{int(p_sel + p_huile)} g")
    st.metric("Malt", f"{p_malt:.1f} g")

st.divider()
poids_total_pate = farine_totale + eau_totale_cible + p_sel + p_huile + p_malt
poids_par_paton = poids_total_pate / nb_patons
st.info(f"⚖️ Poids total : **{int(poids_total_pate)}g** | Soit environ **{int(poids_par_paton)}g** par pâton.")
