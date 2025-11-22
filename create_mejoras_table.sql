-- ========================================
-- TABLA: mejoras_app
-- ========================================
-- Sistema de gestión de mejoras y feature requests para la aplicación

CREATE TABLE IF NOT EXISTS mejoras_app (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Información básica
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,

    -- Categorización
    tipo VARCHAR(50) CHECK (tipo IN (
        'feature',      -- Nueva funcionalidad
        'mejora',       -- Mejora de algo existente
        'bug',          -- Corrección de error
        'ui_ux',        -- Mejora de interfaz/experiencia
        'performance',  -- Optimización de rendimiento
        'documentacion' -- Mejora de docs
    )) DEFAULT 'feature',

    prioridad VARCHAR(20) CHECK (prioridad IN (
        'critica',   -- Debe hacerse ASAP
        'alta',      -- Importante
        'media',     -- Bueno tenerlo
        'baja'       -- Nice to have
    )) DEFAULT 'media',

    -- Estado
    estado VARCHAR(50) CHECK (estado IN (
        'pendiente',    -- Por revisar
        'aprobada',     -- Aprobada para desarrollo
        'en_progreso',  -- En desarrollo
        'completada',   -- Terminada
        'descartada',   -- Decidido no hacerla
        'pausada'       -- En espera temporal
    )) DEFAULT 'pendiente',

    -- Estimación y tracking
    complejidad VARCHAR(20) CHECK (complejidad IN (
        'trivial',   -- < 1 hora
        'facil',     -- 1-4 horas
        'media',     -- 1 día
        'compleja',  -- 2-3 días
        'muy_compleja' -- 1+ semana
    )),

    tiempo_estimado_horas NUMERIC(5,1), -- Opcional: estimación manual en horas
    tiempo_real_horas NUMERIC(5,1),     -- Opcional: tiempo real invertido

    -- Categoría funcional (a qué parte de la app afecta)
    modulo VARCHAR(100), -- Ej: "chistes", "analisis_ia", "bitacora", "exportacion"

    -- Impacto
    impacto VARCHAR(20) CHECK (impacto IN (
        'muy_alto',  -- Cambia radicalmente la app
        'alto',      -- Mejora significativa
        'medio',     -- Mejora notable
        'bajo'       -- Mejora menor
    )),

    -- Beneficios esperados (puede ser texto o JSON)
    beneficios TEXT,

    -- Detalles técnicos
    notas_tecnicas TEXT, -- Notas de implementación, consideraciones técnicas
    dependencias TEXT[], -- IDs de otras mejoras que deben completarse antes

    -- Relación con usuarios/ideas
    fuente VARCHAR(50) CHECK (fuente IN (
        'usuario',      -- Pedido por usuario
        'equipo',       -- Idea del equipo
        'analytics',    -- Detectado en métricas
        'bug_report'    -- Reporte de error
    )) DEFAULT 'equipo',

    usuario_solicitante VARCHAR(255), -- Email o nombre de quien lo pidió

    -- URLs y referencias
    issue_url TEXT,       -- Link a issue de GitHub si existe
    pr_url TEXT,          -- Link a PR cuando se implemente
    documentacion_url TEXT, -- Link a docs relacionadas

    -- Screenshots/diseños
    imagenes_url TEXT[],  -- URLs de mockups, screenshots, etc

    -- Timestamps
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    fecha_modificacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    fecha_completada TIMESTAMP WITH TIME ZONE,
    fecha_descartada TIMESTAMP WITH TIME ZONE,

    -- Motivos
    motivo_descarte TEXT, -- Por qué se descartó
    notas_implementacion TEXT, -- Notas al completarla

    -- Soft delete
    eliminado BOOLEAN DEFAULT FALSE
);

-- ========================================
-- ÍNDICES
-- ========================================
CREATE INDEX idx_mejoras_estado ON mejoras_app(estado) WHERE NOT eliminado;
CREATE INDEX idx_mejoras_prioridad ON mejoras_app(prioridad) WHERE NOT eliminado;
CREATE INDEX idx_mejoras_tipo ON mejoras_app(tipo) WHERE NOT eliminado;
CREATE INDEX idx_mejoras_modulo ON mejoras_app(modulo) WHERE modulo IS NOT NULL;
CREATE INDEX idx_mejoras_fecha_creacion ON mejoras_app(fecha_creacion DESC);
CREATE INDEX idx_mejoras_complejidad ON mejoras_app(complejidad) WHERE complejidad IS NOT NULL;

