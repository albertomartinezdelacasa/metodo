-- ========================================
-- MÉTODO COMEDIA - DATABASE SCHEMA
-- ========================================
-- Ejecutar en Supabase SQL Editor
-- Base de datos PostgreSQL para gestión de chistes y análisis

-- ========================================
-- TABLA: chistes
-- ========================================
CREATE TABLE IF NOT EXISTS chistes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    titulo VARCHAR(255),
    contenido TEXT NOT NULL,
    estado VARCHAR(50) DEFAULT 'borrador' CHECK (estado IN ('borrador', 'revisado', 'probado', 'pulido', 'archivado')),

    -- Calificación y uso
    calificacion INTEGER CHECK (calificacion >= 1 AND calificacion <= 10),
    veces_usado INTEGER DEFAULT 0,

    -- Campos básicos de análisis (pueden llenarse manualmente o con IA)
    concepto TEXT,
    premisa TEXT,
    remate TEXT,

    -- Timestamps
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    fecha_modificacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ultima_presentacion TIMESTAMP WITH TIME ZONE,

    -- Reacción de audiencia (JSON)
    reaccion_audiencia JSONB DEFAULT '{"risas": 0, "silencio": 0, "aplausos": 0, "groans": 0}'::jsonb,

    -- Notas personales
    notas TEXT,

    -- Soft delete
    eliminado BOOLEAN DEFAULT FALSE
);

-- Índices para chistes
CREATE INDEX idx_chistes_estado ON chistes(estado) WHERE NOT eliminado;
CREATE INDEX idx_chistes_fecha ON chistes(fecha_creacion DESC);
CREATE INDEX idx_chistes_calificacion ON chistes(calificacion DESC) WHERE calificacion IS NOT NULL;
CREATE INDEX idx_chistes_veces_usado ON chistes(veces_usado DESC);

-- ========================================
-- TABLA: analisis_ia
-- ========================================
CREATE TABLE IF NOT EXISTS analisis_ia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chiste_id UUID REFERENCES chistes(id) ON DELETE CASCADE,
    fecha_analisis TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Estructura del chiste (JSON)
    estructura JSONB,

    -- Técnicas identificadas (array)
    tecnicas TEXT[],

    -- Análisis detallado
    puntos_fuertes TEXT[],
    puntos_debiles TEXT[],
    sugerencias TEXT[],

    -- Análisis avanzado de conceptos (opcional, se llena con análisis detallado)
    tipo_concepto VARCHAR(50) CHECK (tipo_concepto IN ('simple', 'compuesto', 'concreto', 'abstracto')),
    explicacion_tipo_concepto TEXT,
    mapa_conceptos JSONB, -- Estructura: {"concepto_principal": "...", "asociaciones": [...], "explicacion": "..."}

    -- Análisis avanzado de rupturas (opcional, se llena con análisis detallado)
    tipo_ruptura VARCHAR(100),
    subtipo_ruptura VARCHAR(100),
    explicacion_ruptura TEXT,

    -- Scoring (0.00 - 10.00)
    puntuacion_estructura NUMERIC(4,2) CHECK (puntuacion_estructura >= 0 AND puntuacion_estructura <= 10),
    puntuacion_originalidad NUMERIC(4,2) CHECK (puntuacion_originalidad >= 0 AND puntuacion_originalidad <= 10),
    puntuacion_timing NUMERIC(4,2) CHECK (puntuacion_timing >= 0 AND puntuacion_timing <= 10),
    puntuacion_general NUMERIC(4,2) CHECK (puntuacion_general >= 0 AND puntuacion_general <= 10),

    -- Metadata del modelo
    modelo_ia VARCHAR(50) DEFAULT 'gemini-1.5-flash',
    prompt_version VARCHAR(20) DEFAULT '1.0'
);

-- Índices para análisis
CREATE INDEX idx_analisis_chiste ON analisis_ia(chiste_id);
CREATE INDEX idx_analisis_fecha ON analisis_ia(fecha_analisis DESC);
CREATE INDEX idx_analisis_puntuacion ON analisis_ia(puntuacion_general DESC);

