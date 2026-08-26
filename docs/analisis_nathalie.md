# Análisis de datos - Nathalie

## 1. Objetivo

Analizar los archivos CSV asignados al bloque de equipos e histórico para identificar las entidades, atributos, relaciones, claves y transformaciones necesarias antes de construir el modelo relacional en PostgreSQL.

## 2. Archivos asignados

Los archivos analizados son:

- `Team.csv`
- `Team_Attributes.csv`
- `Team_History.csv`
- `Player.csv`
- `Player_Salary.csv`

Para cada archivo se revisarán:

- Cantidad de registros y columnas.
- Identificadores disponibles.
- Valores nulos.
- Registros duplicados.
- Atributos redundantes.
- Relaciones con otros archivos.
- Posibles entidades.
- Transformaciones necesarias.
- Atributos que podrían excluirse del modelo final.

## 3. Análisis de Team.csv

`Team.csv` contiene la información general de los equipos.

### Estructura

- Registros: 30
- Columnas: 7
- Registros duplicados exactos: 0
- Valores nulos: 0

Columnas encontradas:

- `id`
- `full_name`
- `abbreviation`
- `nickname`
- `city`
- `state`
- `year_founded`

### Identificador

La columna `id` identifica al equipo. Dentro del modelo relacional se utilizará el nombre estandarizado `id_equipo`.

### Hallazgos

No se encontraron registros duplicados ni valores nulos. El archivo contiene información general que puede utilizarse como base para construir la entidad `EQUIPO`.


## 4. Análisis de Team_Attributes.csv

`Team_Attributes.csv` contiene información adicional sobre los equipos.

### Estructura

- Registros: 30
- Columnas: 14
- Registros duplicados exactos: 0

Se encontraron las siguientes columnas:

- `ID`
- `ABBREVIATION`
- `NICKNAME`
- `YEARFOUNDED`
- `CITY`
- `ARENA`
- `ARENACAPACITY`
- `OWNER`
- `GENERALMANAGER`
- `HEADCOACH`
- `DLEAGUEAFFILIATION`
- `FACEBOOK_WEBSITE_LINK`
- `INSTAGRAM_WEBSITE_LINK`
- `TWITTER_WEBSITE_LINK`

### Valores faltantes

La columna `ARENACAPACITY` presenta 10 valores nulos. Las demás columnas no presentan valores faltantes.

### Redundancia con Team.csv

Se identificaron atributos que representan información ya presente en `Team.csv`:

- `ID` / `id`
- `ABBREVIATION` / `abbreviation`
- `NICKNAME` / `nickname`
- `YEARFOUNDED` / `year_founded`
- `CITY` / `city`

Por lo tanto, almacenar estos atributos nuevamente en una tabla independiente produciría redundancia.

### Decisión de modelado

`Team.csv` y `Team_Attributes.csv` se utilizarán como fuentes para construir una única entidad `EQUIPO`.

`Team.csv` proporcionará la información general del equipo y `Team_Attributes.csv` complementará esta entidad con atributos adicionales.

La capacidad de la arena deberá permitir valores `NULL`, debido a que `ARENACAPACITY` contiene 10 valores faltantes.

Las columnas correspondientes a Facebook, Instagram y Twitter se consideran candidatas a excluirse del modelo final debido a que no aportan directamente al análisis principal del proyecto. Esta decisión será confirmada durante el diseño final de las tablas.