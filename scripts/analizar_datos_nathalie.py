import pandas as pd
from pathlib import Path


# Ruta de la carpeta donde se encuentran los CSV
RUTA_DATA = Path(__file__).resolve().parent.parent / "data" / "csv"


# Archivos asignados a Nathalie
archivos = [
    "Team.csv",
    "Team_Attributes.csv",
    "Team_History.csv",
    "Player.csv",
    "Player_Salary.csv"
]



print("ANÁLISIS INICIAL DE LOS CSV - NATHALIE")


for archivo in archivos:

    ruta = RUTA_DATA / archivo

    print(f"ARCHIVO: {archivo}")

    # Leer CSV
    df = pd.read_csv(ruta)

    # Dimensiones
    print(f"Cantidad de filas: {df.shape[0]}")
    print(f"Cantidad de columnas: {df.shape[1]}")

    # Columnas
    print("\nColumnas:")
    for columna in df.columns:
        print(f" - {columna}")

    # Tipos de datos detectados por pandas
    print("\nTipos de datos:")
    print(df.dtypes)

    # Valores nulos
    print("\nValores nulos por columna:")
    print(df.isnull().sum())

    # Duplicados exactos
    duplicados = df.duplicated().sum()
    print(f"\nRegistros duplicados exactos: {duplicados}")

    # Primeros registros
    print("\nPrimeros 5 registros:")
    print(df.head())


print("FIN DEL ANÁLISIS INICIAL")

print("COMPARACIÓN DE IDENTIFICADORES DE EQUIPOS")

team = pd.read_csv(RUTA_DATA / "Team.csv")
team_attributes = pd.read_csv(RUTA_DATA / "Team_Attributes.csv")

ids_team = set(team["id"])
ids_attributes = set(team_attributes["ID"])

print(f"IDs únicos en Team.csv: {len(ids_team)}")
print(f"IDs únicos en Team_Attributes.csv: {len(ids_attributes)}")

print(
    "¿Los dos archivos contienen exactamente los mismos IDs?",
    ids_team == ids_attributes
)

print("IDs presentes en Team.csv pero no en Team_Attributes.csv:")
print(ids_team - ids_attributes)

print("IDs presentes en Team_Attributes.csv pero no en Team.csv:")
print(ids_attributes - ids_team)

print("ANÁLISIS DE TEAM_HISTORY")


team_history = pd.read_csv(RUTA_DATA / "Team_History.csv")

# Cantidad de equipos diferentes
print(f"Equipos únicos en Team_History.csv: {team_history['ID'].nunique()}")

# Cantidad de registros históricos por equipo
registros_por_equipo = (
    team_history
    .groupby("ID")
    .size()
    .sort_values(ascending=False)
)

print("\nCantidad de registros históricos por equipo:")
print(registros_por_equipo)

# Comprobar relación con Team.csv
ids_history = set(team_history["ID"])
ids_team = set(team["id"])

print("\n¿Todos los equipos históricos existen en Team.csv?")
print(ids_history.issubset(ids_team))

print("\nIDs de Team_History que no existen en Team.csv:")
print(ids_history - ids_team)

# Buscar IDs repetidos
print("\nCantidad de registros con ID repetido:")
print(team_history["ID"].duplicated().sum())

print("COMPROBACIÓN DE CLAVES CANDIDATAS - TEAM_HISTORY")


# Candidata 1: ID + YEARFOUNDED
duplicados_id_anio = team_history.duplicated(
    subset=["ID", "YEARFOUNDED"]
).sum()

print("\nCandidata: (ID, YEARFOUNDED)")
print(f"Combinaciones duplicadas: {duplicados_id_anio}")
print(
    "¿Puede identificar cada registro de forma única?",
    duplicados_id_anio == 0
)

# Candidata 2: ID + CITY + NICKNAME
duplicados_id_ciudad_apodo = team_history.duplicated(
    subset=["ID", "CITY", "NICKNAME"]
).sum()

print("\nCandidata: (ID, CITY, NICKNAME)")
print(f"Combinaciones duplicadas: {duplicados_id_ciudad_apodo}")
print(
    "¿Puede identificar cada registro de forma única?",
    duplicados_id_ciudad_apodo == 0
)

# Candidata 3: ID + YEARFOUNDED + YEARACTIVETILL
duplicados_periodo = team_history.duplicated(
    subset=["ID", "YEARFOUNDED", "YEARACTIVETILL"]
).sum()

print("\nCandidata: (ID, YEARFOUNDED, YEARACTIVETILL)")
print(f"Combinaciones duplicadas: {duplicados_periodo}")
print(
    "¿Puede identificar cada registro de forma única?",
    duplicados_periodo == 0
)

# Comprobar si existen filas históricas completamente duplicadas
duplicados_completos = team_history.duplicated().sum()

print("\nFilas históricas completamente duplicadas:")
print(duplicados_completos)


print("ANÁLISIS DE PLAYER")


player = pd.read_csv(RUTA_DATA / "Player.csv")