-- ========================================
-- TABLA: tags
-- ========================================
CREATE TABLE IF NOT EXISTS tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR(100) UNIQUE NOT NULL,
    categoria VARCHAR(50) CHECK (categoria IN ('tema', 'tecnica', 'audiencia', 'tono', 'evento')),
    color VARCHAR(20) DEFAULT '#6B7280',
    descripcion TEXT,
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índice para tags
CREATE INDEX idx_tags_categoria ON tags(categoria);
CREATE INDEX idx_tags_nombre ON tags(nombre);

-- ========================================
-- TABLA: chistes_tags (relación muchos a muchos)
-- ========================================
CREATE TABLE IF NOT EXISTS chistes_tags (
    chiste_id UUID REFERENCES chistes(id) ON DELETE CASCADE,
    tag_id UUID REFERENCES tags(id) ON DELETE CASCADE,
    asignado_en TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (chiste_id, tag_id)
);

-- ========================================
-- TABLA: versiones_chiste (historial)
-- ========================================
CREATE TABLE IF NOT EXISTS versiones_chiste (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chiste_id UUID REFERENCES chistes(id) ON DELETE CASCADE,
    version_numero INTEGER NOT NULL,
    contenido_anterior TEXT NOT NULL,
    titulo_anterior VARCHAR(255),
    fecha_version TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    motivo_cambio TEXT,
    UNIQUE (chiste_id, version_numero)
);

-- Índice para versiones
CREATE INDEX idx_versiones_chiste ON versiones_chiste(chiste_id, version_numero DESC);

-- ========================================
-- TABLA: presentaciones (shows/eventos)
-- ========================================
CREATE TABLE IF NOT EXISTS presentaciones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fecha TIMESTAMP WITH TIME ZONE NOT NULL,
    lugar VARCHAR(255),
    tipo_evento VARCHAR(100) CHECK (tipo_evento IN ('show_abierto', 'monologo', 'privado', 'grabacion', 'ensayo')),
    audiencia_tamano INTEGER CHECK (audiencia_tamano >= 0),
    duracion_minutos INTEGER,
    notas TEXT,
    exito_general INTEGER CHECK (exito_general >= 1 AND exito_general <= 10),
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índice para presentaciones
CREATE INDEX idx_presentaciones_fecha ON presentaciones(fecha DESC);
CREATE INDEX idx_presentaciones_tipo ON presentaciones(tipo_evento);

-- ========================================
-- TABLA: chistes_presentaciones (relación)
-- ========================================
CREATE TABLE IF NOT EXISTS chistes_presentaciones (
    chiste_id UUID REFERENCES chistes(id) ON DELETE CASCADE,
    presentacion_id UUID REFERENCES presentaciones(id) ON DELETE CASCADE,
    orden_presentacion INTEGER,
    reaccion VARCHAR(50) CHECK (reaccion IN ('genial', 'buena', 'regular', 'mala', 'silencio')),
    duracion_risas INTEGER, -- segundos
    notas TEXT,
    PRIMARY KEY (chiste_id, presentacion_id)
);

