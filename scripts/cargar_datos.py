import os
from dotenv import load_dotenv

load_dotenv()
import pandas as pd
import psycopg2

# CARGAR CSV DE EQUIPOS

team = pd.read_csv("data/Team.csv")
team_attributes = pd.read_csv("data/Team_Attributes.csv")


# UNIR LOS DOS CSV
# Team.id = Team_Attributes.ID


equipos = team.merge(
    team_attributes,
    left_on="id",
    right_on="ID",
    how="left"
)

# SELECCIONAR LOS DATOS QUE NECESITA NUESTRA BD
equipos = equipos[
    [
        "id",
        "full_name",
        "abbreviation",
        "nickname",
        "city",
        "state",
        "year_founded",
        "ARENA",
        "ARENACAPACITY",
        "OWNER",
        "GENERALMANAGER",
        "HEADCOACH",
        "DLEAGUEAFFILIATION"
    ]
]


# ==========================================================
# RENOMBRAR SEGÚN NUESTRO MODELO RELACIONAL
# ==========================================================

equipos = equipos.rename(
    columns={
        "id": "id_equipo",
        "full_name": "nombre_equipo",
        "abbreviation": "abreviatura",
        "nickname": "apodo",
        "city": "ciudad",
        "state": "estado",
        "year_founded": "anio_fundacion",
        "ARENA": "arena",
        "ARENACAPACITY": "capacidad_arena",
        "OWNER": "propietario",
        "GENERALMANAGER": "gerente_general",
        "HEADCOACH": "entrenador",
        "DLEAGUEAFFILIATION": "afiliacion_dleague"
    }
)

# Convertir valores faltantes de Pandas a NULL para PostgreSQL
equipos = equipos.astype(object).where(pd.notna(equipos), None)

# ==========================================================
# MOSTRAR RESULTADO
# ==========================================================

print("\nDATOS PREPARADOS PARA LA TABLA EQUIPO:\n")

print(equipos)

print("\nColumnas finales:")
print(equipos.columns.tolist())

print("\nDimensiones:")
print(equipos.shape)

# ==========================================================
# CONEXIÓN A POSTGRESQL
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
# INSERTAR EQUIPOS
# ==========================================================

sql_equipo = """
INSERT INTO equipo (
    id_equipo,
    nombre_equipo,
    abreviatura,
    apodo,
    ciudad,
    estado,
    anio_fundacion,
    arena,
    capacidad_arena,
    propietario,
    gerente_general,
    entrenador,
    afiliacion_dleague
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (id_equipo) DO NOTHING;
"""

for _, fila in equipos.iterrows():

    valores = (
        fila["id_equipo"],
        fila["nombre_equipo"],
        fila["abreviatura"],
        fila["apodo"],
        fila["ciudad"],
        fila["estado"],
        fila["anio_fundacion"],
        fila["arena"],
        fila["capacidad_arena"],
        fila["propietario"],
        fila["gerente_general"],
        fila["entrenador"],
        fila["afiliacion_dleague"]
    )

    print(valores)

    cursor.execute(sql_equipo, valores)

# Confirmar cambios
conexion.commit()

print("\nEquipos insertados correctamente en PostgreSQL.")




# ==========================================================
# JUGADORES - REVISAR CSV
# ==========================================================

player = pd.read_csv("data/Player.csv")
player_attributes = pd.read_csv("data/Player_Attributes.csv")

print("\nCOLUMNAS DE Player.csv:")
print(player.columns.tolist())

print("\nCOLUMNAS DE Player_Attributes.csv:")
print(player_attributes.columns.tolist())

print("\nDIMENSIONES:")
print("Player.csv:", player.shape)
print("Player_Attributes.csv:", player_attributes.shape)

# ==========================================================
# PREPARAR TABLA JUGADOR
# ==========================================================

# Unir Player.csv con Player_Attributes.csv
# Player.csv será la tabla base porque contiene 4501 jugadores.
jugadores = player.merge(
    player_attributes,
    left_on="id",
    right_on="ID",
    how="left"
)


# ==========================================================
# SELECCIONAR COLUMNAS NECESARIAS
# ==========================================================

jugadores = jugadores[
    [
        "id",
        "full_name",
        "first_name",
        "last_name",
        "BIRTHDATE",
        "COUNTRY",
        "SCHOOL",
        "POSITION",
        "HEIGHT",
        "WEIGHT",
        "is_active"
    ]
]

# ==========================================================
# RENOMBRAR SEGÚN EL MODELO RELACIONAL
# ==========================================================

jugadores = jugadores.rename(
    columns={
        "id": "id_jugador",
        "full_name": "nombre_completo",
        "first_name": "nombre",
        "last_name": "apellido",
        "BIRTHDATE": "fecha_nacimiento",
        "COUNTRY": "pais",
        "SCHOOL": "universidad",
        "POSITION": "posicion",
        "HEIGHT": "altura",
        "WEIGHT": "peso",
        "is_active": "esta_activo"
    }
)


# ==========================================================
# CONVERTIR 0/1 A BOOLEAN
# ==========================================================

jugadores["esta_activo"] = jugadores["esta_activo"].map({
    0: False,
    1: True
})


# ==========================================================
# LIMPIAR VALORES FALTANTES
# ==========================================================

jugadores = jugadores.astype(object).where(
    pd.notna(jugadores),
    None
)


print("\nDATOS PREPARADOS PARA JUGADOR:")
print(jugadores.head())

print("\nDimensiones de jugador:")
print(jugadores.shape)

# ==========================================================
# INSERTAR JUGADORES EN POSTGRESQL
# ==========================================================

sql_jugador = """
INSERT INTO jugador (
    id_jugador,
    nombre_completo,
    nombre,
    apellido,
    fecha_nacimiento,
    pais,
    universidad,
    posicion,
    altura,
    peso,
    esta_activo
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (id_jugador) DO NOTHING;
"""

for _, fila in jugadores.iterrows():

    valores = (
        fila["id_jugador"],
        fila["nombre_completo"],
        fila["nombre"],
        fila["apellido"],
        fila["fecha_nacimiento"],
        fila["pais"],
        fila["universidad"],
        fila["posicion"],
        fila["altura"],
        fila["peso"],
        fila["esta_activo"]
    )

    cursor.execute(sql_jugador, valores)


conexion.commit()

print("\nJugadores insertados correctamente en PostgreSQL.")

# ==========================================================
# PREPARAR TABLA TEMPORADA
# ==========================================================

team_salary = pd.read_csv("data/Team_Salary.csv")

# Buscar columnas que representan temporadas
columnas_temporadas = [
    columna
    for columna in team_salary.columns
    if columna.startswith("X20")
]

# Quitar la X inicial
nombres_temporadas = [
    columna.replace("X", "", 1)
    for columna in columnas_temporadas
]

print("\nTEMPORADAS ENCONTRADAS:")
print(nombres_temporadas)

