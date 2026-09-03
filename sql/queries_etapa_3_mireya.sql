-- Etapa #3 preguntas 7,8,9
-- ¿Qué equipos dependen menos de jugar como locales?
SELECT e.nombre_equipo, 

-- Victorias de cada equipo como locales y convertirlos a 1
SUM( CASE WHEN p.id_equipo_local = e.id_equipo AND p.resultado_local = 'W' THEN 1 
ELSE 0 END ) AS victorias_local, 
--Victorias de cada equipo como visitantes y convertirlos a 1
SUM( CASE WHEN p.id_equipo_visitante = e.id_equipo AND p.resultado_visitante = 'W' 
THEN 1 ELSE 0 END) AS victorias_visitante, 
-- Diferencia entre victorias locales y visitantes con valor absoluto
ABS( SUM( CASE WHEN p.id_equipo_local = e.id_equipo AND p.resultado_local = 'W' THEN 1
ELSE 0 END ) - SUM(CASE WHEN p.id_equipo_visitante = e.id_equipo AND p.resultado_visitante = 'W'
THEN 1 ELSE 0 END )) AS diferencia

FROM equipo e
JOIN partido p ON e.id_equipo = p.id_equipo_local OR e.id_equipo = p.id_equipo_visitante
JOIN temporada t ON p.id_temporada = t.id_temporada

WHERE t.nombre_temporada = '2020-21'
GROUP BY e.id_equipo, e.nombre_equipo
ORDER BY diferencia ASC
--Mejores 10
LIMIT 10;

-- ¿Qué equipos presentan menor volatilidad?
SELECT e.nombre_equipo, ROUND(AVG(x.diferencia), 2) AS diferencial_promedio, MAX(x.diferencia)
AS mejor_diferencial, MIN(x.diferencia) AS peor_diferencial, MAX(x.diferencia) - MIN(x.diferencia)
AS variacion

--Perspectiva de locales
FROM (SELECT id_equipo_local AS id_equipo, puntos_local - puntos_visitante AS diferencia 
FROM partido p JOIN temporada t ON p.id_temporada = t.id_temporada WHERE t.nombre_temporada = '2020-21'
--perspectiva visitantes
UNION ALL SELECT id_equipo_visitante AS id_equipo, puntos_visitante - puntos_local AS diferencia
FROM partido p JOIN temporada t ON p.id_temporada = t.id_temporada WHERE t.nombre_temporada = '2020-21'
) x

JOIN equipo e ON x.id_equipo = e.id_equipo GROUP BY e.id_equipo, e.nombre_equipo
-- Eliminamos los equipos consistentemente malos
HAVING AVG(x.diferencia) > 0 ORDER BY variacion ASC

LIMIT 10;

-- ¿Qué equipos consiguieron un rendimiento superior al promedio utilizando una inversión 
-- salarial inferior al promedio, y cuáles obtuvieron más victorias 
-- por cada millón de dólares destinado a salarios?

SELECT e.nombre_equipo, est.victorias, est.salario, est.plus_minus,
-- Los numeros en salarios se convierten a millones y se dividen con las victorios por millon
    ROUND( est.victorias / (est.salario / 1000000.0), 2) AS victorias_por_millon

FROM estadistica_equipo_temporada est

JOIN equipo e ON est.id_equipo = e.id_equipo

JOIN temporada t ON est.id_temporada = t.id_temporada

WHERE t.nombre_temporada = '2020-21'

-- rendimiento superior al promedio en temporada 2020-21 
-- y quedarse con lo que estén superiores al prom
AND est.victorias > ( SELECT AVG(est2.victorias) FROM estadistica_equipo_temporada est2
JOIN temporada t2 ON est2.id_temporada = t2.id_temporada
WHERE t2.nombre_temporada = '2020-21')

-- gastar menos que el promedio y trabajar con los que esten por debajo del AVG
AND est.salario < ( SELECT AVG(est3.salario) FROM estadistica_equipo_temporada est3
JOIN temporada t3 ON est3.id_temporada = t3.id_temporada WHERE t3.nombre_temporada = '2020-21')

-- Primero equipos serán los que tienen mayor valor por millón 
ORDER BY victorias_por_millon DESC;