# Cantidad de registros
print(f"Cantidad de jugadores: {len(player)}")

# Cantidad de IDs únicos
print(f"IDs únicos: {player['id'].nunique()}")

# Comprobar si id puede funcionar como PK
ids_duplicados = player["id"].duplicated().sum()

print(f"IDs duplicados: {ids_duplicados}")
print(
    "¿id puede identificar de forma única a cada jugador?",
    ids_duplicados == 0
)

# Valores nulos
print("\nValores nulos por columna:")
print(player.isnull().sum())

# Analizar nombres completos
nombres_duplicados = player["full_name"].duplicated().sum()

print(f"\nNombres completos duplicados: {nombres_duplicados}")

# Mostrar los nombres repetidos, si existen
jugadores_nombre_repetido = player[
    player["full_name"].duplicated(keep=False)
].sort_values("full_name")

print("\nJugadores con full_name repetido:")
if jugadores_nombre_repetido.empty:
    print("No se encontraron nombres completos repetidos.")
else:
    print(
        jugadores_nombre_repetido[
            ["id", "full_name", "first_name", "last_name"]
        ].to_string(index=False)
    )

# Mostrar registros que contienen algún valor nulo
jugadores_con_nulos = player[player.isnull().any(axis=1)]

print("\nRegistros con valores nulos:")
if jugadores_con_nulos.empty:
    print("No se encontraron registros con valores nulos.")
else:
    print(jugadores_con_nulos.to_string(index=False))

print("ANÁLISIS DE PLAYER_SALARY")


player_salary = pd.read_csv(RUTA_DATA / "Player_Salary.csv")

# Información general
print(f"Cantidad de registros: {len(player_salary)}")
print(f"Cantidad de columnas: {len(player_salary.columns)}")

print("\nColumnas:")
print(player_salary.columns.tolist())

# Valores nulos
print("\nValores nulos por columna:")
print(player_salary.isnull().sum())

# Duplicados completos
print(f"\nFilas completamente duplicadas: {player_salary.duplicated().sum()}")

# Temporadas
print("\nTemporadas encontradas:")
print(sorted(player_salary["slugSeason"].unique()))

print(f"Cantidad de temporadas: {player_salary['slugSeason'].nunique()}")

# Equipos
print(f"\nEquipos distintos en salarios: {player_salary['nameTeam'].nunique()}")

print("\nNombres de equipos:")
print(sorted(player_salary["nameTeam"].unique()))

# Jugadores
print(f"\nNombres de jugadores distintos: {player_salary['namePlayer'].nunique()}")

# Valores de salario
print("\nResumen de value:")
print(player_salary["value"].describe())

# Estados booleanos / indicadores
columnas_estado = [
    "statusPlayer",
    "isFinalSeason",
    "isWaived",
    "isOnRoster",
    "isNonGuaranteed",
    "isTeamOption",
    "isPlayerOption",
    "typeContractDetail"
]

print("\nValores distintos en columnas de estado/contrato:")

for columna in columnas_estado:
    print(f"\n{columna}:")
    print(player_salary[columna].value_counts(dropna=False))



print("RELACIÓN PLAYER_SALARY -> TEAM")


# Nombres únicos de equipos
equipos_salary = set(player_salary["nameTeam"])
equipos_team = set(team["full_name"])

print(f"Equipos únicos en Player_Salary: {len(equipos_salary)}")
print(f"Equipos únicos en Team: {len(equipos_team)}")

print(
    "¿Todos los equipos de Player_Salary existen en Team?",
    equipos_salary.issubset(equipos_team)
)

print("\nEquipos de Player_Salary sin coincidencia en Team:")
print(equipos_salary - equipos_team)


print("RELACIÓN PLAYER_SALARY -> PLAYER")

jugadores_salary = set(player_salary["namePlayer"])
jugadores_player = set(player["full_name"])

coinciden = jugadores_salary & jugadores_player
no_coinciden = jugadores_salary - jugadores_player

print(f"Jugadores distintos en Player_Salary: {len(jugadores_salary)}")
print(f"Jugadores con coincidencia exacta en Player: {len(coinciden)}")
print(f"Jugadores sin coincidencia exacta: {len(no_coinciden)}")

print("\nNombres sin coincidencia exacta:")
print(sorted(no_coinciden))


# Nombres que sí coinciden, pero corresponden a más de un id_jugador
conteo_nombres_player = player.groupby("full_name")["id"].nunique()

nombres_ambiguos = set(
    conteo_nombres_player[conteo_nombres_player > 1].index
)

ambiguos_en_salary = jugadores_salary & nombres_ambiguos

print("\nNombres presentes en salarios que son ambiguos en Player.csv:")
print(f"Cantidad: {len(ambiguos_en_salary)}")
print(sorted(ambiguos_en_salary))




print("NORMALIZACIÓN DE NOMBRES DE JUGADORES")


import re
import unicodedata


