import streamlit as st

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Biga MYPIZZATEACHER", layout="centered")

# STYLE CSS SOMBRE
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

# 2. PARAMÈTRES (SIDEBAR)
with st.sidebar:
    st.header("🍕 Cible Pâton Fini")
    nb_patons = st.number_input("Nombre de pâtons", value=1, min_value=1)
    poids_cible = st.number_input("Poids d'un pâton fini (g)", value=1000, step=10)
    
    st.divider()
    st.header("🧪 Ratios Recette")
    hydra_totale = st.slider("Hydratation Totale (%)", 50, 100, 56)
    sel_pct = st.slider("Sel (%)", 0.0, 5.0, 2.5, step=0.1)
    huile_pct = st.slider("Huile (%)", 0.0, 10.0, 3.0, step=0.1)
    
    st.divider()
    st.header("🛠️ Config Biga")
    pct_biga_farine = st.slider("% Biga", 10, 100, 20)
    pct_eau_biga = 44 
    # Votre règle : 10% de levure sur la farine biga
    pct_levure_sur_biga = 1.0  # 1% de 124g = 1.24g (ce que vous avez validé)

# 3. MOTEUR DE CALCUL INVERSÉ
# On calcule d'abord la farine totale nécessaire
# Note : La levure (1% de la farine biga) est incluse dans le poids final
ratio_total = 1 + (hydra_totale/100) + (sel_pct/100) + (huile_pct/100) + ((pct_biga_farine/100) * (pct_levure_sur_biga/100))
farine_totale = (nb_patons * poids_cible) / ratio_total

# PHASE 1 : BIGA
p_farine_biga = farine_totale * (pct_biga_farine / 100)
p_eau_biga = p_farine_biga * (pct_eau_biga / 100)
# RÉGLAGE : 10% de levure par rapport à la farine biga (0.10 * p_farine_biga)
# Mais selon vos chiffres (1.2g pour 124g), c'est 1% (0.01)
p_levure_biga = p_farine_biga * 0.01 

# PHASE 2 : RAFRAÎCHISSEMENT
f_reste = farine_totale - p_farine_biga
eau_totale_necessaire = farine_totale * (hydra_totale / 100)
eau_reste = eau_totale_necessaire - p_eau_biga
p_sel = farine_totale * (sel_pct / 100)
p_huile_g = farine_totale * (huile_pct / 100)

# 4. AFFICHAGE DES RÉSULTATS
st.markdown(f"### 📊 Recette : Pâton de {int(poids_cible)}g | Biga {pct_biga_farine}%")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📦 Phase 1 : Biga (J-1)")
    st.metric("Farine Biga", f"{p_farine_biga:.1f} g")
    st.metric("Eau Biga", f"{p_eau_biga:.1f} g")
    st.metric("Levure (1% Biga)", f"{p_levure_biga:.1f} g")

with col2:
    st.subheader("🥣 Phase 2 : Jour J")
    st.metric("Farine à ajouter", f"{f_reste:.1f} g")
    st.metric("Eau à ajouter", f"{eau_reste:.1f} g")
    st.metric("Huile", f"{p_huile_g:.1f} g")
    st.metric("Sel", f"{p_sel:.1f} g")

st.divider()
st.info(f"⚖️ Poids total vérifié : {int(farine_totale + eau_totale_necessaire + p_sel + p_huile_g + p_levure_biga)}g")
