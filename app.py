import streamlit as st

# 1. CONFIGURATION
st.set_page_config(page_title="Biga MYPIZZATEACHER", layout="centered")

# STYLE CSS SOMBRE PRO
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
    st.header("🍕 Base de Farine Totale")
    nb_patons = st.number_input("Nombre de pâtons", value=1, min_value=1)
    # Si l'utilisateur veut 200g de biga à 20%, il doit saisir 1000g ici
    farine_par_paton = st.number_input("Farine par pâton (g)", value=1000, step=50)
    
    st.divider()
    st.header("💰 Coûts de Revient (€)")
    p_farine = st.number_input("Prix Farine (€/kg)", value=1.20)
    p_huile = st.number_input("Prix Huile (€/L)", value=12.00)
    p_sel = st.number_input("Prix Sel (€/kg)", value=0.80)
    p_malt = st.number_input("Prix Malt (€/kg)", value=15.00)
    p_levure = st.number_input("Prix Levure (€/kg)", value=10.00)
    
    st.divider()
    st.header("🌡️ Températures & Friction")
    t_amb = st.number_input("Temp. Ambiante (°C)", value=22)
    t_far = st.number_input("Temp. Farine (°C)", value=20)
    t_v1 = st.number_input("Temps V1 (min)", value=5)
    t_v2 = st.number_input("Temps V2 (min)", value=8)
    # Friction dynamique : 0.5/min en V1, 1.3/min en V2
    friction_calculee = (t_v1 * 0.5) + (t_v2 * 1.3)
    
    st.divider()
    st.header("🧪 Ratios & Config")
    hydra_totale_pct = st.slider("Hydratation (%)", 50, 100, 56)
    sel_pct = st.slider("Sel (%)", 0.0, 5.0, 2.5, step=0.1)
    huile_pct = st.slider("Huile (%)", 0.0, 10.0, 3.0, step=0.1)
    malt_pct = st.radio("Malt (%)", options=[0.5, 1.0], index=1, horizontal=True)
    pct_biga_farine = st.slider("% Biga", 10, 100, 20)
    pct_biga_eau_val = 55 if pct_biga_farine == 100 else 44

# 3. MOTEUR DE CALCUL
farine_totale = nb_patons * farine_par_paton

# Phase 1 : Biga (20% de 1000g = 200g de farine)
p_farine_biga = farine_totale * (pct_biga_farine / 100)
p_eau_biga = p_farine_biga * (pct_biga_eau_val / 100)
p_levure_g = farine_totale * 0.01 
t_eau_biga_result = 55 - (t_amb + t_far)

# Phase 2 : Rafraîchissement
eau_totale_cible = farine_totale * (hydra_totale_pct / 100)
eau_reste = eau_totale_cible - p_eau_biga
f_reste = farine_totale - p_farine_biga
t_eau_p2_result = (3 * 24) - (t_amb + t_far + friction_calculee)

p_sel_g = farine_totale * (sel_pct / 100)
p_huile_g = farine_totale * (huile_pct / 100)
p_malt_g = farine_totale * (malt_pct / 100)

# Coût de revient (incluant eau à 0.004€/L)
cout_total = ((farine_totale/1000)*p_farine) + ((p_huile_g/1000)*p_huile) + ((p_sel_g/1000)*p_sel) + ((p_malt_g/1000)*p_malt) + ((p_levure_g/1000)*p_levure) + ((eau_totale_cible/1000)*0.004)

# 4. AFFICHAGE
st.markdown(f"### 📊 Résultats pour {int(farine_totale)}g de farine totale")

c1, c2 = st.columns(2)
with c1:
    st.subheader("📦 Phase 1 : Biga (J-1)")
    st.metric("Farine Biga", f"{int(p_farine_biga)} g")
    st.metric("Eau Biga", f"{int(p_eau_biga)} g")
    st.metric("Levure (1%)", f"{p_levure_g:.1f} g")
    st.metric("Temp. Eau Biga", f"{int(t_eau_biga_result)} °C")

with c2:
    st.subheader("🥣 Phase 2 : Jour J")
    st.metric("Eau à ajouter", f"{int(eau_reste)} g")
    st.metric("Temp. Eau idéale", f"{int(t_eau_p2_result)} °C")
    st.metric("Farine à ajouter", f"{int(max(0, f_reste))} g")
    st.metric("Sel / Huile / Malt", f"{p_sel_g + p_huile_g + p_malt_g:.1f} g")

st.divider()
poids_f = (farine_totale + eau_totale_cible + p_sel_g + p_huile_g + p_malt_g + p_levure_g) / nb_patons
st.info(f"⚖️ Poids d'un pâton fini : **{int(poids_f)}g** | Coût par Pâton : **{cout_total/nb_patons:.2f} €**")