# ==========================================================
# INSERTAR TEMPORADAS
# ==========================================================

sql_temporada = """
INSERT INTO temporada (
    nombre_temporada
)
VALUES (%s)
ON CONFLICT (nombre_temporada) DO NOTHING;
"""

for temporada in nombres_temporadas:
    cursor.execute(
        sql_temporada,
        (temporada,)
    )

conexion.commit()

print("\nTemporadas insertadas correctamente en PostgreSQL.")

# ==========================================================
# REVISAR GAME_OFFICIALS
# ==========================================================

game_officials = pd.read_csv("data/Game_Officials.csv")

print("\nCOLUMNAS DE Game_Officials.csv:")
print(game_officials.columns.tolist())

print("\nDIMENSIONES:")
print(game_officials.shape)

print("\nPRIMERAS FILAS:")
print(game_officials.head())

# ==========================================================
# PREPARAR TABLA ARBITRO
# ==========================================================

arbitros = game_officials[
    [
        "OFFICIAL_ID",
        "FIRST_NAME",
        "LAST_NAME",
        "JERSEY_NUM"
    ]
].copy()

# Eliminar repeticiones del mismo árbitro
arbitros = arbitros.drop_duplicates(
    subset=["OFFICIAL_ID"]
)

# Renombrar según nuestro modelo relacional
arbitros = arbitros.rename(
    columns={
        "OFFICIAL_ID": "id_arbitro",
        "FIRST_NAME": "nombre",
        "LAST_NAME": "apellido",
        "JERSEY_NUM": "numero_camiseta"
    }
)

# Convertir NaN a NULL
arbitros = arbitros.astype(object).where(
    pd.notna(arbitros),
    None
)

print("\nDATOS PREPARADOS PARA ARBITRO:")
print(arbitros.head())

print("\nCantidad de árbitros únicos:")
print(arbitros.shape)

# ==========================================================
# INSERTAR ARBITROS EN POSTGRESQL
# ==========================================================

sql_arbitro = """
INSERT INTO arbitro (
    id_arbitro,
    nombre,
    apellido,
    numero_camiseta
)
VALUES (%s, %s, %s, %s)
ON CONFLICT (id_arbitro) DO NOTHING;
"""

for _, fila in arbitros.iterrows():

    valores = (
        fila["id_arbitro"],
        fila["nombre"],
        fila["apellido"],
        fila["numero_camiseta"]
    )

    cursor.execute(sql_arbitro, valores)

conexion.commit()

print("\nÁrbitros insertados correctamente en PostgreSQL.")

# ==========================================================
# REVISAR TEAM_HISTORY
# ==========================================================

team_history = pd.read_csv("data/Team_History.csv")

print("\nCOLUMNAS DE Team_History.csv:")
print(team_history.columns.tolist())

print("\nDIMENSIONES:")
print(team_history.shape)

print("\nPRIMERAS FILAS:")
print(team_history.head())

# ==========================================================
# PREPARAR TABLA HISTORIAL_EQUIPO
# ==========================================================

historial_equipos = team_history[
    [
        "ID",
        "YEARFOUNDED",
        "CITY",
        "NICKNAME",
        "YEARACTIVETILL"
    ]
].copy()

# Renombrar según nuestro modelo relacional
historial_equipos = historial_equipos.rename(
    columns={
        "ID": "id_equipo",
        "YEARFOUNDED": "anio_fundacion",
        "CITY": "ciudad",
        "NICKNAME": "apodo",
        "YEARACTIVETILL": "anio_activo_hasta"
    }
)

# Convertir valores faltantes a NULL
historial_equipos = historial_equipos.astype(object).where(
    pd.notna(historial_equipos),
    None
)

print("\nDATOS PREPARADOS PARA HISTORIAL_EQUIPO:")
print(historial_equipos.head())

print("\nDimensiones:")
print(historial_equipos.shape)

# ==========================================================
# PREPARAR TABLA HISTORIAL_EQUIPO
# ==========================================================

historial_equipos = team_history[
    [
        "ID",
        "YEARFOUNDED",
        "CITY",
        "NICKNAME",
        "YEARACTIVETILL"
    ]
].copy()

# Renombrar según nuestro modelo relacional
historial_equipos = historial_equipos.rename(
    columns={
        "ID": "id_equipo",
        "YEARFOUNDED": "anio_fundacion",
        "CITY": "ciudad",
        "NICKNAME": "apodo",
        "YEARACTIVETILL": "anio_activo_hasta"
    }
)

# Convertir valores faltantes a NULL
historial_equipos = historial_equipos.astype(object).where(
    pd.notna(historial_equipos),
    None
)

print("\nDATOS PREPARADOS PARA HISTORIAL_EQUIPO:")
print(historial_equipos.head())

print("\nDimensiones:")
print(historial_equipos.shape)

# ==========================================================
# INSERTAR HISTORIAL DE EQUIPOS
# ==========================================================

sql_historial = """
INSERT INTO historial_equipo (
    id_equipo,
    anio_fundacion,
    ciudad,
    apodo,
    anio_activo_hasta
)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (
    id_equipo,
    anio_fundacion,
    ciudad,
    apodo
)
DO NOTHING;
"""
for _, fila in historial_equipos.iterrows():

    valores = (
        fila["id_equipo"],
        fila["anio_fundacion"],
        fila["ciudad"],
        fila["apodo"],
        fila["anio_activo_hasta"]
    )

    cursor.execute(sql_historial, valores)

conexion.commit()

print("\nHistorial de equipos insertado correctamente en PostgreSQL.")

# ==========================================================
# REVISAR DRAFT.CSV
# ==========================================================

draft_csv = pd.read_csv("data/Draft.csv")

print("\nCOLUMNAS DE Draft.csv:")
print(draft_csv.columns.tolist())

print("\nDIMENSIONES:")
print(draft_csv.shape)

print("\nPRIMERAS FILAS:")
print(draft_csv.head())

# ==========================================================
# PREPARAR TABLA DRAFT
# ==========================================================

draft = draft_csv[
    [
        "idPlayer",
        "namePlayer",
        "idTeam",
        "yearDraft",
        "numberPickOverall",
        "numberRound",
        "numberRoundPick",
        "nameOrganizationFrom",
        "typeOrganizationFrom",
        "slugOrganizationTypeFrom",
        "locationOrganizationFrom"
    ]
].copy()


draft = draft.rename(
    columns={
        "idPlayer": "id_jugador",
        "namePlayer": "nombre_jugador_fuente",
        "idTeam": "id_equipo",
        "yearDraft": "anio_draft",
        "numberPickOverall": "numero_pick",
        "numberRound": "ronda_pick",
        "numberRoundPick": "numero_pick_ronda",
        "nameOrganizationFrom": "nombre_organizacion_origen",
        "typeOrganizationFrom": "tipo_organizacion_origen",
        "slugOrganizationTypeFrom": "codigo_tipo_organizacion_origen",
        "locationOrganizationFrom": "ubicacion_organizacion_origen"
    }
)

