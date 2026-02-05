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
st.markdown('<p class="sub-title">Calculateur de précision par nombre de pâtons</p>', unsafe_allow_html=True)

# 2. PARAMÈTRES (SIDEBAR)
with st.sidebar:
    st.header("🍕 Format des Pâtons")
    nb_patons = st.number_input("Nombre de pâtons", value=10, min_value=1)
    poids_unitaire = st.number_input("Poids d'un pâton (g)", value=250, step=10)
    
    st.divider()
    st.header("🧪 Ratios Recette")
    hydra_totale_pct = st.slider("Hydratation Totale (%)", 50, 100, 70)
    sel_pct = st.slider("Sel (%)", 0.0, 5.0, 2.5, step=0.1)
    huile_pct = st.slider("Huile (%)", 0.0, 10.0, 3.0, step=0.1)
    
    st.divider()
    st.header("🛠️ Config Biga")
    pct_biga_farine = st.slider("% Biga (sur Farine Totale)", 10, 100, 20)
    
    # Règle : Si Biga 100%, alors Hydra Biga 55%. Sinon 44%.
    pct_biga_eau = 55 if pct_biga_farine == 100 else 44
    pct_biga_levure = 1

# 3. MOTEUR DE CALCUL INVERSÉ
# On calcule d'abord le poids total de pâte souhaité
poids_pate_total = nb_patons * poids_unitaire

# On déduit la farine totale (Base 100%)
# Formule : Poids Total = Farine * (1 + %Hydra + %Sel + %Huile)
farine_totale = poids_pate_total / (1 + (hydra_totale_pct/100) + (sel_pct/100) + (huile_pct/100))

# Phase 1 : Biga (sur Farine Totale)
p_farine_biga = farine_totale * (pct_biga_farine / 100)
p_eau_biga = farine_totale * (pct_biga_eau / 100)
p_levure_biga = farine_totale * (pct_biga_levure / 100)

# Phase 2 : Rafraîchissement
f_reste = farine_totale - p_farine_biga
eau_cible = farine_totale * (hydra_totale_pct / 100)
eau_reste = eau_cible - p_eau_biga
p_sel = farine_totale * (sel_pct / 100)
p_huile = farine_totale * (huile_pct / 100)

# 4. AFFICHAGE DES RÉSULTATS
st.markdown(f"### 📊 Pour {nb_patons} pâtons de {poids_unitaire}g")
st.write(f"Masse totale : **{int(poids_pate_total)}g** | Farine totale nécessaire : **{int(farine_totale)}g**")

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
    st.metric("Sel & Huile", f"{int(p_sel + p_huile)} g")

st.divider()
st.info(f"💡 Rappel : Biga à **{pct_biga_eau}%** d'hydratation.")
