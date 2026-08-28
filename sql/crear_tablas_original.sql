-- =====================================================
-- PROYECTO NBA
-- Creación de tablas - PostgreSQL
-- Base de datos: proyecto_nba
-- =====================================================

-- ============================================================
-- 1. EQUIPO
-- Tabla principal de equipos.
-- ============================================================

CREATE TABLE equipo (
    id_equipo BIGINT PRIMARY KEY,
    nombre_equipo VARCHAR(100) NOT NULL,
    abreviatura VARCHAR(10),
    apodo VARCHAR(100),
    ciudad VARCHAR(100),
    estado VARCHAR(100),
    anio_fundacion INTEGER,
    arena VARCHAR(150),
    capacidad_arena INTEGER,
    propietario VARCHAR(150),
    gerente_general VARCHAR(150),
    entrenador VARCHAR(150),
    afiliacion_dleague VARCHAR(150)
);


-- ============================================================
-- 2. JUGADOR
-- Información principal de los jugadores.
-- ============================================================

CREATE TABLE jugador (
    id_jugador BIGINT PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    nombre_completo VARCHAR(200),
    fecha_nacimiento DATE,
    pais VARCHAR(100),
    altura DECIMAL(6,2),
    peso DECIMAL(7,2),
    esta_activo BOOLEAN
);


-- ============================================================
-- 3. TEMPORADA
-- Ejemplo nombre_temporada: 2021-22
-- ============================================================

CREATE TABLE temporada (
    id_temporada BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre_temporada VARCHAR(10) NOT NULL UNIQUE
);


-- ============================================================
-- 4. ARBITRO
-- ============================================================

CREATE TABLE arbitro (
    id_arbitro BIGINT PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    numero_camiseta VARCHAR(10)
);


-- ============================================================
-- 5. NOTICIA
-- Información proveniente de News.csv.
-- ============================================================

CREATE TABLE noticia (
    id_noticia BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    titulo TEXT,
    autor VARCHAR(200),
    fecha_publicacion TIMESTAMP,
    url TEXT,
    contenido TEXT
);


-- ============================================================
-- 6. HISTORIAL_EQUIPO
-- Un equipo puede tener diferentes nombres/ciudades
-- a lo largo de su historia.
-- ============================================================

CREATE TABLE historial_equipo (
    id_historial BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    id_equipo BIGINT NOT NULL,

    ciudad VARCHAR(100),
    apodo VARCHAR(100),
    anio_fundacion INTEGER,
    anio_activo_hasta INTEGER,

    CONSTRAINT fk_historial_equipo
        FOREIGN KEY (id_equipo)
        REFERENCES equipo(id_equipo)
);


-- ============================================================
-- 7. DRAFT
-- Relaciona jugador seleccionado, equipo y datos del draft.
-- ============================================================

CREATE TABLE draft (
    id_draft BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    id_jugador BIGINT NOT NULL,
    id_equipo BIGINT,

    anio_draft INTEGER NOT NULL,
    numero_pick INTEGER,
    ronda_pick INTEGER,

    nombre_organizacion_origen VARCHAR(200),
    tipo_organizacion_origen VARCHAR(100),
    codigo_tipo_organizacion_origen VARCHAR(50),
    ubicacion_organizacion_origen VARCHAR(150),

    CONSTRAINT fk_draft_jugador
        FOREIGN KEY (id_jugador)
        REFERENCES jugador(id_jugador),

    CONSTRAINT fk_draft_equipo
        FOREIGN KEY (id_equipo)
        REFERENCES equipo(id_equipo)
);


-- ============================================================
-- 8. DRAFT_COMBINE
-- Mediciones y pruebas físicas de jugadores.
-- ============================================================

CREATE TABLE draft_combine (
    id_combine BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    id_jugador BIGINT NOT NULL,

    anio_combine INTEGER,
    posicion VARCHAR(50),

    altura DECIMAL(6,2),
    peso DECIMAL(7,2),
    alcance DECIMAL(6,2),
    salto_vertical DECIMAL(6,2),

    repeticiones_banca INTEGER,
    tiempo_agilidad DECIMAL(8,3),
    tiempo_sprint_tres_cuartos DECIMAL(8,3),

    CONSTRAINT fk_combine_jugador
        FOREIGN KEY (id_jugador)
        REFERENCES jugador(id_jugador)
);


-- ============================================================
-- 9. SALARIO_JUGADOR
-- Contrato/salario de un jugador con un equipo
-- durante una temporada.
-- ============================================================

CREATE TABLE salario_jugador (
    id_salario_jugador BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    id_jugador BIGINT,
    id_equipo BIGINT NOT NULL,
    id_temporada BIGINT NOT NULL,

    estado_jugador VARCHAR(100),

    temporada_final BOOLEAN,
    en_roster BOOLEAN,
    no_garantizado BOOLEAN,
    opcion_equipo BOOLEAN,
    opcion_jugador BOOLEAN,

    tipo_contrato VARCHAR(100),
    salario DECIMAL(18,2),

    CONSTRAINT fk_salario_jugador
        FOREIGN KEY (id_jugador)
        REFERENCES jugador(id_jugador),

    CONSTRAINT fk_salario_equipo
        FOREIGN KEY (id_equipo)
        REFERENCES equipo(id_equipo),

    CONSTRAINT fk_salario_temporada
        FOREIGN KEY (id_temporada)
        REFERENCES temporada(id_temporada)
);


