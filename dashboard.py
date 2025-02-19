import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ------ CONFIGURATION DE LA PAGE ------
st.set_page_config(page_title="Dashboard Veille Concurrentielle", page_icon="📊", layout="wide")

# ------ CHARGEMENT DES DONNÉES ------
@st.cache_data
def load_data():
    file_path = "veille.csv"  # Remplace avec ton chemin de fichier
    df = pd.read_csv(file_path, delimiter=";", encoding="utf-8")  # Encodage sécurisé
    df.columns = df.columns.str.strip()  # Supprime les espaces autour des noms de colonnes
    df = df.dropna(axis=1, how='all')  # Suppression colonnes vides
    df = df.fillna("NC")  # Remplacement des valeurs manquantes
    return df

df = load_data()
# DEBUG : Afficher les colonnes pour voir si le nom est correct
st.write("Colonnes détectées :", df.columns.tolist())

# Vérifier si "Nom de la Solution" existe vraiment
if "Nom de la Solution" not in df.columns:
    st.error("Erreur : La colonne 'Nom de la Solution' n'existe pas. Vérifiez le fichier CSV.")


# ------ STYLISATION ------
primary_color = "#FF6600"  # Orange vif
secondary_color = "#333333"  # Gris foncé
background_color = "#FFFFFF"  # Blanc

st.markdown(
    f"""
    <style>
        .main {{ background-color: {background_color}; }}
        h1, h2, h3, h4, h5, h6 {{ color: {secondary_color}; }}
        .stButton>button {{ background-color: {primary_color}; color: white; }}
    </style>
    """,
    unsafe_allow_html=True
)

# ------ FILTRES ------
st.sidebar.header("🔎 Filtres")
selected_competitors = st.sidebar.multiselect(
    "Sélectionner les solutions concurrentes",
    options=df["Nom de la Solution"].unique(),
    default=df["Nom de la Solution"].unique()[:3]
)

selected_kpi = st.sidebar.selectbox(
    "Choisir un KPI à analyser",
    [
        "Score d’innovation & adoption technologique",
        "Indice d’Interopérabilité",
        "Niveau de digitalisation",
        "Indice de conformité réglementaire",
        "Score de couverture fonctionnelle",
        "Performance énergétique & suivi",
        "Évolutivité & mises à jour"
    ]
)

# Filtrer les données selon la sélection
filtered_df = df[df["Nom de la Solution"].isin(selected_competitors + ["SEXTANT"])]

# ------ ORGANISATION DU DASHBOARD ------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Accueil", "⚡ Innovation", "🔗 Interopérabilité", "📊 Performance", "🔍 Conformité", "📈 Comparatif"
])

# ------ PAGE D'ACCUEIL ------
with tab1:
    st.title("📊 Dashboard Veille Concurrentielle - Smart Building")
    st.markdown("**Comparaison de SEXTANT (Nextiim) avec d'autres solutions du marché.**")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🔹 Solutions Comparées", len(filtered_df))
    with col2:
        st.metric("🚀 Score d'Innovation", "⚡ 85%")
    with col3:
        st.metric("🔄 Interopérabilité Moyenne", "🔗 78%")

    # Graphique circulaire du niveau de digitalisation
    digitalisation_counts = filtered_df["App Full Web"].value_counts()
    fig_digital = px.pie(
        names=digitalisation_counts.index, 
        values=digitalisation_counts.values,
        title="Niveau de Digitalisation (Full Web vs Serveur Client)",
        color=digitalisation_counts.index,
        color_discrete_map={"OUI": primary_color, "NON": secondary_color, "NC": "grey"}
    )
    st.plotly_chart(fig_digital, use_container_width=True)

# ------ INNOVATION & DIGITALISATION ------
with tab2:
    st.header("⚡ Score d’Innovation & Digitalisation")
    st.markdown("Analyse de la présence de **l’IA, IoT et BIM** dans les solutions.")

    features = ["Analyse des données par IA", "Intégration IOT", "Maquette BIM"]
    innovation_df = filtered_df[["Nom de la Solution"] + features].copy()

    # Conversion en valeurs numériques
    for col in features:
        innovation_df[col] = innovation_df[col].apply(lambda x: 1 if x == "OUI" else 0)

    innovation_df["Score Innovation"] = innovation_df[features].sum(axis=1)

    # Graphique Radar
    fig_radar = go.Figure()
    for solution in innovation_df["Nom de la Solution"]:
        values = innovation_df[innovation_df["Nom de la Solution"] == solution][features].values[0]
        fig_radar.add_trace(go.Scatterpolar(
            r=values, theta=features, fill='toself', name=solution
        ))
    
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True)
    st.plotly_chart(fig_radar, use_container_width=True)

# ------ INTEROPÉRABILITÉ ------
with tab3:
    st.header("🔗 Indice d’Interopérabilité")
    
    interop_features = ["Interface GTB existante", "Déploiement GTB", "Interaction GTB", "Intégration IOT"]
    interop_df = filtered_df[["Nom de la Solution"] + interop_features].copy()
    
    for col in interop_features:
        interop_df[col] = interop_df[col].apply(lambda x: 1 if x == "OUI" else 0)
    
    interop_df["Score Interopérabilité"] = interop_df[interop_features].sum(axis=1)

    fig_interop = px.bar(
        interop_df, x="Nom de la Solution", y="Score Interopérabilité",
        title="Comparaison des solutions les plus interopérables",
        color="Nom de la Solution"
    )
    st.plotly_chart(fig_interop, use_container_width=True)

# ------ PERFORMANCE ÉNERGÉTIQUE ------
with tab4:
    st.header("📊 Suivi des consommations & performance énergétique")
    
    energy_features = ["Conso mensuelles", "Conso cumulés", "Répartition énergétique", "HeatMap"]
    energy_df = filtered_df[["Nom de la Solution"] + energy_features].copy()
    
    for col in energy_features:
        energy_df[col] = energy_df[col].apply(lambda x: 1 if x == "OUI" else 0)
    
    energy_df["Score Énergie"] = energy_df[energy_features].sum(axis=1)

    fig_energy = px.bar(
        energy_df, x="Nom de la Solution", y="Score Énergie",
        title="Comparaison de la gestion énergétique",
        color="Nom de la Solution"
    )
    st.plotly_chart(fig_energy, use_container_width=True)

st.success("🚀 Dashboard prêt ! Teste les filtres pour explorer les données.")
