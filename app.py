import streamlit as st

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Calculateur Biga MYPIZZATEACHER", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #FDF5E6; }
    
    /* Alignement du titre et du sous-titre au centre */
    .main-title {
        text-align: center;
        color: #8B0000;
        font-family: 'serif';
        font-size: 3rem;
        margin-bottom: 0;
    }
    .sub-title {
        text-align: center;
        color: #4B2C20;
        font-style: italic;
        margin-bottom: 2rem;
    }
    
    h2, h3 { color: #8B0000 !important; font-family: 'serif'; }
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

# TITRES ALIGNÉS
st.markdown('<h1 class="main-title">🍕 Calculateur Biga MYPIZZATEACHER</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Expertise en fermentations indirectes et hydratations poussées</p>', unsafe_allow_html=True)

# 2. BARRE LATÉRALE - PARAMÈTRES RÉGLABLES
with st.sidebar:
    st.header("⚙️ Recette Totale")
    nb_patons = st.number_input("Nombre de pâtons", value=10, min_value=1)
    poids_paton = st.number_input("Poids d'un pâton (g)", value=250, step=10)
    
    st.divider()
    st.subheader("🧪 Ratios Finaux")
    hydra_totale = st.slider("Hydratation Totale (%)", 50, 100, 70)
    sel_pct = st.slider("Sel (%)", 2.0, 3.5, 2.5, step=0.1)
    malt_pct = st.slider("Malt / Sucre (%)", 0.0, 3.0, 1.0, step=0.1)

    st.divider()
    st.subheader("🛠️ Paramétrage Biga")
    pct_farine_biga = st.slider("% de farine en Biga", 10, 100, 30)
    
    if hydra_totale == 100:
        hydra_biga_fixe = 55
    else:
        hydra_biga_fixe = 44
    
    levure_biga_fixe = 1 
    st.info(f"Hydra. Biga appliquée : {hydra_biga_fixe}%")

# 3. MOTEUR DE CALCUL
poids_total_cible = nb_patons * poids_paton
farine_totale = poids_total_cible / (1 + (hydra_totale/100) + (sel_pct/100) + (malt_pct/100))

farine_biga = farine_totale * (pct_farine_biga / 100)
eau_biga = farine_biga * (hydra_biga_fixe / 100)
levure_biga = farine_biga * (levure_biga_fixe / 100)

farine_restante = farine_totale - farine_biga
eau_totale_recette = farine_totale * (hydra_totale / 100)
eau_a_ajouter = eau_totale_recette - eau_biga
sel_total = farine_totale * (sel_pct / 100)
