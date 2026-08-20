from nba_api.stats.endpoints import leaguedashteamstats

temporada = "2025-26"

datos = leaguedashteamstats.LeagueDashTeamStats(
    season=temporada,
    season_type_all_star="Regular Season",
    per_mode_detailed="PerGame"
)

df = datos.get_data_frames()[0]

df["SEASON"] = temporada

print(df)

print("\nColumnas:")
print(df.columns.tolist())

print("\nDimensiones:")
print(df.shape)