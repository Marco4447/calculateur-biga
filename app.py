import streamlit as st

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Biga MYPIZZATEACHER", layout="centered")

# 2. DESIGN SOMBRE PROFESSIONNEL (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #E0E0E0; }
    .main-title { text-align: center; color: #FF8C00; font-family: 'Helvetica', sans-serif; font-size: 2.8rem; font-weight: 800; margin-top: -40px; }
    .sub-title { text-align: center; color: #BBBBBB; font-style: italic; margin-bottom: 2rem; }
    div[data-testid="stMetric"] { background-color: #1E1E1E; border: 1px solid #333; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    [data-testid="stMetricValue"] { color: #FF8C00 !important; font-weight: bold; }
    [data-testid="stMetricLabel"] { color: #AAAAAA !important; }
    section[data-testid="stSidebar"] { background-color: #1A1A1A; border-right: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# TITRES ALIGNÉS
st.markdown('<h1 class="main-title">🔥 Biga MYPIZZATEACHER</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Expertise en fermentations indirectes</p>', unsafe_allow_html=True)

# 3. PARAMÈTRES (SIDEBAR)
with st.sidebar:
    st.header("⚙️ Base Recette")
    farine_totale = st.number_input("Farine Totale (g)", value=1000, step=100)
    hydra_totale_pct = st.slider("Hydratation Totale (%)", 50, 100, 56)
    
    st.divider()
    st.subheader("🛠️ Configuration Biga")
    pct_biga_farine = st.slider("% Biga (sur Farine Totale)", 10, 100, 20)
    
    # RÈGLE DYNAMIQUE : Si Biga = 100%, alors Eau = 55%. Sinon 44%.
    if pct_biga_farine == 100:
        pct_biga_eau = 55
    else:
        pct_biga_eau = 44
    
    pct_biga_levure = 1 # 1% fixe

    st.divider()
    st.subheader("🧂 Phase 2 (Rafraîchissement)")
    sel_pct = st.slider("Sel (%)", 0.0, 5.0, 2.5, step=0.1)
    huile_pct = st.slider("Huile (%)", 0.0, 10.0, 3.0, step=0.1)

# 4. MOTEUR DE CALCUL (LOGIQUE MARCO)
# Phase 1 : Biga (Calculée sur la farine totale)
p_farine_biga = farine_totale * (pct_biga_farine / 100)
p_eau_biga = farine_totale * (pct_biga_eau / 100)
p_levure_biga = farine_totale * (pct_biga_levure / 100)

# Phase 2 : Rafraîchissement
f_reste = farine_totale - p_farine_biga
eau_cible = farine_totale * (hydra_totale_pct / 100)
eau_reste = eau_cible - p_eau_biga
p_sel = farine_totale * (sel_pct / 100)
p_huile = farine_totale * (huile_pct / 100)

# 5. AFFICHAGE DES RÉSULTATS
st.markdown(f"### 📊 Pour {int(farine_totale)}g de farine")
st.write(f"Configuration : Biga **{pct_biga_farine}%** | Eau Biga **{pct_biga_eau}%**")

c1, c2 = st.columns(2)
with c1:
    st.subheader("📦 Phase 1 : Biga (J-1)")
    st.metric("Farine Biga", f"{int(p_farine_biga)} g")
    st.metric("Eau Biga", f"{int(p_eau_biga)} g")
    st.metric("Levure", f"{int(p_levure_biga)} g")

with c2:
    st.subheader("🥣 Phase 2 : Jour J")
    st.metric("Farine à ajouter", f"{int(max(0, f_reste))} g")
    st.metric("Eau à ajouter", f"{int(eau_reste)} g")
    st.metric("Sel", f"{int(p_sel)} g")
    st.metric("Huile", f"{int(p_huile)} g")

st.divider()
poids_total = farine_totale + eau_cible + p_sel + p_huile
st.info(f"⚖️ Poids total de la pâte : **{int(poids_total)} g**")
