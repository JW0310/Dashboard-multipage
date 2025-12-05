import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard RATP 2020",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------
# Chargement DATA PRINCIPALE (commun à toutes pages)
# --------------------------------------------
@st.cache_data
def load_main_data():
    df_raw = pd.read_csv("data_ratp.csv", header=None, dtype=str)

    header_line = df_raw.iloc[0, 0].split(";")
    df = df_raw.iloc[1:].copy()
    df = df[0].str.split(";", expand=True)
    df.columns = header_line

    df.columns = (
        df.columns.str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
        .str.replace("é", "e")
        .str.replace("è", "e")
        .str.replace("ê", "e")
        .str.replace("à", "a")
    )

    df["trafic"] = pd.to_numeric(df["trafic"], errors="coerce")
    df["rang"] = pd.to_numeric(df["rang"], errors="coerce")

    corr_cols = [c for c in df.columns if "correspondance" in c]
    df[corr_cols] = df[corr_cols].fillna("Aucune").replace("", "Aucune")

    df["arrondissement_pour_paris"] = (
        df["arrondissement_pour_paris"]
        .replace("", None)
        .astype(float)
    )

    df["nb_corr"] = df[corr_cols].apply(lambda r: sum(v != "Aucune" for v in r), axis=1)

    return df

@st.cache_data
def load_geocoded():
    return pd.read_csv("stations_geocode.csv")


# INITIALISATION SESSION
if "df" not in st.session_state:
    st.session_state["df"] = load_main_data()
if "df_geo" not in st.session_state:
    st.session_state["df_geo"] = load_geocoded()

df = st.session_state["df"]


st.title("🚇 Dashboard RATP 2020")
st.markdown("Bienvenue dans l'application multipage. Utilisez le menu de gauche.")
