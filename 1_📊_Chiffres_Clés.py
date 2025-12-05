import streamlit as st
import pandas as pd
import plotly.express as px

df = st.session_state["df"]
# --- SIDEBAR (à mettre partout) ---
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
# -----------------------------------
st.title("📊 Chiffres clés")

df_global = df[df["reseau"] == reseau_sel]

trafic_total = df_global["trafic"].sum()
nb_stations = df_global["station"].nunique()
station_max = df_global.loc[df_global["trafic"].idxmax(), "station"]
trafic_moyen = int(df_global["trafic"].mean())

# Fonction KPI
def kpi_small(label, value):
    st.markdown(
        f"""
        <div style="text-align:center;">
            <div style="font-size:16px; color:#003A70; font-weight:600;">{label}</div>
            <div style="font-size:24px; color:#000000; font-weight:700; margin-top:4px;">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

k1, k2, k3, k4 = st.columns([1.3, 1, 1.5, 1])

with k1:
    kpi_small("Trafic total", f"{trafic_total:,.0f}".replace(",", " "))
with k2:
    kpi_small("Nombre de stations", nb_stations)
with k3:
    kpi_small("Station la plus fréquentée", station_max.title())
with k4:
    kpi_small("Trafic moyen / station", f"{trafic_moyen:,.0f}".replace(",", " "))

st.markdown("---")

# PIE CHART
st.write("### 🍩 Répartition du trafic — Métro vs RER")
df_pie = df.groupby("reseau")["trafic"].sum().reset_index()

fig_pie = px.pie(
    df_pie,
    names="reseau",
    values="trafic",
    color="reseau",
    color_discrete_map={"Metro": "#009B77", "Métro": "#009B77", "RER": "#003A70"},
    title="Répartition du trafic — 2020"
)

st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# BAR CHART CORRESPONDANCES
st.write("### 🔝 Top 10 des stations avec le plus de correspondances")
df_top_corr = df.sort_values("nb_corr", ascending=False).head(10)

fig_corr = px.bar(
    df_top_corr,
    x="station",
    y="nb_corr",
    color="nb_corr",
    title="Top 10 — Nombre de correspondances"
)

st.plotly_chart(fig_corr, use_container_width=True)