# ==========================================================
# CONVERTIR COLUMNAS NUMERICAS
# ==========================================================

columnas_enteras = [
    "id_jugador",
    "anio_draft",
    "id_equipo",
    "numero_pick",
    "ronda_pick",
    "numero_pick_ronda"
]

for columna in columnas_enteras:
    draft[columna] = draft[columna].apply(
        lambda x: int(x) if pd.notna(x) else None
    )


# ==========================================================
# VALIDAR FOREIGN KEYS
# ==========================================================

ids_jugadores = set(jugadores["id_jugador"])
ids_equipos = set(equipos["id_equipo"])

print(
    "\nJugadores del Draft que no están en jugador:",
    (~draft["id_jugador"].isin(ids_jugadores)).sum()
)

print(
    "Equipos del Draft que no están en equipo:",
    (
        draft["id_equipo"].notna()
        & ~draft["id_equipo"].isin(ids_equipos)
    ).sum()
)


# Si el jugador no existe, dejamos la FK en NULL
draft.loc[
    ~draft["id_jugador"].isin(ids_jugadores),
    "id_jugador"
] = None


# Si el equipo no existe, dejamos la FK en NULL
draft.loc[
    draft["id_equipo"].notna()
    & ~draft["id_equipo"].isin(ids_equipos),
    "id_equipo"
] = None


# Convertir NaN restantes a NULL
draft = draft.astype(object).where(
    pd.notna(draft),
    None
)


print("\nDATOS PREPARADOS PARA DRAFT:")
print(draft.head())

print("\nCOLUMNAS FINALES DE DRAFT:")
print(draft.columns.tolist())

print("\nDimensiones finales de draft:")
print(draft.shape)

duplicados_draft = draft[
    draft.duplicated(
        subset=["anio_draft", "numero_pick"],
        keep=False
    )
]

print("\nFilas con año + pick repetidos:")
print(len(duplicados_draft))

print("\nEjemplos:")
print(
    duplicados_draft[
        [
            "anio_draft",
            "numero_pick",
            "nombre_jugador_fuente"
        ]
    ].head(30)
)

print("\nDraft sin año:")
print(draft["anio_draft"].isna().sum())

print("\nDraft sin número de pick:")
print(draft["numero_pick"].isna().sum())

# ==========================================================
# INSERTAR DRAFT EN POSTGRESQL
# ==========================================================

