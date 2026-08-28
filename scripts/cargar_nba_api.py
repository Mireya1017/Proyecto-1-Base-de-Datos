import os
from dotenv import load_dotenv

load_dotenv()
import pandas as pd
import psycopg2

from nba_api.stats.endpoints import leaguedashteamstats


# ==========================================================
# CONEXION A POSTGRESQL
# ==========================================================

conexion = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

cursor = conexion.cursor()


# ==========================================================
# TEMPORADAS A CONSULTAR
# ==========================================================

temporadas = [
    "2020-21",
    "2021-22",
    "2022-23",
    "2023-24",
    "2024-25",
    "2025-26"
]


# ==========================================================
# OBTENER MAPA DE TEMPORADAS
# ==========================================================

cursor.execute("""
    SELECT id_temporada, nombre_temporada
    FROM temporada;
""")

mapa_temporadas = {
    nombre: id_temporada
    for id_temporada, nombre in cursor.fetchall()
}


# ==========================================================
# OBTENER EQUIPOS VALIDOS
# ==========================================================

cursor.execute("""
    SELECT id_equipo
    FROM equipo;
""")

ids_equipos = {
    fila[0]
    for fila in cursor.fetchall()
}


# ==========================================================
# SQL DE INGESTA
# ==========================================================

sql_estadistica = """
INSERT INTO estadistica_equipo_temporada (
    id_equipo,
    id_temporada,
    partidos_jugados,
    victorias,
    derrotas,
    minutos,
    puntos,
    rebotes,
    asistencias,
    robos,
    bloqueos,
    perdidas,
    porcentaje_tiros_campo,
    porcentaje_triples,
    porcentaje_tiros_libres,
    plus_minus
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s
)
ON CONFLICT (id_equipo, id_temporada)
DO UPDATE SET
    partidos_jugados = EXCLUDED.partidos_jugados,
    victorias = EXCLUDED.victorias,
    derrotas = EXCLUDED.derrotas,
    minutos = EXCLUDED.minutos,
    puntos = EXCLUDED.puntos,
    rebotes = EXCLUDED.rebotes,
    asistencias = EXCLUDED.asistencias,
    robos = EXCLUDED.robos,
    bloqueos = EXCLUDED.bloqueos,
    perdidas = EXCLUDED.perdidas,
    porcentaje_tiros_campo = EXCLUDED.porcentaje_tiros_campo,
    porcentaje_triples = EXCLUDED.porcentaje_triples,
    porcentaje_tiros_libres = EXCLUDED.porcentaje_tiros_libres,
    plus_minus = EXCLUDED.plus_minus;
"""


# ==========================================================
# CONSULTAR NBA API POR TEMPORADA
# ==========================================================

for temporada in temporadas:

    print("\n==========================================")
    print("Consultando temporada:", temporada)
    print("==========================================")

    datos = leaguedashteamstats.LeagueDashTeamStats(
        season=temporada,
        season_type_all_star="Regular Season",
        per_mode_detailed="PerGame"
    )

    df = datos.get_data_frames()[0]

    # Guardar explícitamente la temporada
    df["SEASON"] = temporada


    # ======================================================
    # ELIMINAR COLUMNAS RANK
    # ======================================================

    columnas_rank = [
        columna
        for columna in df.columns
        if columna.endswith("_RANK")
    ]

    df = df.drop(columns=columnas_rank)


    # ======================================================
    # SELECCIONAR SOLO LO QUE USA NUESTRA BD
    # ======================================================

    df = df[
        [
            "TEAM_ID",
            "GP",
            "W",
            "L",
            "MIN",
            "PTS",
            "REB",
            "AST",
            "STL",
            "BLK",
            "TOV",
            "FG_PCT",
            "FG3_PCT",
            "FT_PCT",
            "PLUS_MINUS",
            "SEASON"
        ]
    ].copy()


    # ======================================================
    # AGREGAR ID_TEMPORADA
    # ======================================================

    df["id_temporada"] = df["SEASON"].map(
        mapa_temporadas
    )


    print("Equipos obtenidos:", len(df))

    print(
        "Equipos no encontrados en PostgreSQL:",
        (~df["TEAM_ID"].isin(ids_equipos)).sum()
    )

    print(
        "Filas sin temporada relacionada:",
        df["id_temporada"].isna().sum()
    )


    # ======================================================
    # INSERT / UPDATE
    # ======================================================

    for _, fila in df.iterrows():

        # Solo insertamos equipos que existen en nuestra BD
        if int(fila["TEAM_ID"]) not in ids_equipos:
            continue

        valores = (
            int(fila["TEAM_ID"]),
            int(fila["id_temporada"]),
            int(fila["GP"]),
            int(fila["W"]),
            int(fila["L"]),
            float(fila["MIN"]),
            float(fila["PTS"]),
            float(fila["REB"]),
            float(fila["AST"]),
            float(fila["STL"]),
            float(fila["BLK"]),
            float(fila["TOV"]),
            float(fila["FG_PCT"]),
            float(fila["FG3_PCT"]),
            float(fila["FT_PCT"]),
            float(fila["PLUS_MINUS"])
        )

        cursor.execute(
            sql_estadistica,
            valores
        )

    conexion.commit()

    print(
        "Temporada",
        temporada,
        "cargada correctamente."
    )


# ==========================================================
# CERRAR CONEXION
# ==========================================================

cursor.close()
conexion.close()

print("\nINGESTA NBA API COMPLETADA.")