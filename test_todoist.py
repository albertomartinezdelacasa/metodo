"""
Script para consultar las tareas de Todoist del proyecto Metodo Comedia
"""
import sys
import os
from pathlib import Path

# Configurar encoding para Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')

# Añadir el directorio raíz al path para imports
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from src.services.todoist_client import todoist_client
from src.config import config


def main():
    """Consulta y muestra las tareas del proyecto Todoist"""

    # Verificar configuración
    if not config.TODOIST_TOKEN:
        print("❌ Error: TODOIST_TOKEN no configurado en .env")
        print("Por favor, configura tu token de Todoist en el archivo .env")
        return

    if not config.TODOIST_PROJECT_ID:
        print("❌ Error: TODOIST_PROJECT_ID no configurado en .env")
        return

    print("🔍 Consultando tareas de Todoist...")
    print(f"📁 Proyecto ID: {config.TODOIST_PROJECT_ID}")
    print("-" * 60)

    try:
        # Obtener tareas del proyecto
        tasks = todoist_client.get_project_tasks()

        if not tasks:
            print("✅ No hay tareas pendientes en el proyecto")
            return

        print(f"\n📋 Total de tareas: {len(tasks)}\n")

        # Mostrar cada tarea
        for i, task in enumerate(tasks, 1):
            print(f"\n{'='*60}")
            print(f"Tarea #{i}")
            print(f"{'='*60}")
            print(f"📌 Contenido: {task.get('content', 'Sin título')}")
            print(f"🆔 ID: {task.get('id', 'N/A')}")

            # Descripción
            description = task.get('description', '')
            if description:
                print(f"📝 Descripción: {description}")

            # Prioridad (1-4, siendo 4 la más alta)
            priority = task.get('priority', 1)
            priority_labels = {1: '⚪ Baja', 2: '🔵 Media', 3: '🟡 Alta', 4: '🔴 Urgente'}
            print(f"⚡ Prioridad: {priority_labels.get(priority, 'N/A')}")

            # Labels/Etiquetas
            labels = task.get('labels', [])
            if labels:
                print(f"🏷️  Etiquetas: {', '.join(labels)}")

            # Fecha de creación
            created_at = task.get('created_at', 'N/A')
            print(f"📅 Creada: {created_at}")

            # Fecha de vencimiento
            due = task.get('due')
            if due:
                due_date = due.get('date', 'N/A')
                print(f"⏰ Vencimiento: {due_date}")

            # URL de la tarea
            url = task.get('url', '')
            if url:
                print(f"🔗 URL: {url}")

        print(f"\n{'='*60}\n")
        print(f"✅ Consulta completada: {len(tasks)} tarea(s) encontrada(s)")

    except Exception as e:
        print(f"\n❌ Error al consultar Todoist: {e}")
        print("\nPosibles causas:")
        print("- Token de API inválido o expirado")
        print("- ID de proyecto incorrecto")
        print("- Problemas de conexión a internet")
        print("- Límites de rate limit de la API")


if __name__ == "__main__":
    main()
