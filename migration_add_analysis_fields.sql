-- ========================================
-- MIGRACIÓN: Agregar campos de análisis avanzado
-- ========================================
-- Ejecutar en Supabase SQL Editor después de crear las tablas iniciales
-- Esta migración agrega campos nuevos a tablas existentes

-- ========================================
-- 1. Agregar campos a tabla 'chistes'
-- ========================================

-- Agregar campos de análisis básico
ALTER TABLE chistes
ADD COLUMN IF NOT EXISTS concepto TEXT,
ADD COLUMN IF NOT EXISTS premisa TEXT,
ADD COLUMN IF NOT EXISTS remate TEXT;

-- ========================================
-- 2. Agregar campos a tabla 'analisis_ia'
-- ========================================

-- Agregar campos de análisis de conceptos
ALTER TABLE analisis_ia
ADD COLUMN IF NOT EXISTS tipo_concepto VARCHAR(50) CHECK (tipo_concepto IN ('simple', 'compuesto', 'concreto', 'abstracto')),
ADD COLUMN IF NOT EXISTS explicacion_tipo_concepto TEXT,
ADD COLUMN IF NOT EXISTS mapa_conceptos JSONB;

-- Agregar campos de análisis de rupturas
ALTER TABLE analisis_ia
ADD COLUMN IF NOT EXISTS tipo_ruptura VARCHAR(100),
ADD COLUMN IF NOT EXISTS subtipo_ruptura VARCHAR(100),
ADD COLUMN IF NOT EXISTS explicacion_ruptura TEXT;

-- ========================================
-- 3. Crear tabla 'bitacora' si no existe
-- ========================================

CREATE TABLE IF NOT EXISTS bitacora (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fecha TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    tipo VARCHAR(50) CHECK (tipo IN ('practica', 'reflexion', 'idea', 'observacion', 'nota_general')) DEFAULT 'nota_general',
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

-- ========================================
-- 4. Crear índices para nuevos campos
-- ========================================

CREATE INDEX IF NOT EXISTS idx_bitacora_fecha ON bitacora(fecha DESC) WHERE NOT eliminado;
CREATE INDEX IF NOT EXISTS idx_bitacora_tipo ON bitacora(tipo) WHERE NOT eliminado;
CREATE INDEX IF NOT EXISTS idx_bitacora_chiste ON bitacora(chiste_relacionado_id) WHERE chiste_relacionado_id IS NOT NULL;

-- ========================================
-- 5. Crear trigger para bitácora
-- ========================================

-- Reutilizar la función update_modified_column existente
CREATE TRIGGER IF NOT EXISTS update_bitacora_modtime
    BEFORE UPDATE ON bitacora
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

-- ========================================
-- 6. Verificación
-- ========================================

-- Verificar que los campos se agregaron correctamente
SELECT
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'chistes'
AND column_name IN ('concepto', 'premisa', 'remate')
ORDER BY column_name;

SELECT
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'analisis_ia'
AND column_name IN ('tipo_concepto', 'explicacion_tipo_concepto', 'mapa_conceptos', 'tipo_ruptura', 'subtipo_ruptura', 'explicacion_ruptura')
ORDER BY column_name;

-- Verificar que bitacora se creó
SELECT EXISTS (
    SELECT FROM information_schema.tables
    WHERE table_schema = 'public'
    AND table_name = 'bitacora'
) as bitacora_existe;

-- ========================================
-- FIN DE LA MIGRACIÓN
-- ========================================
