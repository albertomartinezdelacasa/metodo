-- ========================================
-- MIGRACIÓN SIMPLIFICADA - EJECUTAR EN SUPABASE SQL EDITOR
-- ========================================
-- Copia y pega este archivo completo en Supabase SQL Editor y click "Run"

-- 1. Agregar campos a tabla 'chistes'
ALTER TABLE chistes
ADD COLUMN IF NOT EXISTS concepto TEXT,
ADD COLUMN IF NOT EXISTS premisa TEXT,
ADD COLUMN IF NOT EXISTS remate TEXT;

-- 2. Agregar campos de conceptos a 'analisis_ia'
ALTER TABLE analisis_ia
ADD COLUMN IF NOT EXISTS tipo_concepto VARCHAR(50),
ADD COLUMN IF NOT EXISTS explicacion_tipo_concepto TEXT,
ADD COLUMN IF NOT EXISTS mapa_conceptos JSONB;

-- 3. Agregar campos de rupturas a 'analisis_ia'
ALTER TABLE analisis_ia
ADD COLUMN IF NOT EXISTS tipo_ruptura VARCHAR(100),
ADD COLUMN IF NOT EXISTS subtipo_ruptura VARCHAR(100),
ADD COLUMN IF NOT EXISTS explicacion_ruptura TEXT;

-- 4. Crear tabla 'bitacora'
CREATE TABLE IF NOT EXISTS bitacora (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fecha TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    tipo VARCHAR(50) DEFAULT 'nota_general',
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

-- 5. Crear índices para bitacora
CREATE INDEX IF NOT EXISTS idx_bitacora_fecha ON bitacora(fecha DESC) WHERE NOT eliminado;
CREATE INDEX IF NOT EXISTS idx_bitacora_tipo ON bitacora(tipo) WHERE NOT eliminado;
CREATE INDEX IF NOT EXISTS idx_bitacora_chiste ON bitacora(chiste_relacionado_id) WHERE chiste_relacionado_id IS NOT NULL;

-- 6. Crear trigger para actualizar modificado_en en bitacora
-- La función ya debe existir del schema inicial, pero la recreamos por si acaso
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.modificado_en = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Eliminar trigger si existe y crearlo de nuevo
DROP TRIGGER IF EXISTS update_bitacora_modtime ON bitacora;

CREATE TRIGGER update_bitacora_modtime
    BEFORE UPDATE ON bitacora
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

-- 7. Agregar constraints de CHECK (si no existen)
DO $$
BEGIN
    -- Constraint para tipo_concepto
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'analisis_ia_tipo_concepto_check'
    ) THEN
        ALTER TABLE analisis_ia
        ADD CONSTRAINT analisis_ia_tipo_concepto_check
        CHECK (tipo_concepto IN ('simple', 'compuesto', 'concreto', 'abstracto'));
    END IF;

    -- Constraint para tipo en bitacora
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'bitacora_tipo_check'
    ) THEN
        ALTER TABLE bitacora
        ADD CONSTRAINT bitacora_tipo_check
        CHECK (tipo IN ('practica', 'reflexion', 'idea', 'observacion', 'nota_general'));
    END IF;
END $$;

-- 8. Verificar que todo se creó correctamente
SELECT
    'chistes' as tabla,
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'chistes'
AND column_name IN ('concepto', 'premisa', 'remate')

UNION ALL

SELECT
    'analisis_ia' as tabla,
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'analisis_ia'
AND column_name IN ('tipo_concepto', 'explicacion_tipo_concepto', 'mapa_conceptos', 'tipo_ruptura', 'subtipo_ruptura', 'explicacion_ruptura')

UNION ALL

SELECT
    'bitacora' as tabla,
    'tabla_existe' as column_name,
    'boolean' as data_type
FROM information_schema.tables
WHERE table_name = 'bitacora'

ORDER BY tabla, column_name;

-- ========================================
-- FIN DE LA MIGRACIÓN
-- ========================================
-- Si ves resultados en la última query, la migración fue exitosa!
