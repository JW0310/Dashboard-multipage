import streamlit as st
import plotly.express as px
import pandas as pd

df = st.session_state["df"]
df_geo = st.session_state["df_geo"]

# --- SIDEBAR AVEC FILTRES ---
st.sidebar.title("📌 Menu & Filtres")
st.sidebar.markdown("**Dataset : Trafic annuel RATP — 2020**")

reseaux = sorted(df["reseau"].dropna().unique())

if "reseau_sel" not in st.session_state:
    st.session_state["reseau_sel"] = reseaux[0]

reseau_sel = st.sidebar.selectbox(
    "Sélectionner un réseau",
    reseaux,
    index=reseaux.index(st.session_state["reseau_sel"])
)
st.session_state["reseau_sel"] = reseau_sel
# -----------------------------

st.title("🗺️ Carte interactive — Réseau : " + reseau_sel)

# --- 🔥 FILTRE SUR LE RESEAU ---
df_map = df_geo.dropna(subset=["lat", "lon"])
df_map = df_map[df_map["reseau"] == reseau_sel]
# -------------------------------

color_map = {
    "Metro": "#008000",
    "Métro": "#008000",
    "RER": "#0000CC"
}

fig_map = px.scatter_mapbox(
    df_map,
    lat="lat",
    lon="lon",
    hover_name="station",
    hover_data=["reseau", "trafic", "nb_corr"],
    color="reseau",
    zoom=11,
    height=650,
    color_discrete_map=color_map
)

fig_map.update_traces(marker=dict(size=8))
fig_map.update_layout(mapbox_style="open-street-map")
fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig_map, use_container_width=True)