sql_draft = """
INSERT INTO draft (
    id_jugador,
    nombre_jugador_fuente,
    id_equipo,
    anio_draft,
    numero_pick,
    ronda_pick,
    numero_pick_ronda,
    nombre_organizacion_origen,
    tipo_organizacion_origen,
    codigo_tipo_organizacion_origen,
    ubicacion_organizacion_origen
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

print("\nCOLUMNAS FINALES DE DRAFT:")
print(draft.columns.tolist())

# Limpiar Draft antes de volver a cargarlo
cursor.execute("TRUNCATE TABLE draft RESTART IDENTITY;")

for _, fila in draft.iterrows():

    valores = (
        fila["id_jugador"],
        fila["nombre_jugador_fuente"],
        fila["id_equipo"],
        fila["anio_draft"],
        fila["numero_pick"],
        fila["ronda_pick"],
        fila["numero_pick_ronda"],
        fila["nombre_organizacion_origen"],
        fila["tipo_organizacion_origen"],
        fila["codigo_tipo_organizacion_origen"],
        fila["ubicacion_organizacion_origen"]
    )

    cursor.execute(sql_draft, valores)

conexion.commit()

print("\nDraft insertado correctamente en PostgreSQL.")

# ==========================================================
# REVISAR DRAFT_COMBINE.CSV
# ==========================================================

draft_combine_csv = pd.read_csv("data/Draft_Combine.csv")

print("\nCOLUMNAS DE Draft_Combine.csv:")
print(draft_combine_csv.columns.tolist())

print("\nDIMENSIONES:")
print(draft_combine_csv.shape)

print("\nPRIMERAS FILAS:")
print(draft_combine_csv.head())

# ==========================================================
# PREPARAR TABLA DRAFT_COMBINE
# ==========================================================

draft_combine = draft_combine_csv[
    [
        "idPlayer",
        "namePlayer",
        "yearCombine",
        "slugPosition",
        "heightWOShoesInches",
        "weightLBS",
        "wingspanInches",
        "reachStandingInches",
        "verticalLeapStandingInches",
        "verticalLeapMaxInches",
        "timeLaneAgility",
        "timeThreeQuarterCourtSprint",
        "repsBenchPress135",
        "pctBodyFat"
    ]
].copy()


draft_combine = draft_combine.rename(
    columns={
        "namePlayer": "nombre_jugador_fuente",
        "idPlayer": "id_jugador",
        "yearCombine": "anio_combine",
        "slugPosition": "posicion",
        "heightWOShoesInches": "altura_sin_zapatos",
        "weightLBS": "peso",
        "wingspanInches": "envergadura",
        "reachStandingInches": "alcance_de_pie",
        "verticalLeapStandingInches": "salto_vertical",
        "verticalLeapMaxInches": "salto_vertical_maximo",
        "timeLaneAgility": "tiempo_agilidad",
        "timeThreeQuarterCourtSprint": "tiempo_sprint_tres_cuartos",
        "repsBenchPress135": "repeticiones_banca",
        "pctBodyFat": "porcentaje_grasa"
    }
)

# ==========================================================
# CONVERTIR TIPOS
# ==========================================================

draft_combine["id_jugador"] = draft_combine["id_jugador"].apply(
    lambda x: int(x) if pd.notna(x) else None
)

draft_combine["anio_combine"] = draft_combine["anio_combine"].apply(
    lambda x: int(x) if pd.notna(x) else None
)

draft_combine["repeticiones_banca"] = draft_combine["repeticiones_banca"].apply(
    lambda x: int(x) if pd.notna(x) else None
)

# ==========================================================
# VALIDAR JUGADORES
# ==========================================================

ids_jugadores = set(jugadores["id_jugador"])

faltantes_combine = (
    draft_combine["id_jugador"].notna()
    & ~draft_combine["id_jugador"].isin(ids_jugadores)
)

print(
    "\nJugadores de Draft Combine que no están en jugador:",
    faltantes_combine.sum()
)

print("\nEjemplos de jugadores faltantes:")
print(
    draft_combine.loc[
        faltantes_combine,
        ["id_jugador", "anio_combine"]
    ].head(20)
)

print("\nRegistros sin id_jugador:")
print(draft_combine["id_jugador"].isna().sum())

print("\nDimensiones de Draft Combine:")
print(draft_combine.shape)

# Los jugadores que no existen en jugador
# conservan su nombre, pero no pueden tener una FK inválida.
draft_combine.loc[
    faltantes_combine,
    "id_jugador"
] = None

# Convertir NaN restantes a NULL
draft_combine = draft_combine.astype(object).where(
    pd.notna(draft_combine),
    None
)

# INSERTAR

sql_draft_combine = """
INSERT INTO draft_combine (
    id_jugador,
    nombre_jugador_fuente,
    anio_combine,
    posicion,
    altura_sin_zapatos,
    peso,
    envergadura,
    alcance_de_pie,
    salto_vertical,
    salto_vertical_maximo,
    tiempo_agilidad,
    tiempo_sprint_tres_cuartos,
    repeticiones_banca,
    porcentaje_grasa
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

# Como seguimos desarrollando y ejecutando el script varias veces,
# reconstruimos esta tabla antes de cargarla.
cursor.execute("TRUNCATE TABLE draft_combine RESTART IDENTITY;")

for _, fila in draft_combine.iterrows():

    valores = (
        fila["id_jugador"],
        fila["nombre_jugador_fuente"],
        fila["anio_combine"],
        fila["posicion"],
        fila["altura_sin_zapatos"],
        fila["peso"],
        fila["envergadura"],
        fila["alcance_de_pie"],
        fila["salto_vertical"],
        fila["salto_vertical_maximo"],
        fila["tiempo_agilidad"],
        fila["tiempo_sprint_tres_cuartos"],
        fila["repeticiones_banca"],
        fila["porcentaje_grasa"]
    )

    cursor.execute(sql_draft_combine, valores)

conexion.commit()

print("\nDraft Combine insertado correctamente en PostgreSQL.")


# ==========================================================
# REVISAR PLAYER_SALARY.CSV
# ==========================================================

player_salary_csv = pd.read_csv("data/Player_Salary.csv")

print("\nCOLUMNAS DE Player_Salary.csv:")
print(player_salary_csv.columns.tolist())

print("\nDIMENSIONES:")
print(player_salary_csv.shape)

print("\nPRIMERAS FILAS:")
print(player_salary_csv.head()) 

# ==========================================================
# PREPARAR SALARIO_JUGADOR
# ==========================================================

salarios_jugador = player_salary_csv.copy()

# Renombrar según nuestro modelo
salarios_jugador = salarios_jugador.rename(
    columns={
        "slugSeason": "nombre_temporada",
        "nameTeam": "nombre_equipo",
        "namePlayer": "nombre_jugador_fuente",
        "statusPlayer": "estado_jugador",
        "isFinalSeason": "temporada_final",
        "isOnRoster": "en_roster",
        "isNonGuaranteed": "no_garantizado",
        "isTeamOption": "opcion_equipo",
        "isPlayerOption": "opcion_jugador",
        "typeContractDetail": "tipo_contrato",
        "value": "salario"
    }
)

# ==========================================================
# BUSCAR IDS A PARTIR DE LOS NOMBRES
# ==========================================================

mapa_jugadores = dict(
    zip(
        jugadores["nombre_completo"],
        jugadores["id_jugador"]
    )
)

mapa_equipos = dict(
    zip(
        equipos["nombre_equipo"],
        equipos["id_equipo"]
    )
)

# Las temporadas las consultamos de PostgreSQL
cursor.execute("""
    SELECT id_temporada, nombre_temporada
    FROM temporada;
""")

mapa_temporadas = {
    nombre: id_temporada
    for id_temporada, nombre in cursor.fetchall()
}

salarios_jugador["id_jugador"] = (
    salarios_jugador["nombre_jugador_fuente"]
    .map(mapa_jugadores)
)

salarios_jugador["id_equipo"] = (
    salarios_jugador["nombre_equipo"]
    .map(mapa_equipos)
)

salarios_jugador["id_temporada"] = (
    salarios_jugador["nombre_temporada"]
    .map(mapa_temporadas)
)

# ==========================================================
# CONVERTIR BOOLEANOS
# ==========================================================

columnas_booleanas_salario = [
    "temporada_final",
    "en_roster",
    "no_garantizado",
    "opcion_equipo",
    "opcion_jugador"
]

for columna in columnas_booleanas_salario:
    salarios_jugador[columna] = salarios_jugador[columna].map({
        0: False,
        1: True,
        False: False,
        True: True
    })

# isWaived no lo habíamos renombrado
salarios_jugador["fue_cortado"] = salarios_jugador["isWaived"].map({
    0: False,
    1: True,
    False: False,
    True: True
})


# ==========================================================
# VALIDAR RELACIONES
# ==========================================================

print("\nSALARIOS SIN JUGADOR RELACIONADO:")
print(salarios_jugador["id_jugador"].isna().sum())

print("\nSALARIOS SIN EQUIPO RELACIONADO:")
print(salarios_jugador["id_equipo"].isna().sum())

print("\nSALARIOS SIN TEMPORADA RELACIONADA:")
print(salarios_jugador["id_temporada"].isna().sum())

print("\nTEMPORADAS PRESENTES EN PLAYER_SALARY:")
print(
    sorted(
        salarios_jugador["nombre_temporada"]
        .dropna()
        .unique()
    )
)

print("\nEJEMPLOS SIN JUGADOR:")
print(
    salarios_jugador.loc[
        salarios_jugador["id_jugador"].isna(),
        ["nombre_jugador_fuente"]
    ]
    .drop_duplicates()
    .head(20)
)

print("\nEJEMPLOS SIN EQUIPO:")
print(
    salarios_jugador.loc[
        salarios_jugador["id_equipo"].isna(),
        ["nombre_equipo"]
    ]
    .drop_duplicates()
    .head(20)
)
salarios_jugador = salarios_jugador[
    [
        "id_jugador",
        "id_equipo",
        "id_temporada",
        "nombre_jugador_fuente",
        "estado_jugador",
        "temporada_final",
        "fue_cortado",
        "en_roster",
        "no_garantizado",
        "opcion_equipo",
        "opcion_jugador",
        "tipo_contrato",
        "salario"
    ]
].copy()

# NaN -> NULL
salarios_jugador = salarios_jugador.astype(object).where(
    pd.notna(salarios_jugador),
    None
)

print("\nDATOS PREPARADOS PARA SALARIO_JUGADOR:")
print(salarios_jugador.head())

print("\nDimensiones:")
print(salarios_jugador.shape)

# ==========================================================
# INSERTAR SALARIO_JUGADOR
# ==========================================================

sql_salario_jugador = """
INSERT INTO salario_jugador (
    id_jugador,
    id_equipo,
    id_temporada,
    nombre_jugador_fuente,
    estado_jugador,
    temporada_final,
    fue_cortado,
    en_roster,
    no_garantizado,
    opcion_equipo,
    opcion_jugador,
    tipo_contrato,
    salario
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s
);
"""

cursor.execute("TRUNCATE TABLE salario_jugador RESTART IDENTITY;")

for _, fila in salarios_jugador.iterrows():

    valores = (
        fila["id_jugador"],
        fila["id_equipo"],
        fila["id_temporada"],
        fila["nombre_jugador_fuente"],
        fila["estado_jugador"],
        fila["temporada_final"],
        fila["fue_cortado"],
        fila["en_roster"],
        fila["no_garantizado"],
        fila["opcion_equipo"],
        fila["opcion_jugador"],
        fila["tipo_contrato"],
        fila["salario"]
    )

    cursor.execute(sql_salario_jugador, valores)

conexion.commit()

print("\nSalarios de jugadores insertados correctamente.")

# ==========================================================
# REVISAR TEAM_SALARY.CSV
# ==========================================================

team_salary_csv = pd.read_csv("data/Team_Salary.csv")

print("\nCOLUMNAS DE Team_Salary.csv:")
print(team_salary_csv.columns.tolist())

print("\nDIMENSIONES:")
print(team_salary_csv.shape)

print("\nPRIMERAS FILAS:")
print(team_salary_csv.head())
# ==========================================================
# PREPARAR SALARIOS PARA ESTADISTICA_EQUIPO_TEMPORADA
# ==========================================================

columnas_salarios = [
    "X2020-21",
    "X2021-22",
    "X2022-23",
    "X2023-24",
    "X2024-25",
    "X2025-26"
]

# Convertir temporadas que están como columnas a filas
salarios_equipo = team_salary_csv.melt(
    id_vars=["nameTeam"],
    value_vars=columnas_salarios,
    var_name="nombre_temporada",
    value_name="salario"
)

# Quitar la X inicial
salarios_equipo["nombre_temporada"] = (
    salarios_equipo["nombre_temporada"]
    .str.replace("X", "", n=1)
)

print("\nSALARIOS DESPUES DEL MELT:")
print(salarios_equipo.head(10))

print("\nDimensiones:")
print(salarios_equipo.shape)

# ==========================================================
# RELACIONAR EQUIPO Y TEMPORADA
# ==========================================================

salarios_equipo["id_equipo"] = (
    salarios_equipo["nameTeam"]
    .map(mapa_equipos)
)

salarios_equipo["id_temporada"] = (
    salarios_equipo["nombre_temporada"]
    .map(mapa_temporadas)
)

print(
    "\nSalarios sin equipo relacionado:",
    salarios_equipo["id_equipo"].isna().sum()
)

print(
    "Salarios sin temporada relacionada:",
    salarios_equipo["id_temporada"].isna().sum()
)

print(
    "\nCantidad de salarios con valor 0:",
    (salarios_equipo["salario"] == 0).sum()
)

# En este dataset, 0 representa ausencia de información,
# no un salario real de cero.
salarios_equipo.loc[
    salarios_equipo["salario"] == 0,
    "salario"
] = None

salarios_equipo = salarios_equipo[
    [
        "id_equipo",
        "id_temporada",
        "salario"
    ]
].copy()

salarios_equipo = salarios_equipo.astype(object).where(
    pd.notna(salarios_equipo),
    None
)

print("\nDATOS DE SALARIO PARA ESTADISTICA_EQUIPO_TEMPORADA:")
print(salarios_equipo.head())

print("\nDimensiones finales:")
print(salarios_equipo.shape)

# ==========================================================
# INSERTAR SALARIOS EN ESTADISTICA_EQUIPO_TEMPORADA
# ==========================================================

sql_salario_equipo = """
INSERT INTO estadistica_equipo_temporada (
    id_equipo,
    id_temporada,
    salario
)
VALUES (%s, %s, %s)
ON CONFLICT (id_equipo, id_temporada)
DO UPDATE SET
    salario = EXCLUDED.salario;
"""

for _, fila in salarios_equipo.iterrows():

    valores = (
        fila["id_equipo"],
        fila["id_temporada"],
        fila["salario"]
    )

    cursor.execute(sql_salario_equipo, valores)

conexion.commit()

print(
    "\nSalarios de equipos insertados correctamente "
    "en estadistica_equipo_temporada."
)

# ==========================================================
# REVISAR GAME.CSV
# ==========================================================

game_csv = pd.read_csv("data/Game.csv")

print("\nCOLUMNAS DE Game.csv:")
print(game_csv.columns.tolist())

print("\nDIMENSIONES:")
print(game_csv.shape)

print("\nPRIMERAS FILAS:")
print(game_csv.head())

print("\nVALORES DE SEASON_ID:")
print(sorted(game_csv["SEASON_ID"].dropna().unique())[:20])

print("\nCantidad de temporadas diferentes:")
print(game_csv["SEASON_ID"].nunique())

print("\nFILAS TOTALES GAME:")
print(len(game_csv))

print("\nGAME_ID UNICOS:")
print(game_csv["GAME_ID"].nunique())

print("\nGAME_ID DUPLICADOS:")
print(game_csv["GAME_ID"].duplicated().sum())

# ==========================================================
# AGREGAR TEMPORADAS HISTORICAS DESDE GAME.CSV
# ==========================================================

anios_game = sorted(
    game_csv["SEASON"]
    .dropna()
    .astype(int)
    .unique()
)

temporadas_game = [
    f"{anio}-{str(anio + 1)[-2:]}"
    for anio in anios_game
]

print("\nTEMPORADAS CONSTRUIDAS DESDE GAME:")
print(temporadas_game)

print("\nCantidad:")
print(len(temporadas_game))

for nombre_temporada in temporadas_game:
    cursor.execute(
        """
        INSERT INTO temporada (nombre_temporada)
        VALUES (%s)
        ON CONFLICT (nombre_temporada) DO NOTHING;
        """,
        (nombre_temporada,)
    )

conexion.commit()

print("\nTemporadas históricas insertadas.")

cursor.execute("""
    SELECT id_temporada, nombre_temporada
    FROM temporada;
""")

mapa_temporadas = {
    nombre: id_temporada
    for id_temporada, nombre in cursor.fetchall()
}

print("\nTotal de temporadas en PostgreSQL:")
print(len(mapa_temporadas))

# ==========================================================
# PREPARAR PARTIDO
# ==========================================================

partidos = game_csv[
    [
        "GAME_ID",
        "SEASON",
        "TEAM_ID_HOME",
        "TEAM_ID_AWAY",
        "GAME_DATE",
        "GAME_TIME",
        "GAME_STATUS_TEXT",
        "ATTENDANCE",

        "PTS_HOME",
        "REB_HOME",
        "AST_HOME",
        "STL_HOME",
        "BLK_HOME",
        "TOV_HOME",

        "PTS_AWAY",
        "REB_AWAY",
        "AST_AWAY",
        "STL_AWAY",
        "BLK_AWAY",
        "WL_HOME",
        "WL_AWAY",
        "TOV_AWAY"
    ]
].copy()

partidos = partidos.rename(
    columns={
        "GAME_ID": "id_partido",
        "TEAM_ID_HOME": "id_equipo_local",
        "TEAM_ID_AWAY": "id_equipo_visitante",
        "GAME_DATE": "fecha_partido",
        "GAME_TIME": "hora_partido",
        "GAME_STATUS_TEXT": "estado_partido",
        "ATTENDANCE": "asistencia",

        "PTS_HOME": "puntos_local",
        "REB_HOME": "rebotes_local",
        "AST_HOME": "asistencias_local",
        "STL_HOME": "robos_local",
        "BLK_HOME": "bloqueos_local",
        "TOV_HOME": "perdidas_local",

        "PTS_AWAY": "puntos_visitante",
        "REB_AWAY": "rebotes_visitante",
        "AST_AWAY": "asistencias_visitante",
        "STL_AWAY": "robos_visitante",
        "BLK_AWAY": "bloqueos_visitante",
        "WL_HOME": "resultado_local",
        "WL_AWAY": "resultado_visitante",
        "TOV_AWAY": "perdidas_visitante"
    }
)

partidos["nombre_temporada"] = partidos["SEASON"].apply(
    lambda x: (
        f"{int(x)}-{str(int(x) + 1)[-2:]}"
        if pd.notna(x)
        else None
    )
)

partidos["id_temporada"] = (
    partidos["nombre_temporada"]
    .map(mapa_temporadas)
)

ids_equipos = set(equipos["id_equipo"])

locales_faltantes = (
    partidos["id_equipo_local"].notna()
    & ~partidos["id_equipo_local"].isin(ids_equipos)
)

visitantes_faltantes = (
    partidos["id_equipo_visitante"].notna()
    & ~partidos["id_equipo_visitante"].isin(ids_equipos)
)

print(
    "\nPartidos con equipo local no encontrado:",
    locales_faltantes.sum()
)

print(
    "Partidos con equipo visitante no encontrado:",
    visitantes_faltantes.sum()
)

print(
    "Partidos sin temporada relacionada:",
    partidos["id_temporada"].isna().sum()
)

print("\nEquipos locales históricos no encontrados:")
print(
    partidos.loc[
        locales_faltantes,
        ["id_equipo_local"]
    ]
    .drop_duplicates()
    .head(30)
)

print("\nDimensiones de partidos:")
print(partidos.shape)

# ==========================================================
# AGREGAR EQUIPOS HISTORICOS ENCONTRADOS EN GAME.CSV
# ==========================================================

# Equipos históricos que aparecen como locales
equipos_historicos_home = game_csv[
    [
        "TEAM_ID_HOME",
        "TEAM_NAME_HOME",
        "TEAM_ABBREVIATION_HOME",
        "TEAM_CITY_HOME"
    ]
].copy()

equipos_historicos_home.columns = [
    "id_equipo",
    "nombre_equipo",
    "abreviatura",
    "ciudad"
]


# Equipos históricos que aparecen como visitantes
equipos_historicos_away = game_csv[
    [
        "TEAM_ID_AWAY",
        "TEAM_NAME_AWAY",
        "TEAM_ABBREVIATION_AWAY",
        "TEAM_CITY_AWAY"
    ]
].copy()

equipos_historicos_away.columns = [
    "id_equipo",
    "nombre_equipo",
    "abreviatura",
    "ciudad"
]


# Unir locales y visitantes
equipos_historicos = pd.concat(
    [
        equipos_historicos_home,
        equipos_historicos_away
    ],
    ignore_index=True
)


# Eliminar registros sin ID
equipos_historicos = equipos_historicos.dropna(
    subset=["id_equipo"]
)


# Convertir ID a entero
equipos_historicos["id_equipo"] = (
    equipos_historicos["id_equipo"].astype(int)
)


# Conservar una fila por ID
equipos_historicos = equipos_historicos.drop_duplicates(
    subset=["id_equipo"]
)


# Quedarnos solamente con IDs que todavía no existen
ids_equipos_actuales = set(equipos["id_equipo"])

equipos_historicos = equipos_historicos[
    ~equipos_historicos["id_equipo"].isin(ids_equipos_actuales)
]


# NaN -> NULL
equipos_historicos = equipos_historicos.astype(object).where(
    pd.notna(equipos_historicos),
    None
)

print("\nEQUIPOS HISTORICOS NUEVOS:")
print(equipos_historicos)

print("\nCantidad:")
print(equipos_historicos.shape)

# ==========================================================
# INSERTAR EQUIPOS HISTORICOS EN POSTGRESQL
# ==========================================================

sql_equipo_historico = """
INSERT INTO equipo (
    id_equipo,
    nombre_equipo,
    abreviatura,
    ciudad
)
VALUES (%s, %s, %s, %s)
ON CONFLICT (id_equipo) DO NOTHING;
"""

for _, fila in equipos_historicos.iterrows():

    valores = (
        fila["id_equipo"],
        fila["nombre_equipo"],
        fila["abreviatura"],
        fila["ciudad"]
    )

    cursor.execute(sql_equipo_historico, valores)

conexion.commit()

print("\nEquipos históricos insertados correctamente.")

cursor.execute("""
    SELECT id_equipo
    FROM equipo;
""")

ids_equipos = {
    fila[0]
    for fila in cursor.fetchall()
}

print("\nTotal de equipos disponibles en PostgreSQL:")
print(len(ids_equipos))

locales_faltantes = (
    partidos["id_equipo_local"].notna()
    & ~partidos["id_equipo_local"].isin(ids_equipos)
)

visitantes_faltantes = (
    partidos["id_equipo_visitante"].notna()
    & ~partidos["id_equipo_visitante"].isin(ids_equipos)
)

print(
    "\nDESPUÉS DE AGREGAR EQUIPOS HISTÓRICOS:"
)

print(
    "Partidos con equipo local no encontrado:",
    locales_faltantes.sum()
)

print(
    "Partidos con equipo visitante no encontrado:",
    visitantes_faltantes.sum()
)

print(
    "Partidos sin temporada relacionada:",
    partidos["id_temporada"].isna().sum()
)

# ==========================================================
# LIMPIAR Y CONVERTIR TIPOS DE PARTIDO
# ==========================================================

# Convertir fecha a formato de fecha válido
partidos["fecha_partido"] = pd.to_datetime(
    partidos["fecha_partido"],
    errors="coerce"
).dt.date


# ----------------------------------------------------------
# GAME_TIME puede contener NaN.
# Convertimos las horas válidas y los faltantes quedan NULL.
# ----------------------------------------------------------

partidos["hora_partido"] = pd.to_datetime(
    partidos["hora_partido"],
    errors="coerce"
).dt.time


# ----------------------------------------------------------
# Columnas que PostgreSQL espera como enteros
# ----------------------------------------------------------

columnas_enteras_partido = [
    "id_partido",
    "id_temporada",
    "id_equipo_local",
    "id_equipo_visitante",
    "asistencia",
    "puntos_local",
    "puntos_visitante",
    "rebotes_local",
    "rebotes_visitante",
    "asistencias_local",
    "asistencias_visitante",
    "robos_local",
    "robos_visitante",
    "bloqueos_local",
    "bloqueos_visitante",
    "perdidas_local",
    "perdidas_visitante"
]

for columna in columnas_enteras_partido:
    partidos[columna] = partidos[columna].apply(
        lambda x: int(x) if pd.notna(x) else None
    )


# ----------------------------------------------------------
# Convertir todos los valores faltantes restantes a None.
# psycopg2 transforma None en NULL de PostgreSQL.
# ----------------------------------------------------------

partidos = partidos.astype(object).where(
    pd.notna(partidos),
    None
)

partidos = partidos[
    [
        "id_partido",
        "id_temporada",
        "id_equipo_local",
        "id_equipo_visitante",
        "fecha_partido",
        "hora_partido",
        "asistencia",
        "estado_partido",
        "puntos_local",
        "puntos_visitante",
        "rebotes_local",
        "rebotes_visitante",
        "asistencias_local",
        "asistencias_visitante",
        "robos_local",
        "robos_visitante",
        "bloqueos_local",
        "bloqueos_visitante",
        "perdidas_local",
        "perdidas_visitante",
        "resultado_local",
        "resultado_visitante"
    ]
].copy()
# ==========================================================
# INSERTAR PARTIDOS EN POSTGRESQL
# ==========================================================

sql_partido = """
INSERT INTO partido (
    id_partido,
    id_temporada,
    id_equipo_local,
    id_equipo_visitante,
    fecha_partido,
    hora_partido,
    asistencia,
    estado_partido,
    puntos_local,
    puntos_visitante,
    rebotes_local,
    rebotes_visitante,
    asistencias_local,
    asistencias_visitante,
    robos_local,
    robos_visitante,
    bloqueos_local,
    bloqueos_visitante,
    perdidas_local,
    perdidas_visitante,
    resultado_local,
    resultado_visitante
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s
)
ON CONFLICT (id_partido) DO NOTHING;
"""

for _, fila in partidos.iterrows():

    valores = (
        fila["id_partido"],
        fila["id_temporada"],
        fila["id_equipo_local"],
        fila["id_equipo_visitante"],
        fila["fecha_partido"],
        fila["hora_partido"],
        fila["asistencia"],
        fila["estado_partido"],
        fila["puntos_local"],
        fila["puntos_visitante"],
        fila["rebotes_local"],
        fila["rebotes_visitante"],
        fila["asistencias_local"],
        fila["asistencias_visitante"],
        fila["robos_local"],
        fila["robos_visitante"],
        fila["bloqueos_local"],
        fila["bloqueos_visitante"],
        fila["perdidas_local"],
        fila["perdidas_visitante"],
        fila["resultado_local"],
        fila["resultado_visitante"]
    )

    cursor.execute(sql_partido, valores)

conexion.commit()

print("\nPartidos insertados correctamente en PostgreSQL.")

# ==========================================================
# REVISAR GAME_INACTIVE_PLAYERS.CSV
# ==========================================================

inactive_csv = pd.read_csv("data/Game_Inactive_Players.csv")

print("\nCOLUMNAS DE Game_Inactive_Players.csv:")
print(inactive_csv.columns.tolist())

print("\nDIMENSIONES:")
print(inactive_csv.shape)

print("\nPRIMERAS FILAS:")
print(inactive_csv.head())
# ==========================================================
# PREPARAR JUGADOR_INACTIVO
# ==========================================================

jugadores_inactivos = inactive_csv[
    [
        "PLAYER_ID",
        "FIRST_NAME",
        "LAST_NAME",
        "JERSEY_NUM",
        "TEAM_ID",
        "GAME_ID"
    ]
].copy()

jugadores_inactivos = jugadores_inactivos.rename(
    columns={
        "PLAYER_ID": "id_jugador",
        "FIRST_NAME": "nombre",
        "LAST_NAME": "apellido",
        "JERSEY_NUM": "numero_camiseta",
        "TEAM_ID": "id_equipo",
        "GAME_ID": "id_partido"
    }
)

# Crear nombre de respaldo
jugadores_inactivos["nombre_jugador_fuente"] = (
    jugadores_inactivos["nombre"].fillna("")
    + " "
    + jugadores_inactivos["apellido"].fillna("")
).str.strip()


# ==========================================================
# CONVERTIR IDS
# ==========================================================

for columna in ["id_jugador", "id_equipo", "id_partido"]:
    jugadores_inactivos[columna] = jugadores_inactivos[columna].apply(
        lambda x: int(x) if pd.notna(x) else None
    )


# ==========================================================
# OBTENER IDS VALIDOS DESDE POSTGRESQL
# ==========================================================

cursor.execute("SELECT id_jugador FROM jugador;")
ids_jugadores_bd = {fila[0] for fila in cursor.fetchall()}

cursor.execute("SELECT id_equipo FROM equipo;")
ids_equipos_bd = {fila[0] for fila in cursor.fetchall()}

cursor.execute("SELECT id_partido FROM partido;")
ids_partidos_bd = {fila[0] for fila in cursor.fetchall()}


# ==========================================================
# VALIDAR FOREIGN KEYS
# ==========================================================

inactivos_sin_jugador = (
    jugadores_inactivos["id_jugador"].notna()
    & ~jugadores_inactivos["id_jugador"].isin(ids_jugadores_bd)
)

inactivos_sin_equipo = (
    jugadores_inactivos["id_equipo"].notna()
    & ~jugadores_inactivos["id_equipo"].isin(ids_equipos_bd)
)

inactivos_sin_partido = (
    jugadores_inactivos["id_partido"].notna()
    & ~jugadores_inactivos["id_partido"].isin(ids_partidos_bd)
)


print(
    "\nInactivos sin jugador relacionado:",
    inactivos_sin_jugador.sum()
)

print(
    "Inactivos sin equipo relacionado:",
    inactivos_sin_equipo.sum()
)

print(
    "Inactivos sin partido relacionado:",
    inactivos_sin_partido.sum()
)

print(
    "Registros sin PLAYER_ID:",
    jugadores_inactivos["id_jugador"].isna().sum()
)

print("\nDimensiones finales para jugador_inactivo:")
print(jugadores_inactivos.shape)

# ==========================================================
# AJUSTAR JUGADORES SIN FK
# ==========================================================

jugadores_inactivos.loc[
    inactivos_sin_jugador,
    "id_jugador"
] = None

# Ya no necesitamos nombre y apellido por separado
jugadores_inactivos = jugadores_inactivos[
    [
        "id_jugador",
        "id_partido",
        "id_equipo",
        "numero_camiseta",
        "nombre_jugador_fuente"
    ]
].copy()

# NaN -> NULL
jugadores_inactivos = jugadores_inactivos.astype(object).where(
    pd.notna(jugadores_inactivos),
    None
)

print("\nDATOS FINALES DE JUGADOR_INACTIVO:")
print(jugadores_inactivos.head())

print("\nDimensiones:")
print(jugadores_inactivos.shape)

# ==========================================================
# INSERTAR JUGADOR_INACTIVO
# ==========================================================

sql_jugador_inactivo = """
INSERT INTO jugador_inactivo (
    id_jugador,
    id_partido,
    id_equipo,
    numero_camiseta,
    nombre_jugador_fuente
)
VALUES (%s, %s, %s, %s, %s);
"""

cursor.execute(
    "TRUNCATE TABLE jugador_inactivo RESTART IDENTITY;"
)

for _, fila in jugadores_inactivos.iterrows():

    valores = (
        fila["id_jugador"],
        fila["id_partido"],
        fila["id_equipo"],
        fila["numero_camiseta"],
        fila["nombre_jugador_fuente"]
    )

    cursor.execute(sql_jugador_inactivo, valores)

conexion.commit()

print("\nJugadores inactivos insertados correctamente.")

# ==========================================================
# PREPARAR ARBITRO_PARTIDO
# ==========================================================

arbitros_partidos = game_officials[
    [
        "OFFICIAL_ID",
        "GAME_ID"
    ]
].copy()

arbitros_partidos = arbitros_partidos.rename(
    columns={
        "OFFICIAL_ID": "id_arbitro",
        "GAME_ID": "id_partido"
    }
)

# Convertir IDs a enteros
for columna in ["id_arbitro", "id_partido"]:
    arbitros_partidos[columna] = arbitros_partidos[columna].apply(
        lambda x: int(x) if pd.notna(x) else None
    )


# ==========================================================
# VALIDAR FOREIGN KEYS
# ==========================================================

cursor.execute("SELECT id_arbitro FROM arbitro;")
ids_arbitros_bd = {
    fila[0]
    for fila in cursor.fetchall()
}

cursor.execute("SELECT id_partido FROM partido;")
ids_partidos_bd = {
    fila[0]
    for fila in cursor.fetchall()
}

sin_arbitro = (
    arbitros_partidos["id_arbitro"].notna()
    & ~arbitros_partidos["id_arbitro"].isin(ids_arbitros_bd)
)

sin_partido = (
    arbitros_partidos["id_partido"].notna()
    & ~arbitros_partidos["id_partido"].isin(ids_partidos_bd)
)

print(
    "\nRelaciones arbitro-partido sin arbitro:",
    sin_arbitro.sum()
)

print(
    "Relaciones arbitro-partido sin partido:",
    sin_partido.sum()
)

print(
    "Registros sin OFFICIAL_ID:",
    arbitros_partidos["id_arbitro"].isna().sum()
)

print(
    "Registros sin GAME_ID:",
    arbitros_partidos["id_partido"].isna().sum()
)

print("\nDimensiones:")
print(arbitros_partidos.shape)

# ==========================================================
# LIMPIAR DUPLICADOS ARBITRO_PARTIDO
# ==========================================================

arbitros_partidos = arbitros_partidos.drop_duplicates(
    subset=["id_arbitro", "id_partido"]
)

print(
    "\nRelaciones únicas arbitro-partido:",
    arbitros_partidos.shape
)


# ==========================================================
# INSERTAR ARBITRO_PARTIDO EN POSTGRESQL
# ==========================================================

sql_arbitro_partido = """
INSERT INTO arbitro_partido (
    id_arbitro,
    id_partido
)
VALUES (%s, %s)
ON CONFLICT (id_arbitro, id_partido) DO NOTHING;
"""

for _, fila in arbitros_partidos.iterrows():

    valores = (
        int(fila["id_arbitro"]),
        int(fila["id_partido"])
    )

    cursor.execute(sql_arbitro_partido, valores)

conexion.commit()

print("\nRelaciones árbitro-partido insertadas correctamente.")


# REVISAR NEWS.CSV
# ==========================================================

news_csv = pd.read_csv(
    "data/News.csv",
    low_memory=False
)

print("\nCOLUMNAS DE News.csv:")
print(news_csv.columns.tolist())

print("\nDIMENSIONES:")
print(news_csv.shape)

print("\nPRIMERAS FILAS:")
print(news_csv.head())

print("\nTIPOS DE DATOS:")
print(news_csv.dtypes)

# ==========================================================
# PREPARAR TABLA NOTICIA
# ==========================================================

noticias = news_csv[
    [
        "title",
        "author",
        "published_date",
        "link",
        "clean_url",
        "summary",
        "topic",
        "country",
        "language",
        "is_opinion",
        "text"
    ]
].copy()


noticias = noticias.rename(
    columns={
        "title": "titulo",
        "author": "autor",
        "published_date": "fecha_publicacion",
        "link": "url",
        "clean_url": "dominio",
        "summary": "resumen",
        "topic": "tema",
        "country": "pais",
        "language": "idioma",
        "is_opinion": "es_opinion",
        "text": "contenido"
    }
)

noticias["fecha_publicacion"] = pd.to_datetime(
    noticias["fecha_publicacion"],
    errors="coerce"
)

noticias["es_opinion"] = noticias["es_opinion"].map({
    0: False,
    1: True,
    False: False,
    True: True
})

# NaN / NaT -> NULL
noticias = noticias.astype(object).where(
    pd.notna(noticias),
    None
)

print("\nDATOS PREPARADOS PARA NOTICIA:")
print(noticias.head())

print("\nDimensiones:")
print(noticias.shape)

print(
    "\nNoticias sin URL:",
    noticias["url"].isna().sum()
)

print(
    "URLs duplicadas:",
    noticias["url"].duplicated().sum()
)
print(
    "Títulos duplicados:",
    noticias["titulo"].duplicated().sum()
)

# ==========================================================
# ELIMINAR NOTICIAS DUPLICADAS
# ==========================================================

noticias = noticias.drop_duplicates(
    subset=["url"],
    keep="first"
)

print("\nDimensiones después de eliminar URLs duplicadas:")
print(noticias.shape)

# ==========================================================
# INSERTAR NOTICIAS EN POSTGRESQL
# ==========================================================

sql_noticia = """
INSERT INTO noticia (
    titulo,
    autor,
    fecha_publicacion,
    url,
    dominio,
    resumen,
    tema,
    pais,
    idioma,
    es_opinion,
    contenido
)
VALUES (
    %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s
)
ON CONFLICT (url) DO NOTHING;
"""

for _, fila in noticias.iterrows():

    valores = (
        fila["titulo"],
        fila["autor"],
        fila["fecha_publicacion"],
        fila["url"],
        fila["dominio"],
        fila["resumen"],
        fila["tema"],
        fila["pais"],
        fila["idioma"],
        fila["es_opinion"],
        fila["contenido"]
    )

    cursor.execute(sql_noticia, valores)

conexion.commit()

print("\nNoticias insertadas correctamente en PostgreSQL.")