-- ========================================
-- TRIGGER para fecha_modificacion
-- ========================================
CREATE TRIGGER update_mejoras_modtime
    BEFORE UPDATE ON mejoras_app
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

-- ========================================
-- VISTAS ÚTILES
-- ========================================

-- Vista de mejoras pendientes ordenadas por prioridad
CREATE OR REPLACE VIEW mejoras_pendientes AS
SELECT
    id,
    titulo,
    tipo,
    prioridad,
    estado,
    complejidad,
    modulo,
    fecha_creacion,
    CASE prioridad
        WHEN 'critica' THEN 1
        WHEN 'alta' THEN 2
        WHEN 'media' THEN 3
        WHEN 'baja' THEN 4
    END as orden_prioridad
FROM mejoras_app
WHERE estado IN ('pendiente', 'aprobada', 'en_progreso')
AND NOT eliminado
ORDER BY orden_prioridad, fecha_creacion;

-- Vista de estadísticas de mejoras
CREATE OR REPLACE VIEW estadisticas_mejoras AS
SELECT
    estado,
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE prioridad = 'critica') as criticas,
    COUNT(*) FILTER (WHERE prioridad = 'alta') as altas,
    AVG(tiempo_real_horas) FILTER (WHERE tiempo_real_horas IS NOT NULL) as promedio_horas
FROM mejoras_app
WHERE NOT eliminado
GROUP BY estado;

-- Vista de mejoras por módulo
CREATE OR REPLACE VIEW mejoras_por_modulo AS
SELECT
    modulo,
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE estado = 'completada') as completadas,
    COUNT(*) FILTER (WHERE estado IN ('pendiente', 'aprobada')) as pendientes,
    COUNT(*) FILTER (WHERE estado = 'en_progreso') as en_progreso
FROM mejoras_app
WHERE NOT eliminado
AND modulo IS NOT NULL
GROUP BY modulo
ORDER BY total DESC;

-- ========================================
-- DATOS INICIALES (ejemplos)
-- ========================================
INSERT INTO mejoras_app (titulo, descripcion, tipo, prioridad, estado, complejidad, modulo, impacto) VALUES

('Exportar chistes a Obsidian',
 'Permitir exportar chistes individuales o todos los chistes al vault de Obsidian en formato Markdown',
 'feature', 'media', 'pendiente', 'media', 'exportacion', 'medio'),

('Grabar audio de chistes',
 'Añadir funcionalidad para grabar audio mientras practicas un chiste y guardarlo vinculado al chiste',
 'feature', 'alta', 'pendiente', 'compleja', 'chistes', 'alto'),

('Modo offline completo',
 'Mejorar PWA para que funcione 100% offline, guardando cambios y sincronizando cuando vuelva conexión',
 'mejora', 'media', 'pendiente', 'compleja', 'pwa', 'alto'),

('Dashboard de estadísticas',
 'Crear página de estadísticas con gráficos: chistes por estado, uso a lo largo del tiempo, mejores valorados, etc',
 'feature', 'media', 'pendiente', 'media', 'analytics', 'medio'),

('Búsqueda y filtros avanzados',
 'Añadir barra de búsqueda con filtros: por texto, tags, calificación, estado, fecha',
 'feature', 'alta', 'pendiente', 'facil', 'chistes', 'alto'),

('Modo oscuro',
 'Implementar tema oscuro para la interfaz',
 'ui_ux', 'baja', 'pendiente', 'facil', 'frontend', 'bajo'),

('Integración con Google Calendar',
 'Sincronizar presentaciones con Google Calendar automáticamente',
 'feature', 'baja', 'pendiente', 'media', 'presentaciones', 'medio')

ON CONFLICT DO NOTHING;

-- ========================================
-- VERIFICACIÓN
-- ========================================
SELECT
    'Tabla mejoras_app creada correctamente' as mensaje,
    COUNT(*) as ejemplos_insertados
FROM mejoras_app;
