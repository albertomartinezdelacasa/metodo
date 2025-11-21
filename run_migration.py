"""
Script para ejecutar la migración de base de datos automáticamente
"""
import sys
from pathlib import Path

# Añadir el directorio raíz al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from src.services.supabase_client import SupabaseClient
from src.config import config


def run_migration():
    """Ejecuta la migración de base de datos"""

    print("=" * 60)
    print("MIGRACIÓN DE BASE DE DATOS - MÉTODO COMEDIA")
    print("=" * 60)
    print()

    # Verificar configuración
    if not config.SUPABASE_URL or not config.SUPABASE_SERVICE_KEY:
        print("❌ Error: Credenciales de Supabase no configuradas")
        print("Necesitas SUPABASE_URL y SUPABASE_SERVICE_KEY en .env")
        return False

    try:
        # Obtener cliente de Supabase
        client = SupabaseClient.get_client()
        print("✅ Conectado a Supabase")
        print()

        # SQL para la migración
        migrations = [
            {
                "name": "Agregar campos a tabla 'chistes'",
                "sql": """
                    ALTER TABLE chistes
                    ADD COLUMN IF NOT EXISTS concepto TEXT,
                    ADD COLUMN IF NOT EXISTS premisa TEXT,
                    ADD COLUMN IF NOT EXISTS remate TEXT;
                """
            },
            {
                "name": "Agregar campos de conceptos a 'analisis_ia'",
                "sql": """
                    ALTER TABLE analisis_ia
                    ADD COLUMN IF NOT EXISTS tipo_concepto VARCHAR(50) CHECK (tipo_concepto IN ('simple', 'compuesto', 'concreto', 'abstracto')),
                    ADD COLUMN IF NOT EXISTS explicacion_tipo_concepto TEXT,
                    ADD COLUMN IF NOT EXISTS mapa_conceptos JSONB;
                """
            },
            {
                "name": "Agregar campos de rupturas a 'analisis_ia'",
                "sql": """
                    ALTER TABLE analisis_ia
                    ADD COLUMN IF NOT EXISTS tipo_ruptura VARCHAR(100),
                    ADD COLUMN IF NOT EXISTS subtipo_ruptura VARCHAR(100),
                    ADD COLUMN IF NOT EXISTS explicacion_ruptura TEXT;
                """
            },
            {
                "name": "Crear tabla 'bitacora'",
                "sql": """
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
                """
            },
            {
                "name": "Crear índices para bitacora",
                "sql": """
                    CREATE INDEX IF NOT EXISTS idx_bitacora_fecha ON bitacora(fecha DESC) WHERE NOT eliminado;
                    CREATE INDEX IF NOT EXISTS idx_bitacora_tipo ON bitacora(tipo) WHERE NOT eliminado;
                    CREATE INDEX IF NOT EXISTS idx_bitacora_chiste ON bitacora(chiste_relacionado_id) WHERE chiste_relacionado_id IS NOT NULL;
                """
            }
        ]

        # Ejecutar cada migración
        for i, migration in enumerate(migrations, 1):
            print(f"[{i}/{len(migrations)}] {migration['name']}...")

            try:
                # Nota: Supabase Python client no soporta directamente ALTER TABLE
                # Necesitamos usar la función rpc o hacerlo manualmente en el dashboard
                print(f"    ⚠️  Esta migración debe ejecutarse manualmente en Supabase SQL Editor")
                print(f"    SQL: {migration['sql'][:80]}...")

            except Exception as e:
                print(f"    ❌ Error: {e}")
                return False

        print()
        print("=" * 60)
        print("⚠️  ACCIÓN REQUERIDA:")
        print("=" * 60)
        print()
        print("El cliente Python de Supabase no soporta ALTER TABLE directamente.")
        print("Debes ejecutar la migración manualmente:")
        print()
        print("1. Ve a: https://supabase.com/dashboard")
        print("2. Abre tu proyecto")
        print("3. Ve a 'SQL Editor'")
        print("4. Copia y pega el contenido de 'migration_add_analysis_fields.sql'")
        print("5. Click en 'Run'")
        print()
        print("Alternativamente, puedes usar este script SQL simplificado:")
        print()
        print("-" * 60)
        print()

        # Imprimir SQL consolidado
        full_sql = "\n\n".join([m["sql"] for m in migrations])
        print(full_sql)

        print()
        print("-" * 60)
        print()
        print("Una vez ejecutado, tu base de datos estará lista!")
        print()

        return True

    except Exception as e:
        print(f"❌ Error conectando a Supabase: {e}")
        return False


if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)