-- ============================================================
-- 10. SALARIO_EQUIPO_TEMPORADA
-- Salario total de un equipo en determinada temporada.
-- ============================================================

CREATE TABLE salario_equipo_temporada (
    id_equipo BIGINT NOT NULL,
    id_temporada BIGINT NOT NULL,

    salario DECIMAL(18,2),

    PRIMARY KEY (id_equipo, id_temporada),

    CONSTRAINT fk_salario_total_equipo
        FOREIGN KEY (id_equipo)
        REFERENCES equipo(id_equipo),

    CONSTRAINT fk_salario_total_temporada
        FOREIGN KEY (id_temporada)
        REFERENCES temporada(id_temporada)
);


-- ============================================================
-- 11. PARTIDO
-- Cada partido pertenece a una temporada y contiene
-- un equipo local y un equipo visitante.
-- ============================================================

CREATE TABLE partido (
    id_partido BIGINT PRIMARY KEY,

    id_temporada BIGINT NOT NULL,

    id_equipo_local BIGINT NOT NULL,
    id_equipo_visitante BIGINT NOT NULL,

    fecha_partido DATE,
    hora_partido TIME,
    asistencia INTEGER,
    estado_partido VARCHAR(50),

    puntos_local INTEGER,
    puntos_visitante INTEGER,

    rebotes_local INTEGER,
    rebotes_visitante INTEGER,

    asistencias_local INTEGER,
    asistencias_visitante INTEGER,

    robos_local INTEGER,
    robos_visitante INTEGER,

    bloqueos_local INTEGER,
    bloqueos_visitante INTEGER,

    perdidas_local INTEGER,
    perdidas_visitante INTEGER,

    resultado_local VARCHAR(5),
    resultado_visitante VARCHAR(5),

    CONSTRAINT fk_partido_temporada
        FOREIGN KEY (id_temporada)
        REFERENCES temporada(id_temporada),

    CONSTRAINT fk_partido_equipo_local
        FOREIGN KEY (id_equipo_local)
        REFERENCES equipo(id_equipo),

    CONSTRAINT fk_partido_equipo_visitante
        FOREIGN KEY (id_equipo_visitante)
        REFERENCES equipo(id_equipo),

    CONSTRAINT chk_equipos_diferentes
        CHECK (id_equipo_local <> id_equipo_visitante)
);


-- ============================================================
-- 12. JUGADOR_INACTIVO
-- Jugadores que estuvieron inactivos en un partido.
-- ============================================================

CREATE TABLE jugador_inactivo (
    id_jugador BIGINT NOT NULL,
    id_partido BIGINT NOT NULL,
    id_equipo BIGINT NOT NULL,

    numero_camiseta VARCHAR(10),

    PRIMARY KEY (id_jugador, id_partido),

    CONSTRAINT fk_inactivo_jugador
        FOREIGN KEY (id_jugador)
        REFERENCES jugador(id_jugador),

    CONSTRAINT fk_inactivo_partido
        FOREIGN KEY (id_partido)
        REFERENCES partido(id_partido),

    CONSTRAINT fk_inactivo_equipo
        FOREIGN KEY (id_equipo)
        REFERENCES equipo(id_equipo)
);


-- ============================================================
-- 13. ARBITRO_PARTIDO
-- Relación N:M entre árbitros y partidos.
-- ============================================================

CREATE TABLE arbitro_partido (
    id_arbitro BIGINT NOT NULL,
    id_partido BIGINT NOT NULL,

    PRIMARY KEY (id_arbitro, id_partido),

    CONSTRAINT fk_arbitro_partido_arbitro
        FOREIGN KEY (id_arbitro)
        REFERENCES arbitro(id_arbitro),

    CONSTRAINT fk_arbitro_partido_partido
        FOREIGN KEY (id_partido)
        REFERENCES partido(id_partido)
);


-- ============================================================
-- 14. ESTADISTICA_EQUIPO_TEMPORADA
-- Datos que complementaremos mediante NBA API.
-- ============================================================

CREATE TABLE estadistica_equipo_temporada (
    id_equipo BIGINT NOT NULL,
    id_temporada BIGINT NOT NULL,

    partidos_jugados INTEGER,
    victorias INTEGER,
    derrotas INTEGER,

    minutos DECIMAL(10,2),

    puntos DECIMAL(10,2),
    rebotes DECIMAL(10,2),
    asistencias DECIMAL(10,2),
    robos DECIMAL(10,2),
    bloqueos DECIMAL(10,2),
    perdidas DECIMAL(10,2),

    porcentaje_tiros_campo DECIMAL(7,4),
    porcentaje_triples DECIMAL(7,4),
    porcentaje_tiros_libres DECIMAL(7,4),

    plus_minus DECIMAL(10,2),

    PRIMARY KEY (id_equipo, id_temporada),

    CONSTRAINT fk_estadistica_equipo
        FOREIGN KEY (id_equipo)
        REFERENCES equipo(id_equipo),

    CONSTRAINT fk_estadistica_temporada
        FOREIGN KEY (id_temporada)
        REFERENCES temporada(id_temporada)
);