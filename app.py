import streamlit as st
import math

# 1. CONFIGURATION
st.set_page_config(page_title="Biga MYPIZZATEACHER", layout="centered")

# STYLE CSS
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #E0E0E0; }
    .main-title { text-align: center; color: #FF8C00; font-family: 'Helvetica', sans-serif; font-size: 2.8rem; font-weight: 800; margin-top: -40px; }
    div[data-testid="stMetric"] { background-color: #1E1E1E; border: 1px solid #333; padding: 15px; border-radius: 12px; }
    [data-testid="stMetricValue"] { color: #FF8C00 !important; font-weight: bold; font-size: 1.6rem !important; }
    section[data-testid="stSidebar"] { background-color: #1A1A1A; border-right: 1px solid #333; }
    .info-box { background-color: #262730; border-left: 5px solid #FF8C00; padding: 15px; border-radius: 5px; margin-top: 10px; }
    .alert-box { background-color: #443311; border-left: 5px solid #FFD700; padding: 15px; border-radius: 5px; margin-top: 10px; }
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
        friction_biga = 2.0 
        t_v1 = st.number_input("Temps V1 (min)", value=18)
        t_v2 = st.number_input("Temps V2 (min)", value=2)
        friction_p2 = (t_v1 * 0.5) + (t_v2 * 1.3)

# 3. MOTEUR DE CALCUL
ratio_total = 1 + (hydra_totale/100) + (sel_pct/100) + (huile_pct/100) + ((pct_biga_farine/100) * 0.01)
farine_totale = (nb_patons * poids_cible) / ratio_total
poids_total_kilos = (nb_patons * poids_cible) / 1000

# PHASE 1
p_far_biga = farine_totale * (pct_biga_farine / 100)
p_eau_biga = p_far_biga * 0.44
p_lev_biga = p_far_biga * 0.01 
t_eau_biga = 55 - (t_amb_biga + t_far + friction_biga)

# FERMENTATION
if t_amb_biga > 27:
    msg_stockage = "🚨 <b>ALERTE :</b> Stockage IMPÉRATIF en zone régulée (18-19°C)."
    duree_dec = 30.5 - (0.69 * 18.5) 
    box_style = "alert-box"
else:
    msg_stockage = f"⏳ <b>Stockage :</b> Température ambiante ({t_amb_biga}°C)."
    duree_dec = 30.5 - (0.69 * t_amb_biga)
    box_style = "info-box"
h, m = int(duree_dec), int((duree_dec - int(duree_dec)) * 60)

# PHASE 2
f_reste = farine_totale - p_far_biga
eau_reste = (farine_totale * (hydra_totale / 100)) - p_eau_biga
t_eau_p2 = 72 - (t_amb_p2 + t_far + friction_p2)

# 4. AFFICHAGE DES RÉSULTATS
st.markdown(f"### 📊 Recette pour {nb_patons} pâton(s) de {int(poids_cible)}g ({poids_total_kilos:.2f} kg)")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📦 Phase 1 : Biga")
    st.metric("Farine Biga", f"{math.ceil(p_far_biga)} g")
    st.metric("Eau Biga", f"{math.ceil(p_eau_biga)} g")
    st.metric("Temp. eau Biga", f"{max(int(t_eau_biga), 2)} °C")
    st.markdown(f'<div class="{box_style}">🎯 <b>Cible sortie :</b> 19-20°C<br>{msg_stockage}<br>⏱️ {h}h{m:02d}</div>', unsafe_allow_html=True)

with col2:
    st.subheader("🥣 Phase 2 : Jour J")
    st.metric("Farine rafraîchi", f"{math.ceil(f_reste)} g")
    st.metric("Eau rafraîchi", f"{math.ceil(eau_reste)} g")
    st.metric("Temp. eau phase 2", f"{int(t_eau_p2)} °C")

# 5. CONSEILS D'EXPERT (HORS DES COLONNES POUR ÊTRE BIEN VISIBLE)
st.divider()
st.subheader("🎓 Les secrets de la Biga par MyPizzaTeacher")
st.info("""
- **Force de la farine (W)** : Utilise une farine de force (**W 300-340**) pour la Biga afin de résister aux 16h-20h de fermentation.
- **Texture** : La Biga doit être grumeleuse (type crumble), jamais une boule lisse.
- **Température** : La sortie à 19-20°C est la clé pour éviter l'acidité.
- **Stockage** : Idéalement entre 18°C et 19°C. Si TA > 27°C, utilise une zone régulée.
""")
