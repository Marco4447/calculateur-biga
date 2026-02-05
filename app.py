import streamlit as st

# 1. CONFIGURATION
st.set_page_config(page_title="Biga MYPIZZATEACHER", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #E0E0E0; }
    .main-title { text-align: center; color: #FF8C00; font-size: 2.8rem; font-weight: 800; margin-top: -40px; }
    div[data-testid="stMetric"] { background-color: #1E1E1E; border: 1px solid #333; padding: 15px; border-radius: 12px; }
    [data-testid="stMetricValue"] { color: #FF8C00 !important; font-weight: bold; font-size: 1.6rem !important; }
    section[data-testid="stSidebar"] { background-color: #1A1A1A; border-right: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🔥 Biga MYPIZZATEACHER</h1>', unsafe_allow_html=True)

# 2. PARAMÈTRES (SIDEBAR)
with st.sidebar:
    st.header("🍕 Base de Farine")
    nb_patons = st.number_input("Nombre de pâtons", value=10, min_value=1)
    farine_par_paton = st.number_input("Farine par pâton (g)", value=150, step=5)
    
    st.divider()
    st.header("🛠️ Config Biga")
    # LE CURSEUR EST DE RETOUR ICI
    pct_biga_farine = st.slider("% Biga (sur Farine Totale)", 10, 100, 100)
    
    st.divider()
    st.header("🌡️ Températures & Friction")
    t_amb = st.number_input("Temp. Ambiante (°C)", value=22)
    t_far = st.number_input("Temp. Farine (°C)", value=20)
    t_v1 = st.number_input("Temps V1 (min)", value=5)
    t_v2 = st.number_input("Temps V2 (min)", value=10)
    friction_calculee = (t_v1 * 0.5) + (t_v2 * 1.3)
    
    st.divider()
    st.header("🧪 Ratios Recette")
    hydra_totale = st.slider("Hydratation Totale (%)", 50, 100, 70)
    sel_pct = st.slider("Sel (%)", 0.0, 5.0, 2.5, step=0.1)
    huile_pct = st.slider("Huile (%)", 0.0, 10.0, 3.0, step=0.1)
    malt_pct = st.radio("Malt (%)", options=[0.5, 1.0], index=1, horizontal=True)
    
    st.divider()
    st.header("💰 Coûts (€)")
    p_farine = st.number_input("Prix Farine (€/kg)", value=1.20)
    p_huile = st.number_input("Prix Huile (€/L)", value=12.00)

# 3. MOTEUR DE CALCUL
farine_totale = nb_patons * farine_par_paton

# PHASE 1 : BIGA
p_farine_biga = farine_totale * (pct_biga_farine / 100)
p_eau_biga = p_farine_biga * 0.44  # 44% d'eau sur la partie Biga
p_levure = farine_totale * 0.01
t_eau_biga = 55 - (t_amb + t_far)

# PHASE 2 : RAFRAÎCHISSEMENT
f_reste = farine_totale - p_farine_biga
eau_totale = farine_totale * (hydra_totale / 100)
eau_a_ajouter = eau_totale - p_eau_biga
p_sel = farine_totale * (sel_pct / 100)
p_huile = farine_totale * (huile_pct / 100)
p_malt = farine_totale * (malt_pct / 100)
t_eau_p2 = (3 * 24) - (t_amb + t_far + friction_calculee)

# COÛT & POIDS
cout_total = ((farine_totale/1000)*p_farine) + ((p_huile/1000)*p_huile) + ((eau_totale/1000)*0.004)
poids_paton = (farine_totale + eau_totale + p_sel + p_huile + p_malt + p_levure) / nb_patons

# 4. AFFICHAGE
st.markdown(f"### 📊 Résultats | {int(farine_totale)}g de farine | Biga {pct_biga_farine}%")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📦 Phase 1 : Biga (J-1)")
    st.metric("Farine Biga", f"{int(p_farine_biga)} g")
    st.metric("Eau Biga (44%)", f"{int(p_eau_biga)} g")
    st.metric("Levure (1%)", f"{int(p_levure)} g")
    st.metric("Temp. Eau Biga", f"{int(t_eau_biga)} °C")

with col2:
    st.subheader("🥣 Phase 2 : Jour J")
    st.metric("Eau à ajouter", f"{int(eau_a_ajouter)} g")
    st.metric("Temp. Eau idéale", f"{int(t_eau_p2)} °C")
    st.metric("Farine à ajouter", f"{int(max(0, f_reste))} g")
    st.metric("Sel / Huile / Malt", f"{int(p_sel + p_huile + p_malt)} g")

st.divider()
cc1, cc2 = st.columns(2)
cc1.info(f"⚖️ Poids d'un pâton fini : **{int(poids_paton)}g**")
cc2.success(f"💰 Coût de
