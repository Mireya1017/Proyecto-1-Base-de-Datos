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