"""
Ejecutar SQL directamente en Supabase usando psycopg2
"""
import os
from dotenv import load_dotenv
import re

# Cargar variables de entorno
load_dotenv()

def get_connection_string():
    """Construir connection string desde SUPABASE_URL"""
    supabase_url = os.getenv('SUPABASE_URL')
    service_key = os.getenv('SUPABASE_SERVICE_KEY')

    # Extraer el project ref de la URL
    # https://pwztxtbwomiftdmogwjq.supabase.co -> pwztxtbwomiftdmogwjq
    match = re.search(r'https://([^.]+)\.supabase\.co', supabase_url)
    if match:
        project_ref = match.group(1)
        # Usar pooler de Supabase en modo directo
        conn_string = f"postgresql://postgres.{project_ref}:postgres@aws-0-us-east-1.pooler.supabase.com:5432/postgres"
        return conn_string
    return None

def execute_sql_file():
    """Ejecutar el archivo SQL"""
    try:
        import psycopg2
    except ImportError:
        print("[ERROR] psycopg2 no esta instalado")
        print("Instalando psycopg2-binary...")
        import subprocess
        subprocess.run(["pip", "install", "psycopg2-binary"], check=True)
        import psycopg2

    # Leer archivo SQL
    with open('create_mejoras_table.sql', 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # Intentar conexión usando service_key como password
    supabase_url = os.getenv('SUPABASE_URL')
    service_key = os.getenv('SUPABASE_SERVICE_KEY')

    # Extraer project ref
    match = re.search(r'https://([^.]+)\.supabase\.co', supabase_url)
    if not match:
        print("[ERROR] No se pudo extraer project ref de SUPABASE_URL")
        return False

    project_ref = match.group(1)

    # Connection strings para probar
    connection_attempts = [
        # Pooler de Supabase (Transaction mode)
        {
            'host': f'aws-0-us-east-1.pooler.supabase.com',
            'port': 6543,
            'database': 'postgres',
            'user': f'postgres.{project_ref}',
            'password': service_key
        },
        # Directo a la base de datos
        {
            'host': f'db.{project_ref}.supabase.co',
            'port': 5432,
            'database': 'postgres',
            'user': 'postgres',
            'password': service_key
        }
    ]

    for idx, conn_params in enumerate(connection_attempts, 1):
        print(f"\n[INFO] Intento {idx}: Conectando a {conn_params['host']}:{conn_params['port']}...")
        try:
            conn = psycopg2.connect(**conn_params)
            conn.autocommit = True
            cursor = conn.cursor()

            print("[OK] Conexion exitosa!")
            print("[INFO] Ejecutando SQL...")

            # Dividir en statements individuales y ejecutar
            statements = sql_content.split(';')
            successful = 0

            for statement in statements:
                statement = statement.strip()
                if statement and not statement.startswith('--'):
                    try:
                        cursor.execute(statement)
                        successful += 1
                    except Exception as e:
                        # Ignorar errores de "ya existe"
                        if 'already exists' in str(e) or 'ya existe' in str(e):
                            successful += 1
                        else:
                            print(f"[WARN] Error en statement: {str(e)[:100]}")

            print(f"[OK] Ejecutados {successful} statements exitosamente")

            # Verificar que la tabla existe
            cursor.execute("""
                SELECT COUNT(*) FROM mejoras_app;
            """)
            count = cursor.fetchone()[0]
            print(f"[OK] Tabla 'mejoras_app' creada con {count} registros iniciales")

            # Cerrar conexión
            cursor.close()
            conn.close()

            return True

        except Exception as e:
            print(f"[ERROR] Fallo: {str(e)[:200]}")
            continue

    print("\n[ERROR] No se pudo conectar con ninguno de los metodos")
    print("[INFO] Intenta ejecutar manualmente en el SQL Editor de Supabase:")
    print("       https://supabase.com/dashboard/project/pwztxtbwomiftdmogwjq/sql/new")
    return False

if __name__ == '__main__':
    print("=" * 60)
    print("EJECUTANDO MIGRACION SQL EN SUPABASE")
    print("=" * 60)
    execute_sql_file()