-- ========================================
-- TABLA: bitacora (diario de práctica/reflexiones)
-- ========================================
CREATE TABLE IF NOT EXISTS bitacora (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fecha TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    tipo VARCHAR(50) CHECK (tipo IN ('practica', 'reflexion', 'idea', 'observacion', 'nota_general')) DEFAULT 'nota_general',
    titulo VARCHAR(255),
    contenido TEXT NOT NULL,
    estado_animo VARCHAR(50), -- opcional: cómo te sentías al escribir
    tags TEXT[], -- etiquetas libres
    chiste_relacionado_id UUID REFERENCES chistes(id) ON DELETE SET NULL, -- opcional: vincular a un chiste
    presentacion_relacionada_id UUID REFERENCES presentaciones(id) ON DELETE SET NULL, -- opcional: vincular a una presentación
    eliminado BOOLEAN DEFAULT FALSE,
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    modificado_en TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para bitácora
CREATE INDEX idx_bitacora_fecha ON bitacora(fecha DESC) WHERE NOT eliminado;
CREATE INDEX idx_bitacora_tipo ON bitacora(tipo) WHERE NOT eliminado;
CREATE INDEX idx_bitacora_chiste ON bitacora(chiste_relacionado_id) WHERE chiste_relacionado_id IS NOT NULL;

-- ========================================
-- FUNCIONES Y TRIGGERS
-- ========================================

-- Trigger para actualizar fecha_modificacion automáticamente
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_modificacion = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_chistes_modtime
    BEFORE UPDATE ON chistes
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

-- Trigger para crear versión antes de actualizar contenido
CREATE OR REPLACE FUNCTION save_joke_version()
RETURNS TRIGGER AS $$
DECLARE
    next_version INTEGER;
BEGIN
    -- Solo si el contenido cambió
    IF OLD.contenido IS DISTINCT FROM NEW.contenido THEN
        -- Obtener siguiente número de versión
        SELECT COALESCE(MAX(version_numero), 0) + 1
        INTO next_version
        FROM versiones_chiste
        WHERE chiste_id = OLD.id;

        -- Guardar versión anterior
        INSERT INTO versiones_chiste (chiste_id, version_numero, contenido_anterior, titulo_anterior)
        VALUES (OLD.id, next_version, OLD.contenido, OLD.titulo);
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER save_version_before_update
    BEFORE UPDATE ON chistes
    FOR EACH ROW
    EXECUTE FUNCTION save_joke_version();

-- Trigger para actualizar modificado_en en bitácora
CREATE TRIGGER update_bitacora_modtime
    BEFORE UPDATE ON bitacora
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

-- ========================================
-- VISTAS ÚTILES
-- ========================================

-- Vista de chistes con su último análisis
CREATE OR REPLACE VIEW chistes_con_analisis AS
SELECT
    c.*,
    a.puntuacion_general as ultimo_score,
    a.fecha_analisis as fecha_ultimo_analisis,
    a.tecnicas as tecnicas_identificadas
FROM chistes c
LEFT JOIN LATERAL (
    SELECT *
    FROM analisis_ia
    WHERE chiste_id = c.id
    ORDER BY fecha_analisis DESC
    LIMIT 1
) a ON true
WHERE NOT c.eliminado;

-- Vista de estadísticas de chistes
CREATE OR REPLACE VIEW estadisticas_chistes AS
SELECT
    estado,
    COUNT(*) as total,
    AVG(calificacion) as calificacion_promedio,
    AVG(veces_usado) as veces_usado_promedio,
    MAX(veces_usado) as max_veces_usado
FROM chistes
WHERE NOT eliminado
GROUP BY estado;

-- ========================================
-- DATOS INICIALES: Tags comunes
-- ========================================
INSERT INTO tags (nombre, categoria, color) VALUES
    -- Temas
    ('familia', 'tema', '#EF4444'),
    ('tecnologia', 'tema', '#3B82F6'),
    ('viajes', 'tema', '#10B981'),
    ('relaciones', 'tema', '#EC4899'),
    ('trabajo', 'tema', '#F59E0B'),
    ('comida', 'tema', '#8B5CF6'),

    -- Técnicas
    ('exageracion', 'tecnica', '#6366F1'),
    ('wordplay', 'tecnica', '#14B8A6'),
    ('observacional', 'tecnica', '#F97316'),
    ('autoburla', 'tecnica', '#84CC16'),
    ('sarcasmo', 'tecnica', '#A855F7'),
    ('absurdo', 'tecnica', '#EC4899'),

    -- Audiencia
    ('general', 'audiencia', '#6B7280'),
    ('adultos', 'audiencia', '#DC2626'),
    ('corporativo', 'audiencia', '#2563EB'),

    -- Tono
    ('ligero', 'tono', '#34D399'),
    ('oscuro', 'tono', '#64748B'),
    ('sarcástico', 'tono', '#F59E0B')
ON CONFLICT (nombre) DO NOTHING;

-- ========================================
-- POLÍTICAS RLS (Row Level Security)
-- ========================================
-- Descomentar si usas autenticación de usuarios

-- ALTER TABLE chistes ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE analisis_ia ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE tags ENABLE ROW LEVEL SECURITY;

-- CREATE POLICY "Enable read access for all users" ON chistes
--     FOR SELECT USING (true);

-- CREATE POLICY "Enable insert for authenticated users only" ON chistes
--     FOR INSERT WITH CHECK (auth.role() = 'authenticated');

-- ========================================
-- FIN DEL SCHEMA
-- ========================================

-- Verificar creación de tablas
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_name IN ('chistes', 'analisis_ia', 'tags', 'chistes_tags', 'versiones_chiste', 'presentaciones', 'chistes_presentaciones', 'bitacora')
ORDER BY table_name;
