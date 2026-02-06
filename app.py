import streamlit as st

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Biga MYPIZZATEACHER", layout="centered")

# STYLE CSS SOMBRE PROFESSIONNEL
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
    # Pour correspondre à tes 292g + 55g d'eau (Total 347g pour ~619g de farine)
    hydra_totale = st.slider("Hydratation Totale (%)", 50, 100, 56)
    sel_pct = st.slider("Sel (%)", 0.0, 5.0, 2.5, step=0.1)
    huile_pct = st.slider("Huile (%)", 0.0, 10.0, 3.0, step=0.1)
    
    st.divider()
    st.header("🛠️ Config Biga")
    pct_biga_farine = st.slider("% Biga", 10, 100, 20)
    # Ton ratio d'eau Biga (55g d'eau pour 124g de farine = ~44%)
    pct_eau_biga = 44 

    st.divider()
    st.header("💰 Coût Matières (€/kg)")
    p_farine = st.number_input("Prix Farine", value=1.20)
    p_huile = st.number_input("Prix Huile", value=12.00)

# 3. MOTEUR DE CALCUL INVERSÉ
# On calcule la farine totale pour que le total final (Farine+Eau+Sel+Huile+Levure) = Poids Cible
ratio_total = 1 + (hydra_totale/100) + (sel_pct/100) + (huile_pct/100) + 0.01
farine_totale = (nb_patons * poids_cible) / ratio_total

# PHASE 1 : BIGA (20% de la farine totale)
p_farine_biga = farine_totale * (pct_biga_farine / 100)
p_eau_biga = p_farine_biga * (pct_eau_biga / 100)
p_levure_biga = farine_totale * 0.01

# PHASE 2 : RAFRAÎCHISSEMENT
f_reste = farine_totale - p_farine_biga
eau_totale_necessaire = farine_totale * (hydra_totale / 100)
eau_reste = eau_totale_necessaire - p_eau_biga
p_sel = farine_totale * (sel_pct / 100)
p_huile_g = farine_totale * (huile_pct / 100)

# COÛT
cout_total = ((farine_totale/1000)*p_farine) + ((p_huile_g/1000)*p_huile) + ((eau_totale_necessaire/1000)*0.004)

# 4. AFFICHAGE DES RÉSULTATS
st.markdown(f"### 📊 Recette pour {nb_patons} pâton(s) de {int(poids_cible)}g")
st.write(f"Farine totale à peser : **{farine_totale:.1f} g**")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📦 Phase 1 : Biga (J-1)")
    st.metric("Farine Biga", f"{p_farine_biga:.1f} g")
    st.metric("Eau Biga", f"{p_eau_biga:.1f} g")
    st.metric("Levure Biga", f"{p_levure_biga:.1f} g")

with col2:
    st.subheader("🥣 Phase 2 : Jour J")
    st.metric("Farine à ajouter", f"{f_reste:.1f} g")
    st.metric("Eau à ajouter", f"{eau_reste:.1f} g")
    st.metric("Huile", f"{p_huile_g:.1f} g")
    st.metric("Sel", f"{p_sel:.1f} g")

st.divider()
st.info(f"💰 Coût de revient estimé par pâton : **{(cout_total/nb_patons):.2f} €**")
