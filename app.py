import streamlit as st

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Biga Master - Consultapizza", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #FDF5E6; color: #4B2C20; }
    h1, h2, h3 { color: #8B0000 !important; font-family: 'serif'; }
    .stMetric { background-color: #FFFFFF; border: 2px solid #8B0000; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍕 Calculateur Biga Master")
st.write("Méthode indirecte basée sur les standards *Consultapizza*.")

# 2. BARRE LATÉRALE - PARAMÈTRES RÉGLABLES
with st.sidebar:
    st.header("⚙️ Recette Totale")
    nb_patons = st.number_input("Nombre de pâtons", value=10, min_value=1)
    poids_paton = st.number_input("Poids d'un pâton (g)", value=250, step=10)
    
    st.divider()
    st.subheader("🧪 Ratios Finaux")
    hydra_totale = st.slider("Hydratation Totale (%)", 60, 80, 70)
    sel_pct = st.slider("Sel (%)", 2.0, 3.5, 2.5, step=0.1)
    malt_pct = st.slider("Malt / Sucre (%)", 0.0, 3.0, 1.0, step=0.1)

    st.divider()
    st.subheader("🛠️ Paramétrage Biga")
    # Proportion de farine utilisée pour la Biga (votre fameux x %)
    pct_farine_biga = st.slider("% de farine en Biga", 10, 100, 30)
    
    # Ratios fixes de la méthode Consultapizza
    hydra_biga_fixe = 44 
    levure_biga_fixe = 1 

# 3. MOTEUR DE CALCUL
poids_total_cible = nb_patons * poids_paton
# Calcul de la farine totale nécessaire (Base 100%)
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
st.info(f"Masse totale : {int(poids_total_cible)}g  |  Farine totale : {int(farine_totale)}g")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Phase 1 : Biga (J-1)")
    st.write(f"Mélanger grossièrement (**{pct_farine_biga}%** de la farine).")
    st.metric("Farine (W300+)", f"{int(farine_biga)} g")
    st.metric("Eau (44%)", f"{int(eau_biga)} g")
    st.metric("Levure Fraîche (1%)", f"{levure_biga:.2f} g")

with col2:
    st.subheader("🥣 Phase 2 : Jour J")
    st.write("Ajouter à la biga fermentée.")
    st.metric("Farine restante", f"{int(farine_restante)} g")
    st.metric("Eau à rajouter", f"{int(eau_a_ajouter)} g")
    st.metric("Sel", f"{sel_total:.1f} g")
    st.metric("Malt", f"{malt_total:.1f} g")

st.divider()
st.subheader("💡 Rappels Techniques")
st.markdown("""
- **Biga :** Ne pas pétrir. Le mélange doit rester grumeleux (aspect pop-corn).
- **Fermentation :** 16h à 24h à une température constante de 18°C.
- **Pétrissage final :** Briser la biga avec une partie de l'eau avant d'ajouter le reste.
""")
