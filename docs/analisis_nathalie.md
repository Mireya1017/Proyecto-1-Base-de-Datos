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

## 5. Análisis de Team_History.csv

`Team_History.csv` contiene información histórica asociada a los equipos.

### Estructura

El archivo contiene las columnas:

- `ID`
- `CITY`
- `NICKNAME`
- `YEARFOUNDED`
- `YEARACTIVETILL`

Se identificaron 30 equipos únicos.

### Análisis del identificador

La columna `ID` se repite dentro del archivo debido a que un mismo equipo puede presentar varios registros históricos.

Se detectaron 30 registros cuyo `ID` ya había aparecido anteriormente. Algunos equipos presentan múltiples registros históricos; el equipo con ID `1610612764`, por ejemplo, presenta 6 registros.

Por lo tanto, `ID` no puede utilizarse por sí solo como clave primaria de la información histórica.

### Relación con Team.csv

Se compararon los identificadores de `Team_History.csv` con los identificadores presentes en `Team.csv`.

Resultado:

- Todos los equipos históricos tienen correspondencia en `Team.csv`.
- No se encontraron identificadores históricos sin equipo asociado.

Esto permite utilizar el identificador del equipo como clave foránea hacia la entidad `EQUIPO`.

### Decisión de modelado

La información histórica se representará mediante una entidad independiente denominada provisionalmente `HISTORIAL_EQUIPO`.

La columna `ID` será transformada al nombre estandarizado `id_equipo` y funcionará como clave foránea hacia `EQUIPO`.

La relación identificada es:

`EQUIPO 1:N HISTORIAL_EQUIPO`

Un equipo puede tener varios registros históricos, mientras que cada registro histórico corresponde a un solo equipo.

La clave primaria definitiva de `HISTORIAL_EQUIPO` será determinada durante el diseño de tablas, debido a que `id_equipo` no es único dentro de los datos históricos.

### Evaluación de la clave primaria

Debido a que `ID` se repite para representar distintas etapas históricas de un mismo equipo, se evaluaron diferentes combinaciones de atributos como posibles claves candidatas.

Resultados:

- `(ID, YEARFOUNDED)`: 0 combinaciones duplicadas.
- `(ID, CITY, NICKNAME)`: 2 combinaciones duplicadas.
- `(ID, YEARFOUNDED, YEARACTIVETILL)`: 0 combinaciones duplicadas.
- Filas completamente duplicadas: 0.

La combinación `(ID, YEARFOUNDED)` permite identificar de forma única los 60 registros históricos.

### Decisión de clave primaria

Se utilizará una clave primaria compuesta formada por:

`(id_equipo, anio_fundacion)`

No se considera necesario crear un identificador artificial `id_historial`, debido a que los datos ya contienen una combinación de atributos que identifica de forma única cada registro histórico.

`id_equipo` también funcionará como clave foránea hacia `EQUIPO`.

La combinación de tres atributos `(ID, YEARFOUNDED, YEARACTIVETILL)` también resultó única, pero se descartó como clave primaria porque `YEARACTIVETILL` no es necesario para garantizar la unicidad.

## 6. Análisis de Player.csv

`Player.csv` contiene información identificadora y general de los jugadores.

### Estructura

El archivo contiene 4,501 registros con las siguientes columnas:

- `id`
- `full_name`
- `first_name`
- `last_name`
- `is_active`

### Análisis del identificador

Se encontraron:

- 4,501 registros.
- 4,501 valores únicos en `id`.
- 0 identificadores duplicados.

Por lo tanto, `id` permite identificar de forma única cada jugador y será transformado al nombre estandarizado `id_jugador`.

`id_jugador` será la clave primaria de la entidad `JUGADOR`.

### Análisis de nombres

Se encontraron 36 valores duplicados en `full_name`.

Esto demuestra que el nombre completo no puede utilizarse como identificador único de un jugador, debido a que jugadores diferentes pueden compartir el mismo nombre.

Por esta razón, las relaciones con otras entidades deberán realizarse mediante `id_jugador` cuando sea posible y no únicamente mediante `full_name`.

