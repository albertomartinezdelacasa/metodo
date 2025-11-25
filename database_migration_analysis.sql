-- ========================================
-- MIGRACIÓN: Sistema de Análisis Progresivo
-- ========================================
-- Fecha: 2025-11-25
-- Descripción: Añade tabla para análisis de chistes de otros comediantes,
--              categorías dinámicas y campos faltantes en tabla chistes

-- ========================================
-- 1. NUEVA TABLA: analisis_chistes
-- ========================================
-- Para estudiar y analizar chistes de otros comediantes

CREATE TABLE IF NOT EXISTS analisis_chistes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Identificación
    titulo_referencia VARCHAR(255),
    comediante VARCHAR(255),

    -- Estructura del chiste (3 partes separadas)
    premisa TEXT,
    elemento_mecanico VARCHAR(100), -- Elemento mecánico de la premisa
    ruptura TEXT,
    remate TEXT,

    -- Perspectiva
    perspectiva_categoria VARCHAR(100),
    perspectiva_justificacion TEXT,
    actitud VARCHAR(100),
    concepto TEXT,
    concepto_categoria VARCHAR(100),

    -- Desarrollo de la idea (Mind Map)
    desarrollo_idea TEXT,

    -- Formulación
    formulacion_categoria VARCHAR(100),
    formulacion_justificacion TEXT,

    -- Metadatos
    notas TEXT,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    fecha_modificacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    eliminado BOOLEAN DEFAULT FALSE
);

-- Índices para búsquedas rápidas
CREATE INDEX idx_analisis_chistes_comediante ON analisis_chistes(comediante) WHERE NOT eliminado;
CREATE INDEX idx_analisis_chistes_concepto ON analisis_chistes(concepto_categoria) WHERE NOT eliminado;
CREATE INDEX idx_analisis_chistes_fecha ON analisis_chistes(fecha_creacion DESC) WHERE NOT eliminado;

-- Trigger para actualizar fecha_modificacion
CREATE OR REPLACE FUNCTION update_analisis_chistes_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_modificacion = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_analisis_chistes_timestamp
    BEFORE UPDATE ON analisis_chistes
    FOR EACH ROW
    EXECUTE FUNCTION update_analisis_chistes_timestamp();

-- ========================================
-- 2. NUEVA TABLA: categorias_dinamicas
-- ========================================
-- Para almacenar categorías creadas por el usuario en dropdowns

CREATE TABLE IF NOT EXISTS categorias_dinamicas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tipo VARCHAR(50) NOT NULL, -- 'perspectiva', 'actitud', 'concepto', 'formulacion'
    valor VARCHAR(255) NOT NULL,
    usuario_creado BOOLEAN DEFAULT TRUE, -- true = creado por usuario, false = predefinido
    orden INTEGER DEFAULT 0, -- Para ordenar en dropdown
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    CONSTRAINT unique_tipo_valor UNIQUE (tipo, valor)
);

-- Índice para consultas por tipo
CREATE INDEX idx_categorias_tipo ON categorias_dinamicas(tipo, orden);

-- Insertar categorías iniciales (vacío, usuario las crea según necesite)
-- Dejamos la tabla vacía para que el usuario empiece desde cero

-- ========================================
-- 3. ACTUALIZAR TABLA: chistes
-- ========================================
-- Añadir campos faltantes para análisis completo

-- Verificar si las columnas ya existen antes de añadirlas
DO $$
BEGIN
    -- Ruptura (si no existe)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                   WHERE table_name='chistes' AND column_name='ruptura') THEN
        ALTER TABLE chistes ADD COLUMN ruptura TEXT;
    END IF;

    -- Perspectiva
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                   WHERE table_name='chistes' AND column_name='perspectiva_categoria') THEN
        ALTER TABLE chistes ADD COLUMN perspectiva_categoria VARCHAR(100);
    END IF;

    IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                   WHERE table_name='chistes' AND column_name='perspectiva_justificacion') THEN
        ALTER TABLE chistes ADD COLUMN perspectiva_justificacion TEXT;
    END IF;

    -- Actitud
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                   WHERE table_name='chistes' AND column_name='actitud') THEN
        ALTER TABLE chistes ADD COLUMN actitud VARCHAR(100);
    END IF;

    -- Categoría de concepto (concepto ya existe)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                   WHERE table_name='chistes' AND column_name='concepto_categoria') THEN
        ALTER TABLE chistes ADD COLUMN concepto_categoria VARCHAR(100);
    END IF;

    -- Desarrollo de la idea
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                   WHERE table_name='chistes' AND column_name='desarrollo_idea') THEN
        ALTER TABLE chistes ADD COLUMN desarrollo_idea TEXT;
    END IF;

    -- Formulación
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                   WHERE table_name='chistes' AND column_name='formulacion_categoria') THEN
        ALTER TABLE chistes ADD COLUMN formulacion_categoria VARCHAR(100);
    END IF;

    IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                   WHERE table_name='chistes' AND column_name='formulacion_justificacion') THEN
        ALTER TABLE chistes ADD COLUMN formulacion_justificacion TEXT;
    END IF;

    -- Elemento Mecánico
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                   WHERE table_name='chistes' AND column_name='elemento_mecanico') THEN
        ALTER TABLE chistes ADD COLUMN elemento_mecanico VARCHAR(100);
    END IF;
