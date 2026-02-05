import streamlit as st

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Biga Master - Consultapizza", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #FDF5E6; }
    h1, h2, h3 { color: #8B0000 !important; font-family: 'serif'; }
    [data-testid="stMetricValue"] { color: #8B0000 !important; font-weight: bold; }
    [data-testid="stMetricLabel"] { color: #4B2C20 !important; }
    div[data-testid="stMetric"] { 
        background-color: #FFFFFF; 
        border: 2px solid #8B0000; 
        padding: 15px; 
        border-radius: 10px; 
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🍕 Calculateur Biga Master")
st.write("Méthode paramétrable avec ajustement dynamique de la Biga.")

# 2. BARRE LATÉRALE - PARAMÈTRES RÉGLABLES
with st.sidebar:
    st.header("⚙️ Recette Totale")
    nb_patons = st.number_input("Nombre de pâtons", value=10, min_value=1)
    poids_paton = st.number_input("Poids d'un pâton (g)", value=250, step=10)
    
    st.divider()
    st.subheader("🧪 Ratios Finaux")
    # Modification : Plage de 50% à 100%
    hydra_totale = st.slider("Hydratation Totale (%)", 50, 100, 70)
    sel_pct = st.slider("Sel (%)", 2.0, 3.5, 2.5, step=0.1)
    malt_pct = st.slider("Malt / Sucre (%)", 0.0, 3.0, 1.0, step=0.1)

    st.divider()
    st.subheader("🛠️ Paramétrage Biga")
    pct_farine_biga = st.slider("% de farine en Biga", 10, 100, 30)
    
    # LOGIQUE SPÉCIFIQUE : Si Hydra Totale = 100%, alors Hydra Biga = 55%, sinon 44%
    if hydra_totale == 100:
        hydra_biga_fixe = 55
    else:
        hydra_biga_fixe = 44
    
    levure_biga_fixe = 1 
    st.info(f"Hydra. Biga appliquée : {hydra_biga_fixe}%")

# 3. MOTEUR DE CALCUL
poids_total_cible = nb_patons * poids_paton
farine_totale = poids_total_cible / (1 + (hydra_totale/100) + (sel_pct/100) + (malt_pct/100))

# PHASE 1 : LA BIGA (J-1)
farine_biga = farine_totale * (pct_farine_biga / 100)
eau_biga = farine_biga * (hydra_biga_fixe / 100)
levure_biga = farine_biga * (levure_biga_fixe / 100)

# PHASE 2 : LE RAFRAÎCHISSEMENT (JOUR J)
farine_restante = farine_totale - farine_biga
eau_totale_recette = farine_totale * (hydra_totale / 100)
eau_a_ajouter = eau_totale_recette - eau_biga
sel_total = farine_totale * (sel_pct / 100)
malt_total = farine_totale * (malt_pct / 100)

# 4. AFFICHAGE DES RÉSULTATS
st.header(f"📊 Pour {nb_patons} pâtons de {poids_paton}g")
st.write(f"Cible : {hydra_totale}% d'hydratation (Biga à {hydra_biga_fixe}%)")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Phase 1 : Biga (J-1)")
    st.metric("Farine", f"{int(farine_biga)} g")
    st.metric("Eau", f"{int(eau_biga)} g")
    st.metric("Levure", f"{levure_biga:.2f} g")

with col2:
    st.subheader("🥣 Phase 2 : Jour J")
    st.metric("Farine à rajouter", f"{int(farine_restante)} g")
    st.metric("Eau à rajouter", f"{int(eau_a_ajouter)} g")
    st.metric("Sel", f"{sel_total:.1f} g")
    st.metric("Malt", f"{malt_total:.1f} g")

st.divider()
st.info(f"Farine totale utilisée : {int(farine_totale)} g | Eau totale : {int(eau_totale_recette)} g")