### Valores faltantes

Se encontraron 6 valores nulos en `first_name`.

Las demás columnas no presentan valores nulos:

- `id`: 0
- `full_name`: 0
- `first_name`: 6
- `last_name`: 0
- `is_active`: 0

Los registros con `first_name` faltante conservan información en `full_name`, por lo que no serán eliminados.

### Decisión de modelado

Se propone la entidad `JUGADOR` con los siguientes atributos:

- `id_jugador` - clave primaria.
- `nombre_completo`.
- `nombre`.
- `apellido`.
- `esta_activo`.

El atributo `nombre` deberá permitir valores `NULL` debido a los valores faltantes encontrados en la fuente original.

`nombre_completo` no tendrá una restricción `UNIQUE`, ya que se comprobó que existen jugadores diferentes que comparten el mismo nombre.

## 7. Análisis de Player_Salary.csv

`Player_Salary.csv` contiene información salarial y contractual de jugadores asociada con equipos y temporadas.

### Estructura

El archivo contiene:

- 1,292 registros.
- 12 columnas.
- 0 valores nulos.
- 0 filas completamente duplicadas.
- 5 temporadas.
- 30 equipos distintos.
- 520 nombres distintos de jugadores.

Las temporadas encontradas corresponden a:

- `2020-21`
- `2021-22`
- `2022-23`
- `2023-24`
- `2024-25`

### Información salarial

El atributo `value` contiene los valores salariales.

Los valores encontrados se encuentran aproximadamente entre 25,000 y 48,787,680.

### Información contractual

El archivo también contiene atributos relacionados con el estado y características del contrato:

- `statusPlayer`
- `isFinalSeason`
- `isWaived`
- `isOnRoster`
- `isNonGuaranteed`
- `isTeamOption`
- `isPlayerOption`
- `typeContractDetail`

`isWaived` presenta únicamente el valor 0 en los 1,292 registros, por lo que se considera candidato a excluirse del modelo final debido a que no aporta variabilidad dentro de esta fuente.

Los demás atributos presentan diferentes valores y serán evaluados durante el diseño final.

### Relación con equipos

`Player_Salary.csv` no contiene directamente `id_equipo`; utiliza `nameTeam`.

Se compararon los 30 nombres únicos presentes en `nameTeam` con `full_name` de `Team.csv`.

Los 30 equipos presentan coincidencia exacta y no se encontraron equipos sin correspondencia.

Por lo tanto, durante la transformación de datos será posible obtener `id_equipo` mediante la correspondencia entre `nameTeam` y `Team.full_name`.

### Relación con jugadores

`Player_Salary.csv` no contiene directamente `id_jugador`; utiliza `namePlayer`.

Se encontraron 520 nombres distintos de jugadores:

- 416 presentan coincidencia exacta con `Player.full_name`.
- 104 no presentan coincidencia exacta.
- Ninguno de los nombres coincidentes corresponde a más de un `id_jugador`.

Por lo tanto, las 416 coincidencias exactas pueden asociarse de forma no ambigua con su respectivo `id_jugador`.

Los 104 nombres restantes requieren una transformación o análisis adicional antes de establecer la relación.

Se observaron posibles diferencias de formato, como ausencia de espacios, sufijos en nombres y caracteres adicionales. Estas diferencias no se modificarán manualmente sin realizar previamente una comprobación reproducible.

### Decisión pendiente

Antes de diseñar definitivamente la tabla correspondiente a salarios, se analizarán los 104 nombres sin coincidencia para determinar cuáles pueden relacionarse de forma segura mediante transformaciones controladas.

También se analizará qué combinación de atributos identifica de forma única cada registro salarial para determinar la clave primaria adecuada.

### Normalización de nombres de jugadores

Debido a que 104 nombres distintos de `Player_Salary.csv` no presentaban una coincidencia exacta con `Player.full_name`, se realizó una segunda comparación mediante una función de normalización.

La normalización utilizada:

