"""
Script para ejecutar la migración de análisis en Supabase
"""
import os
from dotenv import load_dotenv
from src.services.supabase_client import SupabaseClient
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

def run_migration():
    """Ejecuta la migración SQL en Supabase"""
    try:
        # Obtener cliente de Supabase
        client = SupabaseClient.get_client()

        # Leer el archivo de migración
        migration_file = 'database_migration_analysis.sql'

        if not os.path.exists(migration_file):
            logger.error(f"Archivo de migración no encontrado: {migration_file}")
            return False

        with open(migration_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        logger.info("=" * 60)
        logger.info("MIGRACIÓN DE BASE DE DATOS - SISTEMA DE ANÁLISIS")
        logger.info("=" * 60)
        logger.info("")
        logger.info("⚠️  IMPORTANTE:")
        logger.info("Este script NO puede ejecutar SQL directamente en Supabase desde Python.")
        logger.info("")
        logger.info("📋 INSTRUCCIONES:")
        logger.info("1. Ve a https://supabase.com/dashboard")
        logger.info("2. Selecciona tu proyecto")
        logger.info("3. Ve a 'SQL Editor' en el menú lateral")
        logger.info("4. Crea una nueva query")
        logger.info("5. Copia y pega el contenido de:")
        logger.info(f"   📄 {os.path.abspath(migration_file)}")
        logger.info("6. Ejecuta la query (botón 'Run' o Ctrl+Enter)")
        logger.info("")
        logger.info("=" * 60)
        logger.info("")
        logger.info("✅ La migración incluye:")
        logger.info("   • Nueva tabla: analisis_chistes")
        logger.info("   • Nueva tabla: categorias_dinamicas")
        logger.info("   • Nuevos campos en tabla chistes:")
        logger.info("     - ruptura, elemento_mecanico")
        logger.info("     - perspectiva_categoria, perspectiva_justificacion")
        logger.info("     - actitud, concepto_categoria")
        logger.info("     - desarrollo_idea")
        logger.info("     - formulacion_categoria, formulacion_justificacion")
        logger.info("")
        logger.info("🔍 Verificación post-migración:")
        logger.info("   Ejecuta en Supabase SQL Editor:")
        logger.info("   SELECT table_name FROM information_schema.tables")
        logger.info("   WHERE table_schema = 'public';")
        logger.info("")
        logger.info("=" * 60)

        return True

    except Exception as e:
        logger.error(f"Error: {e}")
        return False

if __name__ == '__main__':
    run_migration()