def normalizar_nombre(nombre):
    nombre = str(nombre).strip()

    # Eliminar indicadores W o E al final del nombre
    nombre = re.sub(r"\s+[WE]$", "", nombre)

    # Convertir a minúsculas
    nombre = nombre.lower()

    # Eliminar tildes/diacríticos
    nombre = unicodedata.normalize("NFKD", nombre)
    nombre = "".join(
        caracter for caracter in nombre
        if not unicodedata.combining(caracter)
    )

    # Conservar únicamente letras y números
    nombre = re.sub(r"[^a-z0-9]", "", nombre)

    return nombre


player["nombre_normalizado"] = player["full_name"].apply(normalizar_nombre)

player_salary["nombre_normalizado"] = (
    player_salary["namePlayer"].apply(normalizar_nombre)
)


# Comprobar si una forma normalizada corresponde a varios jugadores
conteo_normalizado = (
    player
    .groupby("nombre_normalizado")["id"]
    .nunique()
)

normalizados_ambiguos = set(
    conteo_normalizado[conteo_normalizado > 1].index
)


# Nombres que inicialmente no coincidieron
salary_sin_match = player_salary[
    ~player_salary["namePlayer"].isin(player["full_name"])
].copy()


normalizados_player = set(player["nombre_normalizado"])

salary_sin_match["match_normalizado"] = (
    salary_sin_match["nombre_normalizado"].isin(normalizados_player)
)

recuperados = salary_sin_match[
    salary_sin_match["match_normalizado"]
]

print(
    "Nombres distintos inicialmente sin coincidencia:",
    salary_sin_match["namePlayer"].nunique()
)

print(
    "Nombres distintos recuperados mediante normalización:",
    recuperados["namePlayer"].nunique()
)


# Comprobar recuperaciones ambiguas
recuperados_ambiguos = recuperados[
    recuperados["nombre_normalizado"].isin(normalizados_ambiguos)
]

print(
    "Recuperaciones que serían ambiguas:",
    recuperados_ambiguos["namePlayer"].nunique()
)


# Nombres que siguen sin coincidencia
sin_match_normalizado = salary_sin_match[
    ~salary_sin_match["match_normalizado"]
]

print(
    "Nombres distintos que siguen sin coincidencia:",
    sin_match_normalizado["namePlayer"].nunique()
)

print("\nNombres que siguen sin coincidencia:")
print(
    sorted(
        sin_match_normalizado["namePlayer"].unique()
    )
)

print("CLAVES CANDIDATAS - PLAYER_SALARY")


def comprobar_clave(columnas):
    duplicados = player_salary.duplicated(
        subset=columnas
    ).sum()

    print(f"\nCandidata: {tuple(columnas)}")
    print(f"Combinaciones duplicadas: {duplicados}")
    print(
        "¿Identifica cada registro de forma única?",
        duplicados == 0
    )


# Jugador + temporada
comprobar_clave([
    "namePlayer",
    "slugSeason"
])

# Jugador + equipo + temporada
comprobar_clave([
    "namePlayer",
    "nameTeam",
    "slugSeason"
])

# Jugador + equipo + temporada + tipo de contrato
comprobar_clave([
    "namePlayer",
    "nameTeam",
    "slugSeason",
    "typeContractDetail"
])

# Comprobar jugadores con más de un equipo en una temporada
jugador_temporada = (
    player_salary
    .groupby(["namePlayer", "slugSeason"])["nameTeam"]
    .nunique()
)

varios_equipos = jugador_temporada[
    jugador_temporada > 1
]

print("\nJugadores que aparecen con más de un equipo en una temporada:")
print(f"Cantidad de casos: {len(varios_equipos)}")

if len(varios_equipos) > 0:
    print(varios_equipos)

print("COBERTURA FINAL DE RELACIÓN CON JUGADOR")

# Nombres exactos disponibles en Player
nombres_exactos_player = set(player["full_name"])

# Formas normalizadas disponibles en Player
normalizados_player = set(player["nombre_normalizado"])

def clasificar_match(nombre):
    # Coincidencia exacta
    if nombre in nombres_exactos_player:
        return "exacto"

    # Coincidencia mediante normalización
    nombre_norm = normalizar_nombre(nombre)

    if (
        nombre_norm in normalizados_player
        and nombre_norm not in normalizados_ambiguos
    ):
        return "normalizado"

    return "sin_coincidencia"


player_salary["tipo_match_jugador"] = (
    player_salary["namePlayer"].apply(clasificar_match)
)

print("\nRegistros por tipo de coincidencia:")
print(
    player_salary["tipo_match_jugador"]
    .value_counts()
)

sin_relacion = player_salary[
    player_salary["tipo_match_jugador"] == "sin_coincidencia"
]

print(
    "\nCantidad total de registros que quedarían sin id_jugador:",
    len(sin_relacion)
)

print(
    "Porcentaje de registros sin id_jugador:",
    round(len(sin_relacion) / len(player_salary) * 100, 2),
    "%"
)