import streamlit as st
import math

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Biga MYPIZZATEACHER - Expert", layout="centered")

# STYLE CSS SOMBRE ET PROFESSIONNEL (Adapté aux couleurs Lione)
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #E0E0E0; }
    .main-title { text-align: center; color: #D4ED31; font-family: 'Helvetica', sans-serif; font-size: 2.8rem; font-weight: 800; margin-top: -40px; }
    div[data-testid="stMetric"] { background-color: #1E1E1E; border: 1px solid #D4ED31; padding: 15px; border-radius: 12px; }
    [data-testid="stMetricValue"] { color: #D4ED31 !important; font-weight: bold; font-size: 1.6rem !important; }
    section[data-testid="stSidebar"] { background-color: #1A1A1A; border-right: 1px solid #333; }
    .info-box { background-color: #262730; border-left: 5px solid #00FFFF; padding: 15px; border-radius: 5px; margin-top: 10px; }
    .alert-box { background-color: #443311; border-left: 5px solid #FF00FF; padding: 15px; border-radius: 5px; margin-top: 10px; }
    /* Style du bouton de retour personnalisé */
    .btn-retour {
        display: block;
        background-color: #FF00FF;
        color: black !important;
        text-align: center;
        padding: 12px;
        font-weight: 900;
        text-decoration: none;
        border-radius: 8px;
        margin-bottom: 20px;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🔥 Biga MYPIZZATEACHER</h1>', unsafe_allow_html=True)

# 2. PARAMÈTRES (SIDEBAR)
with st.sidebar:
    # --- AJOUT DU BOUTON DE RETOUR ---
    st.markdown('<a href="https://mypizzateacher.com" target="_blank" class="btn-retour">🏠 Retour au Site</a>', unsafe_allow_html=True)
    
    st.header("⚙️ Réglages")
    with st.expander("Poids du pâton", expanded=True):
        nb_patons = st.number_input("Nombre de pâtons", value=90, min_value=1)
        poids_cible = st.number_input("Poids d'un pâton fini (g)", value=280, step=10)
    
    with st.expander("🧪 Ratios & Config Biga", expanded=False):
        hydra_totale = st.slider("Hydratation totale (%)", 50, 100, 56)
        sel_pct = st.slider("Sel (%)", 0.0, 5.0, 2.5, step=0.1)
        huile_pct = st.slider("Huile (%)", 0.0, 10.0, 3.0, step=0.1)
        pct_biga_farine = st.slider("% de Biga dans l'empattement total", 10, 100, 100)
        pct_eau_biga_fixe = 44 

    with st.expander("🌡️ Températures & Friction", expanded=True):
        t_amb_biga = st.number_input("Temp. Ambiante J-1 (Biga) (°C)", value=20)
        t_amb_p2 = st.number_input("Temp. Ambiante Jour J (°C)", value=20)
        t_far = st.number_input("Temp. Farine (°C)", value=20)
        friction_biga = 2.0 
        t_v1 = st.number_input("Temps V1 (min)", value=18)
        t_v2 = st.number_input("Temps V2 (min)", value=2)
        friction_p2 = (t_v1 * 0.5) + (t_v2 * 1.3)

    with st.expander("💰 Coûts de Revient", expanded=False):
        p_farine = st.number_input("Prix Farine (€/kg)", value=1.24)
        p_huile = st.number_input("Prix Huile (€/L)", value=12.00)
        p_sel = st.number_input("Prix Sel (€/kg)", value=0.80)
        p_levure = st.number_input("Prix Levure (€/kg)", value=9.99)

# 3. MOTEUR DE CALCUL INVERSÉ
ratio_total = 1 + (hydra_totale/100) + (sel_pct/100) + (huile_pct/100) + ((pct_biga_farine/100) * 0.01)
farine_totale = (nb_patons * poids_cible) / ratio_total
poids_total_kilos = (nb_patons * poids_cible) / 1000

# PHASE 1 : BIGA
p_far_biga = farine_totale * (pct_biga_farine / 100)
p_eau_biga = p_far_biga * (pct_eau_biga_fixe / 100)
p_lev_biga = p_far_biga * 0.01 
t_eau_biga = 55 - (t_amb_biga + t_far + friction_biga)

# LOGIQUE DE FERMENTATION
if t_amb_biga > 27:
    msg_stockage = "🚨 <b>STOCKAGE RÉGULÉ IMPÉRATIF :</b> Zone 18-19°C."
    duree_dec = 30.5 - (0.69 * 18.5) 
    box_style = "alert-box"
else:
    msg_stockage = f"⏳ <b>Stockage idéal :</b> 18-19°C (Actuel : {t_amb_biga}°C)."
    duree_dec = 30.5 - (0.69 * t_amb_biga)
    box_style = "info-box"
h, m = int(duree_dec), int((duree_dec - int(duree_dec)) * 60)

# PHASE 2 : RAFRAÎCHISSEMENT
f_reste = farine_totale - p_far_biga
eau_reste = (farine_totale * (hydra_totale / 100)) - p_eau_biga
p_sel_g = farine_totale * (sel_pct / 100)
p_huile_g = farine_totale * (huile_pct / 100)
t_eau_p2 = 72 - (t_amb_p2 + t_far + friction_p2)

# CALCUL COÛT
c_total = (((farine_totale/1000)*p_farine) + ((p_huile_g/1000)*p_huile) + 
           ((p_sel_g/1000)*p_sel) + ((p_lev_biga/1000)*p_levure))

# 4. AFFICHAGE DES RÉSULTATS
st.markdown(f"### 📊 Recette pour {nb_patons} pâton(s) de {int(poids_cible)}g soit {poids_total_kilos:.2f} kg de pâte")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📦 Phase 1 : Biga")
    st.metric("Farine Biga", f"{math.ceil(p_far_biga)} g")
    st.metric("Eau Biga (44%)", f"{math.ceil(p_eau_biga)} g")
    st.metric("Temp. eau coulage Biga", f"{max(int(t_eau_biga), 2)} °C")
    st.markdown(f'<div class="{box_style}">🎯 <b>Cible sortie :</b> 19-20°C<br>{msg_stockage}<br>⏱️ <b>Durée :</b> {h}h{m:02d}</div>', unsafe_allow_html=True)

with col2:
    st.subheader("🥣 Phase 2 : Jour J")
    st.metric("Farine à ajouter", f"{math.ceil(f_reste)} g")
    st.metric("Eau à ajouter", f"{math.ceil(eau_reste)} g")
    st.metric("Temp. eau coulage phase 2", f"{int(t_eau_p2)} °C")

st.divider()
st.success(f"💰 Coût de revient par pâton : **{(c_total/nb_patons):.2f} €**")

# 5. L'EXPERTISE MYPIZZATEACHER
st.subheader("🎓 L'expertise MYPIZZATEACHER")
t1, t2, t3 = st.tabs(["🌾 Farine & W", "⚙️ Pétrissage", "❄️ Fermentation"])

with t1:
    st.markdown("""
    **Précision sur la Force (W) :**
    * **Phase 1 (Biga) :** Utilisez impérativement une farine de force **W 300-340**. Elle doit supporter 16h-20h de fermentation à 18-19°C.
    * **Phase 2 (Rafraîchi) :** * Pour une utilisation rapide (< 24h) : **W 240-260** pour plus de souplesse.
        * Pour une maturation longue (24h-48h) : **W 300-320**.
    * **Conseil Expert :** Utiliser la même farine W 300+ pour les deux phases sécurise votre réseau glutineux.
    """)
with t2:
    st.markdown("""
    **Technique de Pétrissage :**
    * **Aspect :** La biga doit être **grumeleuse** (type crumble). Ne formez jamais une boule lisse en phase 1.
    * **Vitesse :** Pétrissez en vitesse 1 lente (4-5 min) pour oxygéner sans chauffer la masse.
    * **Sortie :** La température cible de **19-20°C** est cruciale pour l'équilibre des arômes.
    """)
with t3:
    st.markdown("""
    **Gestion Thermique :**
    * **Zone Idéale :** Entre **18°C et 19°C**. 
    * **Danger :** Au-delà de **22°C**, l'acidité acétique (vinaigre) prend le dessus et fragilise le gluten.
    * **Canicule :** Si TA > 27°C, utilisez impérativement une zone régulée ou cave à vin.
    """)
