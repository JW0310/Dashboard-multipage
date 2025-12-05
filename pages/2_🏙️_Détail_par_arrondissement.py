import streamlit as st
import pandas as pd

df = st.session_state["df"]
reseau_sel = st.session_state["reseau_sel"]

st.title("🏙️ Détail par arrondissement — 2020")

arr_valids = sorted(
    [int(a) for a in df["arrondissement_pour_paris"].dropna().unique()]
)

arr_display = ["Tous"] + [str(a) for a in arr_valids] + ["Non renseigné"]

colA, colB = st.columns(2)

with colA:
    arr_sel = st.selectbox("Arrondissement", arr_display)
with colB:
    reseau_sel_2 = st.selectbox("Réseau", sorted(df["reseau"].unique()),
                                index=sorted(df["reseau"].unique()).index(reseau_sel))

df_arr = df.copy()

if arr_sel not in ["Tous", "Non renseigné"]:
    df_arr = df_arr[df_arr["arrondissement_pour_paris"] == int(arr_sel)]
elif arr_sel == "Non renseigné":
    df_arr = df_arr[df_arr["arrondissement_pour_paris"].isna()]

df_arr = df_arr[df_arr["reseau"] == reseau_sel_2]

st.write(f"### Nombre de stations trouvées : **{len(df_arr)}**")
st.dataframe(df_arr)
