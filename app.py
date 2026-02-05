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
    [data-testid="stMetricLabel"] { color: #AAAAAA !important; }
    section[data-testid="stSidebar"] { background-color: #1A1A1A; border-right: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🔥 Biga MYPIZZATEACHER</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Calculateur Expert : Biga & Rafraîchissement</p>', unsafe_allow_html=True)

# 2. PARAMÈTRES (SIDEBAR)
with st.sidebar:
    st.header("🍕 Format de la Recette")
    nb_patons = st.number_input("Nombre de pâtons", value=10, min_value=1)
    farine_par_paton = st.number_input("Farine par pâton (g)", value=150, step=10)
    
    st.divider()
    st.header("🌡️ Températures Ambiantes")
    t_amb = st.number_input("Temp. Ambiante (°C)", value=22)
    t_far = st.number_input("Temp. Farine (°C)", value=20)
    
    st.divider()
    st.header("🌀 Friction Spirale (Phase 2)")
    t_v1 = st.number_input("Temps en Vitesse 1 (min)", value=5, min_value=0)
    t_v2 = st.number_input("Temps en Vitesse 2 (min)", value=8, min_value=0)
    # Calcul friction : 0.5 par min en V1 + 1.3 par min en V2
    friction_calculee = (t_v1 * 0.5) + (t_v2 * 1.3)
    
    st.divider()
    st.header("🧪 Ratios Recette")
    hydra_totale_pct = st.slider("Hydratation Totale (%)", 50, 100, 56)
    sel_pct = st.slider("Sel (%)", 0.0, 5.0, 2.5, step=0.1)
    huile_pct = st.slider("Huile (%)", 0.0, 10.0, 3.0, step=0.1)
    malt_pct = st.radio("Malt / Sucre (%)", options=[0.5, 1.0], index=1, horizontal=True)
    
    st.divider()
    st.header("🛠️ Config Biga")
    pct_biga_farine = st.slider("% Biga (sur Farine Totale)", 10, 100, 100)
    # Règle MYPIZZATEACHER : 55% si Biga 100%, sinon 44%
    pct_biga_eau_val = 55 if pct_biga_farine == 100 else 44

# 3. MOTEUR DE CALCUL
farine_totale = nb_patons * farine_par_paton

# --- PHASE 1 : BIGA ---
p_farine_biga = farine_totale * (pct_biga_farine / 100)
p_eau_biga = farine_totale * (pct_biga_eau_val / 100)
p_levure_biga = farine_totale * 0.01 
t_eau_biga_result = 55 - (t_amb + t_far)

# --- PHASE 2 : RAFRAÎCHISSEMENT ---
f_reste = farine_totale - p_farine_biga
eau_totale_cible = farine_totale * (hydra_totale_pct / 100)
eau_reste = eau_totale_cible - p_eau_biga
t_eau_p2_result = (3 * 24) - (t_amb + t_far + friction_calculee)

p_sel = farine_totale * (sel_pct / 100)
p_huile = farine_totale * (huile_pct / 100)
p_malt = farine_totale * (malt_pct / 100)

# 4. AFFICHAGE DES RÉSULTATS
st.markdown(f"### 📊 Pour {int(farine_totale)}g de farine")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Phase 1 : Biga (J-1)")
    st.metric("Farine Biga", f"{int(p_farine_biga)} g")
    st.metric("Eau Biga", f"{int(p_eau_biga)} g")
    st.metric("Temp. Eau Biga", f"{int(t_eau_biga_result)} °C")
    st.metric("Levure", f"{int(p_levure_biga)} g")

with col2:
    st.subheader("🥣 Phase 2 : Jour J")
    st.metric("Eau à ajouter", f"{int(eau_reste)} g")
    st.metric("Temp. Eau idéale", f"{int(t_eau_p2_result)} °C")
    st.metric("Farine à ajouter", f"{int(max(0, f_reste))} g")
    st.metric("Sel", f"{p_sel:.1f} g")
    st.metric("Huile", f"{p_huile:.1f} g")
    st.metric("Malt", f"{p_malt:.1f} g")

st.divider()
poids_final = farine_totale + eau_totale_cible + p_sel + p_huile + p_malt
st.info(f"⚖️ Poids total : **{int(poids_final)}g** | Friction : **+{friction_calculee:.1f}°C**")