- Elimina espacios adicionales.
- Convierte los nombres a minúsculas.
- Elimina tildes y otros signos diacríticos.
- Elimina caracteres especiales, espacios y guiones.
- Elimina los indicadores `W` y `E` cuando aparecen al final del nombre.

Esta transformación se utiliza únicamente como mecanismo auxiliar de comparación y no modifica los valores originales almacenados en los CSV.

### Resultados

De los 104 nombres distintos inicialmente sin coincidencia:

- 32 pudieron recuperarse mediante normalización.
- 0 de las coincidencias recuperadas resultaron ambiguas.
- 72 nombres distintos permanecieron sin correspondencia.

Considerando las coincidencias exactas y las recuperadas mediante normalización, se pueden relacionar de manera reproducible 448 de los 520 nombres distintos presentes en `Player_Salary.csv`.

Los 72 nombres restantes no serán asociados arbitrariamente con un `id_jugador`. Su tratamiento deberá quedar documentado como una limitación de integración entre las fuentes.

### Evaluación de clave candidata para salarios

Se evaluaron diferentes combinaciones de atributos para determinar qué información identifica de forma única cada registro de `Player_Salary.csv`.

Resultados:

- `(namePlayer, slugSeason)`: 17 combinaciones duplicadas.
- `(namePlayer, nameTeam, slugSeason)`: 0 combinaciones duplicadas.
- `(namePlayer, nameTeam, slugSeason, typeContractDetail)`: 0 combinaciones duplicadas.

También se encontraron 16 casos en los que un jugador aparece asociado a más de un equipo durante una misma temporada. En uno de los casos, un jugador aparece asociado a tres equipos.

Por lo tanto, jugador y temporada no son suficientes para identificar un registro salarial.

La combinación mínima encontrada que identifica de forma única los registros es:

`(namePlayer, nameTeam, slugSeason)`

Esto indica que cada registro salarial representa conceptualmente la información de un jugador asociada con un equipo durante una temporada determinada.

Agregar `typeContractDetail` a la clave no es necesario, ya que la combinación anterior ya garantiza unicidad.

### Cobertura de la relación con Player.csv

Después de aplicar coincidencia exacta y normalización de nombres, los 1,292 registros salariales se clasificaron de la siguiente manera:

- 955 registros presentan coincidencia exacta.
- 69 registros adicionales pudieron relacionarse mediante normalización.
- 268 registros permanecen sin correspondencia.
- Los registros sin correspondencia representan aproximadamente el 20.74 % del archivo.

En total, 1,024 de los 1,292 registros pueden relacionarse de manera reproducible con un jugador.

### Decisión sobre la clave primaria

Aunque la combinación `(namePlayer, nameTeam, slugSeason)` identifica de forma única los registros de la fuente, no todos los valores de `namePlayer` pueden convertirse de manera confiable en un `id_jugador`.

Utilizar `(id_jugador, id_equipo, temporada)` como clave primaria impediría conservar los registros cuyo jugador no pudo relacionarse, debido a que una clave primaria no puede contener valores NULL.

Por esta razón, se propone utilizar una clave sustituta `id_salario` como clave primaria.

`id_jugador` funcionará como clave foránea hacia `JUGADOR`, pero permitirá valores NULL cuando la relación no pueda establecerse de manera confiable.

`id_equipo` funcionará como clave foránea hacia `EQUIPO` y no requerirá valores NULL, debido a que todos los equipos de la fuente pudieron relacionarse.

Se conservará además el nombre original del jugador proveniente de `Player_Salary.csv` para evitar pérdida de información en los registros que no puedan asociarse con un `id_jugador`.

### Tratamiento de atributos contractuales

Se propone conservar los atributos contractuales que presentan variabilidad en la fuente:

- estado del jugador;
- indicador de temporada final;
- pertenencia al roster;
- contrato no garantizado;
- opción del equipo;
- opción del jugador;
- tipo de contrato;
- valor salarial.

`isWaived` será excluido del modelo debido a que presenta el valor 0 en los 1,292 registros y, por lo tanto, no aporta variabilidad dentro del conjunto analizado.