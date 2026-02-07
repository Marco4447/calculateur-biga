import streamlit as st
import math

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Calculateur Biga - MYPIZZATEACHER", layout="centered")

# STYLE CSS SIMPLIFIÉ (Look Lione)
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    .main-title { 
        text-align: center; color: #D4ED31; font-family: 'Helvetica', sans-serif; 
        font-size: 2.5rem; font-weight: 900; text-transform: uppercase;
    }
    div[data-testid="stMetric"] { 
        background-color: #111111; border: 2px solid #D4ED31; padding: 15px; 
    }
    [data-testid="stMetricValue"] { color: #D4ED31 !important; }
    .site-button {
        background-color: #FF00FF; color: black; padding: 12px; 
        text-align: center; font-weight: bold; text-decoration: none; 
        display: block; border: 2px solid #000; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. BARRE LATÉRALE (Bouton + Réglages)
with st.sidebar:
    # Bouton de retour au site
    st.markdown('<a href="https://mypizzateacher.com" target="_blank" class="site-button">⬅️ RETOUR AU SITE</a>', unsafe_allow_html=True)
    
    st.header("⚙️ RÉGLAGES")
    nb_patons = st.number_input("Nombre de pâtons", value=90)
    poids_paton = st.number_input("Poids d'un pâton (g)", value=280)
    
    st.subheader("🧪 PARAMÈTRES")
    hydra_totale = st.slider("Hydratation totale (%)", 50, 100, 56)
    pct_biga = st.slider("% de Biga souhaité", 10, 100, 100)
    
    st.subheader("🌡️ TEMPÉRATURES")
    t_amb = st.number_input("Température Ambiante (°C)", value=20)
    t_far = st.number_input("Température Farine (°C)", value=20)

# 3. CALCULS SIMPLIFIÉS
# On calcule la masse totale nécessaire
poids_total_pate = nb_patons * poids_paton
# Ratio simplifié pour trouver la farine totale (Farine + Eau + Sel + Huile)
farine_totale = poids_total_pate / (1 + (hydra_totale/100) + 0.055) # 0.055 approx sel/huile

# Phase 1 : Biga
farine_biga = farine_totale * (pct_biga / 100)
eau_biga = farine_biga * 0.44
levure_biga = farine_biga * 0.01
t_eau_biga = 55 - (t_amb + t_far + 2) # Base 55 pour la Biga

# Phase 2 : Rafraîchi
farine_reste = farine_totale - farine_biga
eau_reste = (farine_totale * (hydra_totale / 100)) - eau_biga

# 4. AFFICHAGE
st.markdown('<h1 class="main-title">🧪 CALCULATEUR BIGA</h1>', unsafe_allow_html=True)
st.write(f"### Recette pour {nb_patons} pâtons de {poids_paton}g")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🟢 PHASE 1 : BIGA")
    st.metric("Farine", f"{math.ceil(farine_biga)} g")
    st.metric("Eau (44%)", f"{math.ceil(eau_biga)} g")
    st.metric("Levure Fraîche", f"{levure_biga:.1f} g")
    st.metric("Temp. Eau", f"{int(t_eau_biga)} °C")

with col2:
    st.subheader("🔵 PHASE 2 : JOUR J")
    st.metric("Farine à ajouter", f"{math.ceil(farine_reste)} g")
    st.metric("Eau à ajouter", f"{math.ceil(eau_reste)} g")
    st.metric("Sel (2.5%)", f"{math.ceil(farine_totale * 0.025)} g")
    st.metric("Huile (3%)", f"{math.ceil(farine_totale * 0.03)} g")

st.divider()
st.success("🎯 **CONSEIL EXPERT :** Laisse ta Biga fermenter 16h à 18h entre 18°C et 20°C pour un résultat optimal.")
