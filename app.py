st.markdown("""
    <style>
    /* Fond de page beige clair */
    .stApp { background-color: #FDF5E6; }
    
    /* Titres en rouge foncé */
    h1, h2, h3 { color: #8B0000 !important; font-family: 'serif'; }
    
    /* Couleur du texte des métriques (les chiffres) */
    [data-testid="stMetricValue"] { color: #8B0000 !important; font-weight: bold; }
    
    /* Couleur des étiquettes des métriques */
    [data-testid="stMetricLabel"] { color: #4B2C20 !important; }
    
    /* Cadre blanc autour des chiffres pour la visibilité */
    div[data-testid="stMetric"] { 
        background-color: #FFFFFF; 
        border: 2px solid #8B0000; 
        padding: 15px; 
        border-radius: 10px; 
    }
    </style>
    """, unsafe_allow_html=True)
