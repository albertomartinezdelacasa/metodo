"""
Cliente de Todoist para sincronización de tareas
"""
import requests
from src.config import config
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)


class TodoistClient:
    """Cliente para interactuar con la API de Todoist"""

    def __init__(self):
        self.token = config.TODOIST_TOKEN
        self.project_id = config.TODOIST_PROJECT_ID
        self.base_url = "https://api.todoist.com/rest/v2"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Realiza una petición a la API de Todoist"""
        url = f"{self.base_url}/{endpoint}"

        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data)
            elif method == "DELETE":
                response = requests.delete(url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json() if response.content else {}

        except requests.exceptions.RequestException as e:
            logger.error(f"Todoist API error: {e}")
            raise

    def get_project_tasks(self) -> List[Dict]:
        """Obtiene todas las tareas del proyecto Metodo"""
        try:
            tasks = self._make_request("GET", f"tasks?project_id={self.project_id}")
            logger.info(f"Retrieved {len(tasks)} tasks from Todoist")
            return tasks
        except Exception as e:
            logger.error(f"Error getting project tasks: {e}")
            return []

    def create_task(self, content: str, description: str = "",
                   priority: int = 1, labels: List[str] = None) -> Dict:
        """Crea una nueva tarea en Todoist"""
        task_data = {
            "content": content,
            "project_id": self.project_id,
            "priority": priority
        }

        if description:
            task_data["description"] = description

        if labels:
            task_data["labels"] = labels

        try:
            task = self._make_request("POST", "tasks", task_data)
            logger.info(f"Task created: {task['id']} - {content}")
            return task
        except Exception as e:
            logger.error(f"Error creating task: {e}")
            raise

    def complete_task(self, task_id: str) -> bool:
        """Marca una tarea como completada"""
        try:
            self._make_request("POST", f"tasks/{task_id}/close")
            logger.info(f"Task completed: {task_id}")
            return True
        except Exception as e:
            logger.error(f"Error completing task {task_id}: {e}")
            return False

    def sync_joke_to_task(self, joke_id: str, joke_title: str, estado: str) -> Optional[Dict]:
        """Sincroniza un chiste con Todoist como tarea"""
        task_content = f"Revisar chiste: {joke_title}"
        task_description = f"Estado: {estado}\nID: {joke_id}"

        # Determinar prioridad basado en estado
        priority_map = {
            'borrador': 2,
            'revisado': 3,
            'probado': 4,
            'pulido': 1
        }
        priority = priority_map.get(estado, 1)

        try:
            task = self.create_task(
                content=task_content,
                description=task_description,
                priority=priority,
                labels=['chiste', estado]
            )
            return task
        except Exception as e:
            logger.error(f"Error syncing joke {joke_id} to Todoist: {e}")
            return None


# Instancia global
todoist_client = TodoistClient() if config.TODOIST_TOKEN else None
