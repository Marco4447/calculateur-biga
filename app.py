import streamlit as st

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Calculateur Biga MYPIZZATEACHER", layout="centered")

# 2. DESIGN SOMBRE PROFESSIONNEL (CSS CUSTOM)
st.markdown("""
    <style>
    /* Fond général sombre */
    .stApp {
        background-color: #121212;
        color: #E0E0E0;
    }
    
    /* Titre principal centré et stylisé */
    .main-title {
        text-align: center;
        color: #FF8C00; /* Orange vibrant */
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        margin-top: -50px;
    }
    
    .sub-title {
        text-align: center;
        color: #BBBBBB;
        font-style: italic;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* Cadres des résultats (Métriques) */
    div[data-testid="stMetric"] {
        background-color: #1E1E1E;
        border: 1px solid #333333;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Couleurs des chiffres et labels */
    [data-testid="stMetricValue"] {
        color: #FF8C00 !important;
        font-weight: bold;
    }
    
    [data-testid="stMetricLabel"] {
        color: #AAAAAA !important;
        font-size: 1rem;
    }

    /* Sidebar stylisée */
    section[data-testid="stSidebar"] {
        background-color: #1A1A1A;
        border-right: 1px solid #333333;
    }
    
    /* Séparateurs */
    hr {
        border-top: 1px solid #333333;
    }
    
    /* Info box personnalisée */
    .stAlert {
        background-color: #262626;
        color: #FF8C00;
        border: 1px solid #FF8C00;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. TITRES
st.markdown('<h1 class="main-title">🔥 Biga Master</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Calculateur Expert MYPIZZATEACHER</p>', unsafe_allow_html=True)

# 4. BARRE LATÉRALE - RÉGLAGES
with st.sidebar:
    st.image("https://img.icons8.com/color/96/pizza.png", width=80)
    st.header("⚙️ Configuration")
    
    nb_patons = st.number_input("Nombre de pâtons", value=10, min_value=1)
    poids_paton = st.number_input("Poids du pâton (g)", value=250, step=10)
    
    st.divider()
    st.subheader("🧪 Ratios Finaux")
    hydra_totale = st.slider("Hydratation Totale (%)", 50, 100, 70)
    sel_pct = st.slider("Sel (%)", 2.0, 3.5, 2.8, step=0.1)
    malt_pct = st.slider("Malt / Sucre (%)", 0.0, 3.0, 1.0, step=0.1)

    st.divider()
    st.subheader("🛠️ Paramétrage Biga")
    pct_farine_biga = st.slider("% de farine en Biga", 10, 100, 30)
    
    # LOGIQUE DYNAMIQUE MYPIZZATEACHER
    if hydra_totale == 100:
        hydra_biga_fixe = 55
    else:
        hydra_biga_fixe = 44
    
    st.write(f"💧 Hydra. Biga : **{hydra_biga_fixe}%**")

# 5. MOTEUR DE CALCUL
poids_total_cible = nb_patons * poids_paton
# Calcul base farine (100%)
farine_totale = poids_total_cible / (1 + (hydra_totale/100) + (sel_pct/100) + (malt_pct/100))

farine_biga = farine_totale * (pct_farine_biga / 100)
eau_biga = farine_biga * (hydra_biga_fixe / 100)
levure_biga = farine_biga * 0.01  # 1% fixe selon Consultapizza

farine_restante = farine_totale - farine_biga
eau_totale_recette = farine_totale * (hydra_totale / 100)
eau_a_ajouter = eau_totale_recette - eau_biga
sel_total = farine_totale * (sel_pct / 100)
malt_total = farine_totale * (malt_pct / 100)

# 6. AFFICHAGE PRINCIPAL
st.markdown(f"### 📊 Pour {nb_patons} pâtons de {poids_paton}g")
st.write(f"Objectif : **{hydra_totale}%** d'hydratation globale.")

c1, c2 = st.columns(2)

with c1:
    st.subheader("📦 Phase 1 : Biga (J-1)")
    st.metric("Farine", f"{int(farine_biga)} g")
    st.metric("Eau", f"{int(eau_biga)} g")
    st.metric("Levure (1%)", f"{levure_biga:.2f} g")

with c2:
    st.subheader("🥣 Phase 2 : Jour J")
    st.metric("Farine", f"{int(farine_restante)} g")
    st.metric("Eau à rajouter", f"{int(eau_a_ajouter)} g")
    st.metric("Sel & Malt", f"{int(sel_total + malt_total)} g")

st.divider()
st.info(f"💾 **Récapitulatif** : Farine totale {int(farine_totale)}g | Eau totale {int(eau_totale_recette)}g")

st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem; margin-top: 50px;">
    © 2026 MYPIZZATEACHER - Tous droits réservés
</div>
""", unsafe_allow_html=True)
