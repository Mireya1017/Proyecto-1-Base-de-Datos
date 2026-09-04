-- PROYECTO NBA - ETAPA 2
-- Integrante: Nathalie
-- Queries asignados: 1 al 4

-- QUERY 1
-- ¿Quién es el jugador activo más alto? ¿Y el más bajo?

SELECT
    nombre_completo,
    altura,
    CASE
        WHEN altura = (
            SELECT MAX(altura)
            FROM jugador
            WHERE esta_activo = TRUE
              AND altura IS NOT NULL
        ) THEN 'Jugador activo más alto'

        WHEN altura = (
            SELECT MIN(altura)
            FROM jugador
            WHERE esta_activo = TRUE
              AND altura IS NOT NULL
        ) THEN 'Jugador activo más bajo'
    END AS categoria
FROM jugador
WHERE esta_activo = TRUE
  AND altura IS NOT NULL
  AND altura IN (
      (
          SELECT MAX(altura)
          FROM jugador
          WHERE esta_activo = TRUE
            AND altura IS NOT NULL
      ),
      (
          SELECT MIN(altura)
          FROM jugador
          WHERE esta_activo = TRUE
            AND altura IS NOT NULL
      )
  )
ORDER BY altura DESC;


-- QUERY 2
-- ¿Cuál fue el promedio de puntos anotados y recibidos
-- por cada equipo en cada temporada?

SELECT
    t.nombre_temporada,
    e.nombre_equipo,
    ROUND(AVG(datos.puntos_anotados), 2)
        AS promedio_puntos_anotados,
    ROUND(AVG(datos.puntos_recibidos), 2)
        AS promedio_puntos_recibidos
FROM (
    -- Equipo jugando como local
    SELECT
        id_temporada,
        id_equipo_local AS id_equipo,
        puntos_local AS puntos_anotados,
        puntos_visitante AS puntos_recibidos
    FROM partido
    WHERE puntos_local IS NOT NULL
      AND puntos_visitante IS NOT NULL

    UNION ALL

    -- Equipo jugando como visitante
    SELECT
        id_temporada,
        id_equipo_visitante AS id_equipo,
        puntos_visitante AS puntos_anotados,
        puntos_local AS puntos_recibidos
    FROM partido
    WHERE puntos_local IS NOT NULL
      AND puntos_visitante IS NOT NULL
) AS datos
JOIN equipo e
    ON datos.id_equipo = e.id_equipo
JOIN temporada t
    ON datos.id_temporada = t.id_temporada
GROUP BY
    t.id_temporada,
    t.nombre_temporada,
    e.id_equipo,
    e.nombre_equipo
ORDER BY
    t.nombre_temporada,
    promedio_puntos_anotados DESC;



-- QUERY 3
-- Top 5 de árbitros en cuyos partidos el equipo
-- visitante perdió.

SELECT
    a.id_arbitro,
    CONCAT(a.nombre, ' ', a.apellido) AS arbitro,
    COUNT(*) AS derrotas_equipo_visitante
FROM arbitro a
JOIN arbitro_partido ap
    ON a.id_arbitro = ap.id_arbitro
JOIN partido p
    ON ap.id_partido = p.id_partido
WHERE p.puntos_visitante < p.puntos_local
GROUP BY
    a.id_arbitro,
    a.nombre,
    a.apellido
ORDER BY
    derrotas_equipo_visitante DESC
LIMIT 5;



-- QUERY 4
-- ¿Qué equipos manejan los salarios más altos en la última
-- temporada disponible y cómo se comparan con los equipos
-- que poseen a los jugadores de mayor salario individual?
--
-- Nota metodológica:
-- Para este análisis, "jugador más valioso" se interpreta
-- como jugador con mayor valor económico medido mediante
-- salario, no como mejor rendimiento deportivo.

WITH salario_total_equipo AS (
    SELECT
        sj.id_equipo,
        SUM(sj.salario) AS salario_total
    FROM salario_jugador sj
    WHERE sj.id_temporada = 5
    GROUP BY sj.id_equipo
),

jugador_mejor_pagado AS (
    SELECT DISTINCT ON (sj.id_equipo)
        sj.id_equipo,
        j.nombre_completo AS jugador_mayor_salario,
        sj.salario AS mayor_salario_individual
    FROM salario_jugador sj
    JOIN jugador j
        ON sj.id_jugador = j.id_jugador
    WHERE sj.id_temporada = 5
    ORDER BY
        sj.id_equipo,
        sj.salario DESC
)

SELECT
    e.nombre_equipo,
    ste.salario_total,
    jmp.jugador_mayor_salario,
    jmp.mayor_salario_individual
FROM salario_total_equipo ste
JOIN equipo e
    ON ste.id_equipo = e.id_equipo
LEFT JOIN jugador_mejor_pagado jmp
    ON ste.id_equipo = jmp.id_equipo
ORDER BY
    ste.salario_total DESC;
