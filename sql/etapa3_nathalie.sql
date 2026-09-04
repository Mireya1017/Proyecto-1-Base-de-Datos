-- PROYECTO NBA - ETAPA 3
-- Nathalie - Rendimiento deportivo
-- Objetivo: seleccionar candidatos de inversión para 2021-22


-- QUERY 1
-- ¿Qué equipos fueron los más consistentes en cantidad de
-- victorias durante las temporadas anteriores a 2021-2022?
--
-- Se analizan las cinco temporadas anteriores.

WITH victorias_por_temporada AS (
    SELECT
        t.nombre_temporada,
        e.id_equipo,
        e.nombre_equipo,
        COUNT(*) AS victorias
    FROM partido p
    JOIN temporada t
        ON p.id_temporada = t.id_temporada
    JOIN equipo e
        ON (
            (p.id_equipo_local = e.id_equipo
             AND p.puntos_local > p.puntos_visitante)
            OR
            (p.id_equipo_visitante = e.id_equipo
             AND p.puntos_visitante > p.puntos_local)
        )
    WHERE t.nombre_temporada IN (
        '2016-17',
        '2017-18',
        '2018-19',
        '2019-20',
        '2020-21'
    )
    GROUP BY
        t.nombre_temporada,
        e.id_equipo,
        e.nombre_equipo
)

SELECT
    nombre_equipo,
    ROUND(AVG(victorias), 2) AS promedio_victorias,
    MIN(victorias) AS minimo_victorias,
    MAX(victorias) AS maximo_victorias,
    MAX(victorias) - MIN(victorias) AS rango_victorias,
    COUNT(*) AS temporadas_analizadas
FROM victorias_por_temporada
GROUP BY
    id_equipo,
    nombre_equipo
HAVING COUNT(*) = 5
ORDER BY
    promedio_victorias DESC,
    rango_victorias ASC;


-- QUERY 2
-- ¿Qué equipos mostraron el mayor crecimiento deportivo
-- antes de la temporada 2021-2022?
--
-- Se compara el porcentaje de victorias entre 2019-20
-- y 2020-21 para controlar la distinta cantidad de partidos.

WITH rendimiento AS (
    SELECT
        e.id_equipo,
        e.nombre_equipo,
        t.nombre_temporada,
        COUNT(*) AS partidos_jugados,

        SUM(
            CASE
                WHEN p.id_equipo_local = e.id_equipo
                     AND p.puntos_local > p.puntos_visitante
                    THEN 1

                WHEN p.id_equipo_visitante = e.id_equipo
                     AND p.puntos_visitante > p.puntos_local
                    THEN 1

                ELSE 0
            END
        ) AS victorias

    FROM partido p
    JOIN temporada t
        ON p.id_temporada = t.id_temporada
    JOIN equipo e
        ON e.id_equipo = p.id_equipo_local
        OR e.id_equipo = p.id_equipo_visitante

    WHERE t.nombre_temporada IN (
        '2019-20',
        '2020-21'
    )

    GROUP BY
        e.id_equipo,
        e.nombre_equipo,
        t.nombre_temporada
),

comparacion AS (
    SELECT
        r19.id_equipo,
        r19.nombre_equipo,

        r19.partidos_jugados AS partidos_2019_20,
        r19.victorias AS victorias_2019_20,

        ROUND(
            r19.victorias * 100.0 / r19.partidos_jugados,
            2
        ) AS porcentaje_victorias_2019_20,

        r20.partidos_jugados AS partidos_2020_21,
        r20.victorias AS victorias_2020_21,

        ROUND(
            r20.victorias * 100.0 / r20.partidos_jugados,
            2
        ) AS porcentaje_victorias_2020_21

    FROM rendimiento r19
    JOIN rendimiento r20
        ON r19.id_equipo = r20.id_equipo

    WHERE r19.nombre_temporada = '2019-20'
      AND r20.nombre_temporada = '2020-21'
)

SELECT
    nombre_equipo,
    partidos_2019_20,
    victorias_2019_20,
    porcentaje_victorias_2019_20,
    partidos_2020_21,
    victorias_2020_21,
    porcentaje_victorias_2020_21,

    ROUND(
        porcentaje_victorias_2020_21
        - porcentaje_victorias_2019_20,
        2
    ) AS crecimiento_porcentual

FROM comparacion
ORDER BY crecimiento_porcentual DESC;


-- QUERY 3
-- ¿Qué equipos obtuvieron el mejor diferencial promedio
-- de puntos?
--
-- Se analiza la temporada inmediatamente anterior a la
-- decisión de inversión: 2020-21.

SELECT
    e.nombre_equipo,
    ROUND(AVG(datos.diferencial), 2) AS diferencial_promedio,
    COUNT(*) AS partidos_analizados

FROM (
    -- Equipo jugando como local
    SELECT
        p.id_equipo_local AS id_equipo,
        p.puntos_local - p.puntos_visitante AS diferencial
    FROM partido p
    JOIN temporada t
        ON p.id_temporada = t.id_temporada
    WHERE t.nombre_temporada = '2020-21'
      AND p.puntos_local IS NOT NULL
      AND p.puntos_visitante IS NOT NULL

    UNION ALL

    -- Equipo jugando como visitante
    SELECT
        p.id_equipo_visitante AS id_equipo,
        p.puntos_visitante - p.puntos_local AS diferencial
    FROM partido p
    JOIN temporada t
        ON p.id_temporada = t.id_temporada
    WHERE t.nombre_temporada = '2020-21'
      AND p.puntos_local IS NOT NULL
      AND p.puntos_visitante IS NOT NULL

) AS datos

JOIN equipo e
    ON datos.id_equipo = e.id_equipo

GROUP BY
    e.id_equipo,
    e.nombre_equipo

ORDER BY diferencial_promedio DESC;


