import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time
import os

# ------------------------------
# 1. Chargement + Nettoyage RATP
# ------------------------------

print("Chargement du fichier data_ratp.csv ...")

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

cols_corr = [c for c in df.columns if "correspondance" in c]
df[cols_corr] = df[cols_corr].fillna("Aucune").replace("", "Aucune").astype(str)

df["arrondissement_pour_paris"] = (
    df["arrondissement_pour_paris"]
    .replace("", None)
    .astype(float)
)

# Calcul nb correspondances
df["nb_corr"] = df[cols_corr].apply(lambda row: sum(v != "Aucune" for v in row), axis=1)

# ------------------------------
# 2. Préparation géocodage
# ------------------------------

print("Initialisation du géocodeur (Nominatim)...")

geolocator = Nominatim(user_agent="ratp_geocoder")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Fichier de sauvegarde progressive
save_path = "stations_geocode.csv"

# Reprise si fichier existe déjà
if os.path.exists(save_path):
    print("⚠️ Reprise du fichier existant.")
    df_geo = pd.read_csv(save_path)
else:
    df_geo = pd.DataFrame(columns=[
        "station", "reseau", "trafic", "arrondissement",
        "nb_corr", "lat", "lon"
    ])

# Liste des stations à géocoder
processed_stations = set(df_geo["station"].unique())
stations_to_process = df[~df["station"].isin(processed_stations)]

print(f"Stations déjà géocodées : {len(processed_stations)}")
print(f"Stations restantes       : {len(stations_to_process)}")
print("Début du géocodage...\n")

lat_list = []
lon_list = []

# ------------------------------
# 3. Géocodage principal
# ------------------------------

for idx, row in stations_to_process.iterrows():
    station = row["station"]

    print(f"Géocodage : {station} ...", end=" ")

    try:
        location = geocode(f"{station}, Paris, France")
        if location:
            lat = location.latitude
            lon = location.longitude
            print("OK")
        else:
            lat = None
            lon = None
            print("NON TROUVÉ")
    except Exception as e:
        lat = None
        lon = None
        print(f"ERREUR ({e})")

    df_geo = pd.concat([
        df_geo,
        pd.DataFrame([{
            "station": station,
            "reseau": row["reseau"],
            "trafic": row["trafic"],
            "arrondissement": row["arrondissement_pour_paris"],
            "nb_corr": row["nb_corr"],
            "lat": lat,
            "lon": lon
        }])
    ])

    # Sauvegarde progressive
    df_geo.to_csv(save_path, index=False)

    # Temporisation (sécurité)
    time.sleep(1)

print("\n🎉 GÉOCODAGE TERMINÉ !")
print(f"Fichier généré : {save_path}")
