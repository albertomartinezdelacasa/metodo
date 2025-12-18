-- ========================================
-- MÉTODO COMEDIA - SETUP COMPLETO
-- ========================================
-- Ejecutar TODO este archivo en Supabase SQL Editor
-- Proyecto nuevo: crea todas las tablas necesarias

-- ========================================
-- 1. TABLA: chistes (tus propios chistes)
-- ========================================
CREATE TABLE IF NOT EXISTS chistes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    titulo VARCHAR(255),
    contenido TEXT NOT NULL,
    estado VARCHAR(50) DEFAULT 'borrador' CHECK (estado IN ('borrador', 'revisado', 'probado', 'pulido', 'archivado')),
    calificacion INTEGER CHECK (calificacion >= 1 AND calificacion <= 10),
    veces_usado INTEGER DEFAULT 0,
    concepto TEXT,
    premisa TEXT,
    ruptura TEXT,
    remate TEXT,
    elemento_mecanico VARCHAR(100),
    perspectiva_categoria VARCHAR(100),
    perspectiva_justificacion TEXT,
    actitud VARCHAR(100),
    concepto_categoria VARCHAR(100),
    desarrollo_idea TEXT,
    formulacion_categoria VARCHAR(100),
    formulacion_justificacion TEXT,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    fecha_modificacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ultima_presentacion TIMESTAMP WITH TIME ZONE,
    reaccion_audiencia JSONB DEFAULT '{"risas": 0, "silencio": 0, "aplausos": 0, "groans": 0}'::jsonb,
    notas TEXT,
    eliminado BOOLEAN DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_chistes_estado ON chistes(estado) WHERE NOT eliminado;
CREATE INDEX IF NOT EXISTS idx_chistes_fecha ON chistes(fecha_creacion DESC);

-- ========================================
-- 2. TABLA: analisis_chistes (análisis de chistes de otros)
-- ========================================
CREATE TABLE IF NOT EXISTS analisis_chistes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    titulo_referencia VARCHAR(255),
    comediante VARCHAR(255),
    chiste_completo TEXT,
    premisa TEXT,
    elemento_mecanico VARCHAR(100),
    ruptura TEXT,
    remate TEXT,
    perspectiva_categoria VARCHAR(100),
    perspectiva_justificacion TEXT,
    actitud VARCHAR(100),
    concepto TEXT,
    concepto_categoria VARCHAR(100),
    desarrollo_idea TEXT,
    formulacion_categoria VARCHAR(100),
    formulacion_justificacion TEXT,
    notas TEXT,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    fecha_modificacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    eliminado BOOLEAN DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_analisis_chistes_comediante ON analisis_chistes(comediante) WHERE NOT eliminado;
CREATE INDEX IF NOT EXISTS idx_analisis_chistes_fecha ON analisis_chistes(fecha_creacion DESC) WHERE NOT eliminado;

-- ========================================
-- 3. TABLA: categorias_dinamicas (dropdowns editables)
-- ========================================
CREATE TABLE IF NOT EXISTS categorias_dinamicas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tipo VARCHAR(50) NOT NULL,
    valor VARCHAR(255) NOT NULL,
    usuario_creado BOOLEAN DEFAULT TRUE,
    orden INTEGER DEFAULT 0,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_tipo_valor UNIQUE (tipo, valor)
);

CREATE INDEX IF NOT EXISTS idx_categorias_tipo ON categorias_dinamicas(tipo, orden);

-- ========================================
-- 4. TABLA: tags
-- ========================================
CREATE TABLE IF NOT EXISTS tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR(100) UNIQUE NOT NULL,
    categoria VARCHAR(50) CHECK (categoria IN ('tema', 'tecnica', 'audiencia', 'tono', 'evento')),
    color VARCHAR(20) DEFAULT '#6B7280',
    descripcion TEXT,
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ========================================
-- 5. TABLA: presentaciones
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

-- ========================================
-- 6. TABLA: bitacora
-- ========================================
CREATE TABLE IF NOT EXISTS bitacora (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fecha TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    tipo VARCHAR(50) DEFAULT 'nota_general' CHECK (tipo IN ('practica', 'reflexion', 'idea', 'observacion', 'nota_general')),
    titulo VARCHAR(255),
    contenido TEXT NOT NULL,
    estado_animo VARCHAR(50),
    tags TEXT[],
    chiste_relacionado_id UUID REFERENCES chistes(id) ON DELETE SET NULL,
    presentacion_relacionada_id UUID REFERENCES presentaciones(id) ON DELETE SET NULL,
    eliminado BOOLEAN DEFAULT FALSE,
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    modificado_en TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_bitacora_fecha ON bitacora(fecha DESC) WHERE NOT eliminado;

-- ========================================
-- 7. TRIGGERS para actualizar timestamps
-- ========================================
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_modificacion = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_chistes_modtime ON chistes;
CREATE TRIGGER update_chistes_modtime
    BEFORE UPDATE ON chistes
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

DROP TRIGGER IF EXISTS update_analisis_chistes_modtime ON analisis_chistes;
CREATE TRIGGER update_analisis_chistes_modtime
    BEFORE UPDATE ON analisis_chistes
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

-- ========================================
-- 8. DATOS INICIALES: Tags comunes
-- ========================================
INSERT INTO tags (nombre, categoria, color) VALUES
    ('familia', 'tema', '#EF4444'),
    ('tecnologia', 'tema', '#3B82F6'),
    ('relaciones', 'tema', '#EC4899'),
    ('trabajo', 'tema', '#F59E0B'),
    ('observacional', 'tecnica', '#F97316'),
    ('autoburla', 'tecnica', '#84CC16'),
    ('sarcasmo', 'tecnica', '#A855F7'),
    ('absurdo', 'tecnica', '#EC4899'),
    ('general', 'audiencia', '#6B7280'),
    ('adultos', 'audiencia', '#DC2626')
ON CONFLICT (nombre) DO NOTHING;

-- ========================================
-- 9. VERIFICAR CREACIÓN
-- ========================================
SELECT 'TABLAS CREADAS:' as status;
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_name IN ('chistes', 'analisis_chistes', 'categorias_dinamicas', 'tags', 'presentaciones', 'bitacora')
ORDER BY table_name;

-- ========================================
-- ¡SETUP COMPLETADO!
-- ========================================