END $$;

-- ========================================
-- 4. ÍNDICES ADICIONALES EN chistes
-- ========================================
-- Para mejorar búsquedas y comparaciones

CREATE INDEX IF NOT EXISTS idx_chistes_concepto_categoria
    ON chistes(concepto_categoria) WHERE NOT eliminado;

CREATE INDEX IF NOT EXISTS idx_chistes_perspectiva
    ON chistes(perspectiva_categoria) WHERE NOT eliminado;

CREATE INDEX IF NOT EXISTS idx_chistes_formulacion
    ON chistes(formulacion_categoria) WHERE NOT eliminado;

-- ========================================
-- 5. VISTAS ÚTILES
-- ========================================

-- Vista: Chistes con análisis completo
CREATE OR REPLACE VIEW v_chistes_completos AS
SELECT
    id,
    titulo,
    contenido,
    concepto,
    premisa,
    ruptura,
    remate,
    perspectiva_categoria,
    actitud,
    concepto_categoria,
    formulacion_categoria,
    estado,
    calificacion,
    veces_usado,
    fecha_creacion,
    fecha_modificacion
FROM chistes
WHERE NOT eliminado
  AND premisa IS NOT NULL
  AND ruptura IS NOT NULL
  AND remate IS NOT NULL;

-- Vista: Análisis de chistes completos
CREATE OR REPLACE VIEW v_analisis_completos AS
SELECT
    id,
    titulo_referencia,
    comediante,
    concepto,
    concepto_categoria,
    perspectiva_categoria,
    actitud,
    formulacion_categoria,
    fecha_creacion
FROM analisis_chistes
WHERE NOT eliminado
  AND premisa IS NOT NULL
  AND ruptura IS NOT NULL
  AND remate IS NOT NULL;

-- ========================================
-- 6. FUNCIÓN: Comparar chiste con análisis
-- ========================================
-- Encuentra análisis similares basados en concepto, perspectiva, formulación

CREATE OR REPLACE FUNCTION comparar_chiste_con_analisis(
    p_chiste_id UUID
) RETURNS TABLE (
    analisis_id UUID,
    titulo_referencia VARCHAR,
    comediante VARCHAR,
    similitud_concepto BOOLEAN,
    similitud_perspectiva BOOLEAN,
    similitud_formulacion BOOLEAN,
    score INTEGER
) AS $$
BEGIN
    RETURN QUERY
    WITH chiste_actual AS (
        SELECT
            concepto_categoria,
            perspectiva_categoria,
            formulacion_categoria
        FROM chistes
        WHERE id = p_chiste_id
    )
    SELECT
        a.id,
        a.titulo_referencia,
        a.comediante,
        (a.concepto_categoria = c.concepto_categoria) AS similitud_concepto,
        (a.perspectiva_categoria = c.perspectiva_categoria) AS similitud_perspectiva,
        (a.formulacion_categoria = c.formulacion_categoria) AS similitud_formulacion,
        (
            (CASE WHEN a.concepto_categoria = c.concepto_categoria THEN 3 ELSE 0 END) +
            (CASE WHEN a.perspectiva_categoria = c.perspectiva_categoria THEN 2 ELSE 0 END) +
            (CASE WHEN a.formulacion_categoria = c.formulacion_categoria THEN 1 ELSE 0 END)
        ) AS score
    FROM analisis_chistes a
    CROSS JOIN chiste_actual c
    WHERE NOT a.eliminado
      AND (
          a.concepto_categoria = c.concepto_categoria OR
          a.perspectiva_categoria = c.perspectiva_categoria OR
          a.formulacion_categoria = c.formulacion_categoria
      )
    ORDER BY score DESC, a.fecha_creacion DESC
    LIMIT 10;
END;
$$ LANGUAGE plpgsql;

-- ========================================
-- 7. COMENTARIOS EN TABLAS
-- ========================================

COMMENT ON TABLE analisis_chistes IS 'Análisis estructurado de chistes de otros comediantes para estudio';
COMMENT ON TABLE categorias_dinamicas IS 'Categorías creadas dinámicamente por el usuario para dropdowns';

COMMENT ON COLUMN analisis_chistes.premisa IS 'Líneas de la premisa del chiste (setup)';
COMMENT ON COLUMN analisis_chistes.ruptura IS 'Líneas donde ocurre la ruptura de expectativa';
COMMENT ON COLUMN analisis_chistes.remate IS 'Líneas del remate final (punchline)';
COMMENT ON COLUMN analisis_chistes.desarrollo_idea IS 'Mind map o descripción del proceso creativo';

-- ========================================
-- MIGRACIÓN COMPLETADA
-- ========================================
-- Ejecutar este script en Supabase SQL Editor
-- Verificar que todas las tablas se crearon correctamente con:
-- SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
