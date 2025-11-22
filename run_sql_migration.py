"""
Script para ejecutar la migración SQL en Supabase
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Cargar variables de entorno
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

def ejecutar_migracion():
    """Ejecuta el archivo SQL en Supabase"""

    # Leer el archivo SQL
    with open('create_mejoras_table.sql', 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # Crear cliente de Supabase
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

    print("Ejecutando migración de base de datos...")
    print("=" * 60)

    try:
        # Ejecutar el SQL usando la API REST de Supabase
        # Nota: Supabase no permite ejecutar SQL arbitrario via REST API
        # Necesitas hacerlo desde el SQL Editor del dashboard

        print("IMPORTANTE:")
        print()
        print("Supabase no permite ejecutar SQL directamente desde Python.")
        print("Debes seguir estos pasos:")
        print()
        print("1. Ve a: https://supabase.com/dashboard/project/pwztxtbwomiftdmogwjq/sql/new")
        print("2. Copia y pega el contenido del archivo: create_mejoras_table.sql")
        print("3. Haz clic en 'Run' (F5)")
        print()
        print("=" * 60)

        # Verificar si la tabla ya existe
        print("\nVerificando conexion con Supabase...")
        try:
            # Intentar query simple para verificar conexión
            result = supabase.table('chistes').select("id").limit(1).execute()
            print("[OK] Conexion con Supabase exitosa")

            # Intentar verificar si la tabla ya existe
            try:
                result = supabase.table('mejoras_app').select("id").limit(1).execute()
                print("[OK] La tabla 'mejoras_app' ya existe en la base de datos")

                # Contar registros
                count_result = supabase.table('mejoras_app').select("*", count='exact').execute()
                print(f"Total de mejoras registradas: {count_result.count}")

            except Exception as e:
                print("[INFO] La tabla 'mejoras_app' aun no existe (es normal si es la primera vez)")

        except Exception as e:
            print(f"[ERROR] Error de conexion: {e}")
            return False

        return True

    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False

if __name__ == '__main__':
    ejecutar_migracion()
