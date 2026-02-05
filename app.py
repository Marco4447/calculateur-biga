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
    st.header("🍕 Cible Pâton Fini")
    nb_patons = st.number_input("Nombre de pâtons", value=1, min_value=1)
    # L'utilisateur entre ici le poids réel du pâton qu'il veut en main
    poids_paton_fini = st.number_input("Poids d'un pâton fini (g)", value=1000, step=10)
    
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
    st.header("🛠️ Config Biga")
    pct_biga_farine = st.slider("% Biga (sur Farine Totale)", 10, 100, 100)
    
    st.divider()
    st.header("💰 Coûts (€)")
    p_farine = st.number_input("Prix Farine (€/kg)", value=1.20)
    p_huile = st.number_input("Prix Huile (€/L)", value=12.00)

# 3. MOTEUR DE CALCUL INVERSÉ
# Formule pour trouver la farine : Poids_Total / (1 + Hydra + Sel + Huile + Malt + Levure)
# On part sur une base de 1% de levure fixe
ratio_total = 1 + (hydra_totale / 100) + (sel_pct / 100) + (huile_pct / 100) + (malt_pct / 100) + 0.01
farine_totale = (nb_patons * poids_paton_fini) / ratio_total

# PHASE 1 : BIGA
p_farine_biga = farine_totale * (pct_biga_farine / 100)
p_eau_biga = p_farine_biga * 0.44  # Eau biga fixe à 44%
p_levure = farine_totale * 0.01
t_eau_biga = 55 - (t_amb + t_far)

# PHASE 2 : RAFRAÎCHISSEMENT
eau_totale = farine_totale * (hydra_totale / 100)
eau_a_ajouter = eau_totale - p_eau_biga
f_reste = farine_totale - p_farine_biga
p_sel = farine_totale * (sel_pct / 100)
p_huile_g = farine_totale * (huile_pct / 100)
p_malt = farine_totale * (malt_pct / 100)
t_eau_p2 = (3 * 24) - (t_amb + t_far + friction_calculee)

# COÛT
cout_total = ((farine_totale/1000)*p_farine) + ((p_huile_g/1000)*p_huile) + ((eau_totale/1000)*0.004)

# 4. AFFICHAGE
st.markdown(f"### 📊 Pour {nb_patons} pâton(s) de {poids_paton_fini}g (Poids fini)")
st.write(f"Farine totale à peser : **{int(farine_totale)}g**")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📦 Phase 1 : Biga (J-1)")
    st.metric("Farine Biga", f"{int(p_farine_biga)} g")
    st.metric("Eau Biga (44%)", f"{int(p_eau_biga)} g")
    st.metric("Levure", f"{p_levure:.1f} g")
    st.metric("Temp. Eau Biga", f"{int(t_eau_biga)} °C")

with col2:
    st.subheader("🥣 Phase 2 : Jour J")
    st.metric("Eau à ajouter", f"{int(eau_a_ajouter)} g")
    st.metric("Temp. Eau idéale", f"{int(t_eau_p2)} °C")
    st.metric("Sel / Huile / Malt", f"{int(p_sel + p_huile_g + p_malt)} g")

st.divider()
st.success(f"💰 Coût de revient par pâton : **{(cout_total/nb_patons):.2f} €**")
