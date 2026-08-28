from nba_api.stats.endpoints import leaguedashteamstats

# Temporada que queremos consultar
temporada = "2025-26"

# Solicitud a la NBA API
datos = leaguedashteamstats.LeagueDashTeamStats(
    season=temporada,
    season_type_all_star="Regular Season",
    per_mode_detailed="PerGame"
)

# Convertir la respuesta de la API en un DataFrame
df = datos.get_data_frames()[0]

# Agregar la temporada como columna
df["SEASON"] = temporada

# Identificar todas las columnas que terminan en _RANK
columnas_rank = [
    columna
    for columna in df.columns
    if columna.endswith("_RANK")
]

# Eliminar las columnas de ranking
df = df.drop(columns=columnas_rank)

# Mostrar los datos resultantes
print(df)

print("\nColumnas conservadas:")
print(df.columns.tolist())

print("\nDimensiones:")
print(df.shape)