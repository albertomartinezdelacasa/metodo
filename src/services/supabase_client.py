"""
Cliente de Supabase para gestión de base de datos
"""
from supabase import create_client, Client
from src.config import config
from typing import Optional, Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class SupabaseClient:
    """Cliente singleton de Supabase"""

    _instance: Optional[Client] = None

    @classmethod
    def get_client(cls) -> Client:
        """Obtiene o crea una instancia del cliente de Supabase"""
        if cls._instance is None:
            if not config.SUPABASE_URL or not config.SUPABASE_KEY:
                raise ValueError("Supabase credentials not configured")

            cls._instance = create_client(
                config.SUPABASE_URL,
                config.SUPABASE_KEY
            )
            logger.info("Supabase client initialized")

        return cls._instance


class JokesRepository:
    """Repositorio para gestionar chistes en Supabase"""

    def __init__(self):
        self.client = SupabaseClient.get_client()
        self.table = 'chistes'

    def create_joke(self, joke_data: Dict[str, Any]) -> Dict:
        """Crea un nuevo chiste"""
        try:
            result = self.client.table(self.table).insert(joke_data).execute()
            logger.info(f"Joke created: {result.data[0]['id']}")
            return result.data[0]
        except Exception as e:
            logger.error(f"Error creating joke: {e}")
            raise

    def get_joke(self, joke_id: str) -> Optional[Dict]:
        """Obtiene un chiste por ID"""
        try:
            result = self.client.table(self.table)\
                .select('*')\
                .eq('id', joke_id)\
                .eq('eliminado', False)\
                .execute()

            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error getting joke {joke_id}: {e}")
            raise

    def get_all_jokes(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Obtiene todos los chistes con filtros opcionales"""
        try:
            query = self.client.table(self.table)\
                .select('*')\
                .eq('eliminado', False)\
                .order('fecha_creacion', desc=True)

            # Aplicar filtros si existen
            if filters:
                if 'estado' in filters:
                    query = query.eq('estado', filters['estado'])
                if 'calificacion_min' in filters:
                    query = query.gte('calificacion', filters['calificacion_min'])

            result = query.execute()
            return result.data
        except Exception as e:
            logger.error(f"Error getting jokes: {e}")
            raise

    def update_joke(self, joke_id: str, updates: Dict[str, Any]) -> Dict:
        """Actualiza un chiste"""
        try:
            result = self.client.table(self.table)\
                .update(updates)\
                .eq('id', joke_id)\
                .execute()

            logger.info(f"Joke updated: {joke_id}")
            return result.data[0]
        except Exception as e:
            logger.error(f"Error updating joke {joke_id}: {e}")
            raise

    def delete_joke(self, joke_id: str, soft_delete: bool = True) -> bool:
        """Elimina un chiste (soft delete por defecto)"""
        try:
            if soft_delete:
                self.client.table(self.table)\
                    .update({'eliminado': True})\
                    .eq('id', joke_id)\
                    .execute()
            else:
                self.client.table(self.table)\
                    .delete()\
                    .eq('id', joke_id)\
                    .execute()

            logger.info(f"Joke deleted: {joke_id} (soft={soft_delete})")
            return True
        except Exception as e:
            logger.error(f"Error deleting joke {joke_id}: {e}")
            raise

    def increment_usage(self, joke_id: str) -> Dict:
        """Incrementa el contador de veces usado"""
        try:
            # Primero obtener el valor actual
            joke = self.get_joke(joke_id)
            if not joke:
                raise ValueError(f"Joke {joke_id} not found")

            new_count = (joke.get('veces_usado', 0) or 0) + 1

            result = self.client.table(self.table)\
                .update({
                    'veces_usado': new_count,
                    'ultima_presentacion': 'now()'
                })\
                .eq('id', joke_id)\
                .execute()

            return result.data[0]
        except Exception as e:
            logger.error(f"Error incrementing usage for joke {joke_id}: {e}")
            raise


class AnalysisRepository:
    """Repositorio para gestionar análisis de IA"""

    def __init__(self):
        self.client = SupabaseClient.get_client()
        self.table = 'analisis_ia'

    def create_analysis(self, analysis_data: Dict[str, Any]) -> Dict:
        """Guarda un análisis de IA"""
        try:
            result = self.client.table(self.table).insert(analysis_data).execute()
            logger.info(f"Analysis created for joke: {analysis_data.get('chiste_id')}")
            return result.data[0]
        except Exception as e:
            logger.error(f"Error creating analysis: {e}")
            raise

    def get_joke_analyses(self, joke_id: str) -> List[Dict]:
        """Obtiene todos los análisis de un chiste"""
        try:
            result = self.client.table(self.table)\
                .select('*')\
                .eq('chiste_id', joke_id)\
                .order('fecha_analisis', desc=True)\
                .execute()

            return result.data
        except Exception as e:
            logger.error(f"Error getting analyses for joke {joke_id}: {e}")
            raise

    def get_latest_analysis(self, joke_id: str) -> Optional[Dict]:
        """Obtiene el análisis más reciente de un chiste"""
        try:
            result = self.client.table(self.table)\
                .select('*')\
                .eq('chiste_id', joke_id)\
                .order('fecha_analisis', desc=True)\
                .limit(1)\
                .execute()

            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error getting latest analysis for joke {joke_id}: {e}")
            raise


class BitacoraRepository:
    """Repositorio para gestionar entradas de bitácora"""

    def __init__(self):
        self.client = SupabaseClient.get_client()
        self.table = 'bitacora'

    def create_entry(self, entry_data: Dict[str, Any]) -> Dict:
        """Crea una nueva entrada de bitácora"""
        try:
            result = self.client.table(self.table).insert(entry_data).execute()
            logger.info(f"Bitácora entry created: {result.data[0]['id']}")
            return result.data[0]
        except Exception as e:
            logger.error(f"Error creating bitácora entry: {e}")
            raise

    def get_entry(self, entry_id: str) -> Optional[Dict]:
        """Obtiene una entrada por ID"""
        try:
            result = self.client.table(self.table)\
                .select('*')\
                .eq('id', entry_id)\
                .eq('eliminado', False)\
                .execute()

            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error getting bitácora entry {entry_id}: {e}")
            raise

    def get_all_entries(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Obtiene todas las entradas con filtros opcionales"""
        try:
            query = self.client.table(self.table)\
                .select('*')\
                .eq('eliminado', False)\
                .order('fecha', desc=True)

            # Aplicar filtros si existen
            if filters:
                if 'tipo' in filters:
                    query = query.eq('tipo', filters['tipo'])
                if 'chiste_relacionado_id' in filters:
                    query = query.eq('chiste_relacionado_id', filters['chiste_relacionado_id'])
                if 'limit' in filters:
                    query = query.limit(filters['limit'])

            result = query.execute()
            return result.data
        except Exception as e:
            logger.error(f"Error getting bitácora entries: {e}")
            raise

    def update_entry(self, entry_id: str, updates: Dict[str, Any]) -> Dict:
        """Actualiza una entrada"""
        try:
            result = self.client.table(self.table)\
                .update(updates)\
                .eq('id', entry_id)\
                .execute()

            logger.info(f"Bitácora entry updated: {entry_id}")
            return result.data[0]
        except Exception as e:
            logger.error(f"Error updating bitácora entry {entry_id}: {e}")
            raise

    def delete_entry(self, entry_id: str, soft_delete: bool = True) -> bool:
        """Elimina una entrada (soft delete por defecto)"""
        try:
            if soft_delete:
                self.client.table(self.table)\
                    .update({'eliminado': True})\
                    .eq('id', entry_id)\
                    .execute()
            else:
                self.client.table(self.table)\
                    .delete()\
                    .eq('id', entry_id)\
                    .execute()

            logger.info(f"Bitácora entry deleted: {entry_id} (soft={soft_delete})")
            return True
        except Exception as e:
            logger.error(f"Error deleting bitácora entry {entry_id}: {e}")
            raise


# Instancias globales
jokes_repo = JokesRepository()
analysis_repo = AnalysisRepository()
bitacora_repo = BitacoraRepository()
