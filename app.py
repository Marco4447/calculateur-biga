import streamlit as st
import math

# 1. CONFIGURATION
st.set_page_config(page_title="Biga MYPIZZATEACHER", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #E0E0E0; }
    .main-title { text-align: center; color: #FF8C00; font-family: 'Helvetica', sans-serif; font-size: 2.8rem; font-weight: 800; margin-top: -40px; }
    div[data-testid="stMetric"] { background-color: #1E1E1E; border: 1px solid #333; padding: 15px; border-radius: 12px; }
    [data-testid="stMetricValue"] { color: #FF8C00 !important; font-weight: bold; font-size: 1.6rem !important; }
    section[data-testid="stSidebar"] { background-color: #1A1A1A; border-right: 1px solid #333; }
    .info-box { background-color: #262730; border-left: 5px solid #FF8C00; padding: 10px; border-radius: 5px; margin-top: 10px; }
    .warning-box { background-color: #442222; border-left: 5px solid #FF4B4B; padding: 10px; border-radius: 5px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🔥 Biga MYPIZZATEACHER</h1>', unsafe_allow_html=True)

# 2. PARAMÈTRES (SIDEBAR)
with st.sidebar:
    st.header("⚙️ Réglages")

    with st.expander("Poids du pâton", expanded=True):
        nb_patons = st.number_input("Nombre de pâtons", value=1, min_value=1)
        poids_cible = st.number_input("Poids d'un pâton fini (g)", value=1000, step=10)
    
    with st.expander("🧪 Ratios & Config Biga", expanded=False):
        hydra_totale = st.slider("Hydratation totale de l'empattement", 50, 100, 56)
        sel_pct = st.slider("Sel (%)", 0.0, 5.0, 2.5, step=0.1)
        huile_pct = st.slider("Huile (%)", 0.0, 10.0, 3.0, step=0.1)
        pct_biga_farine = st.slider("% de Biga à utiliser dans l'empattement total", 10, 100, 20)

    with st.expander("🌡️ Températures & Friction", expanded=True):
        t_amb_biga = st.number_input("Temp. Ambiante J-1 (Biga) (°C)", value=20)
        t_amb_p2 = st.number_input("Temp. Ambiante Jour J (°C)", value=20)
        t_far = st.number_input("Temp. Farine (°C)", value=20)
        # Friction pour la Biga (généralement faible car pétrissage court)
        friction_biga = 2.0 
        # Friction Phase 2 (V1/V2)
        t_v1 = st.number_input("Temps V1 (min)", value=18)
        t_v2 = st.number_input("Temps V2 (min)", value=2)
        friction_p2 = (t_v1 * 0.5) + (t_v2 * 1.3)

# 3. MOTEUR DE CALCUL
ratio_total = 1 + (hydra_totale/100) + (sel_pct/100) + (huile_pct/100) + ((pct_biga_farine/100) * 0.01)
farine_totale = (nb_patons * poids_cible) / ratio_total
poids_total_kilos = (nb_patons * poids_cible) / 1000

# PHASE 1 : BIGA
p_far_biga = farine_totale * (pct_biga_farine / 100)
p_eau_biga = p_far_biga * 0.44
p_lev_biga = p_far_biga * 0.01 

# --- AJUSTEMENT FORMULE BIGA (SORTIE 19-20°C) ---
# TB pour Biga ajustée à 55 pour viser une sortie fraîche
t_eau_biga = 55 - (t_amb_biga + t_far + friction_biga)

# LOGIQUE DE FERMENTATION (SORTIE 19-20°C)
if t_amb_biga > 27:
    t_biga_cible = 14 
    msg_repos = "⚠️ <b>Protocole Canicule :</b> 4h56 à TA puis 12h au frigo (4°C)"
    box_class = "warning-box"
else:
    # On vise une fermentation entre 18 et 19°C
    t_biga_cible = 19.5 
    duree_dec = 30.5 - (0.69 * t_amb_biga)
    h, m = int(duree_dec), int((duree_dec - int(duree_dec)) * 60)
    msg_repos = f"⏳ <b>Repos idéal (18-19°C) :</b> {h}h{m:02d}"
    box_class = "info-box"

# PHASE 2 : RAFRAÎCHISSEMENT
eau_tot_besoin = farine_totale * (hydra_totale / 100)
eau_reste = eau_tot_besoin - p_eau_biga
t_eau_p2 = 72 - (t_amb_p2 + t_far + friction_p2)

# 4. AFFICHAGE DES RÉSULTATS
st.markdown(f"### 📊 Recette pour {nb_patons} pâton(s) de {int(poids_cible)}g ({poids_total_kilos:.2f} kg)")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📦 Phase 1 : Biga")
    st.metric("Farine Biga", f"{math.ceil(p_far_biga)} g")
    st.metric("Eau Biga", f"{math.ceil(p_eau_biga)} g")
    st.metric("Temp. eau coulage Biga", f"{max(int(t_eau_biga), 2)} °C") # Sécurité 2°C minimum
    
    st.markdown(f"""<div class="{box_class}">
    🎯 <b>Cible sortie pétrin :</b> {t_biga_cible}°C<br>{msg_repos}
    </div>""", unsafe_allow_html=True)

with col2:
    st.subheader("🥣 Phase 2 : Jour J")
    st.metric("Farine à ajouter", f"{math.ceil(farine_totale - p_far_biga)} g")
    st.metric("Eau à ajouter", f"{math.ceil(eau_reste)} g")
    st.metric("Temp. eau coulage phase 2", f"{int(t_eau_p2)} °C")

st.divider()
st.info(f"Friction estimée (Phase 2) : +{friction_p2:.1f}°C")
