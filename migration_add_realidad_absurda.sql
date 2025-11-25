-- ========================================
-- MIGRACIÓN: Agregar campo realidad_absurda
-- ========================================
-- Ejecutar en Supabase SQL Editor
-- Agrega el campo realidad_absurda a la tabla analisis_ia

-- Agregar columna realidad_absurda
ALTER TABLE analisis_ia
ADD COLUMN IF NOT EXISTS realidad_absurda TEXT;

-- Agregar comentario para documentación
COMMENT ON COLUMN analisis_ia.realidad_absurda IS 'La realidad absurda o inesperada que rompe las expectativas en el chiste';

-- Verificar que se agregó correctamente
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'analisis_ia'
AND column_name = 'realidad_absurda';

-- ========================================
-- FIN DE LA MIGRACIÓN
-- ========================================
