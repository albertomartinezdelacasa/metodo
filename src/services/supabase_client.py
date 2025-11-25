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


class AnalisisChistesRepository:
    """Repositorio para gestionar análisis de chistes de otros comediantes"""

    def __init__(self):
        self.client = SupabaseClient.get_client()
        self.table = 'analisis_chistes'

    def create_analisis(self, analisis_data: Dict[str, Any]) -> Dict:
        """Crea un nuevo análisis de chiste"""
        try:
            result = self.client.table(self.table).insert(analisis_data).execute()
            logger.info(f"Análisis de chiste created: {result.data[0]['id']}")
            return result.data[0]
        except Exception as e:
            logger.error(f"Error creating análisis de chiste: {e}")
            raise

    def get_analisis(self, analisis_id: str) -> Optional[Dict]:
        """Obtiene un análisis por ID"""
        try:
            result = self.client.table(self.table)\
                .select('*')\
                .eq('id', analisis_id)\
                .eq('eliminado', False)\
                .execute()

            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error getting análisis {analisis_id}: {e}")
            raise

    def get_all_analisis(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Obtiene todos los análisis con filtros opcionales"""
        try:
            query = self.client.table(self.table)\
                .select('*')\
                .eq('eliminado', False)\
                .order('fecha_creacion', desc=True)

            # Aplicar filtros si existen
            if filters:
                if 'comediante' in filters:
                    query = query.ilike('comediante', f"%{filters['comediante']}%")
                if 'concepto_categoria' in filters:
                    query = query.eq('concepto_categoria', filters['concepto_categoria'])
                if 'perspectiva_categoria' in filters:
                    query = query.eq('perspectiva_categoria', filters['perspectiva_categoria'])
                if 'limit' in filters:
                    query = query.limit(filters['limit'])

            result = query.execute()
            return result.data
        except Exception as e:
            logger.error(f"Error getting análisis: {e}")
            raise

    def update_analisis(self, analisis_id: str, updates: Dict[str, Any]) -> Dict:
        """Actualiza un análisis"""
        try:
            result = self.client.table(self.table)\
                .update(updates)\
                .eq('id', analisis_id)\
                .execute()

            logger.info(f"Análisis updated: {analisis_id}")
            return result.data[0]
        except Exception as e:
            logger.error(f"Error updating análisis {analisis_id}: {e}")
            raise

    def delete_analisis(self, analisis_id: str, soft_delete: bool = True) -> bool:
        """Elimina un análisis (soft delete por defecto)"""
        try:
            if soft_delete:
                self.client.table(self.table)\
                    .update({'eliminado': True})\
                    .eq('id', analisis_id)\
                    .execute()
            else:
                self.client.table(self.table)\
                    .delete()\
                    .eq('id', analisis_id)\
                    .execute()

            logger.info(f"Análisis deleted: {analisis_id} (soft={soft_delete})")
            return True
        except Exception as e:
            logger.error(f"Error deleting análisis {analisis_id}: {e}")
            raise

    def search_similar(self, concepto_categoria: str = None, perspectiva_categoria: str = None,
                       formulacion_categoria: str = None, limit: int = 10) -> List[Dict]:
        """Busca análisis similares basados en categorías"""
        try:
            query = self.client.table(self.table)\
                .select('*')\
                .eq('eliminado', False)

            if concepto_categoria:
                query = query.eq('concepto_categoria', concepto_categoria)
            if perspectiva_categoria:
                query = query.eq('perspectiva_categoria', perspectiva_categoria)
            if formulacion_categoria:
                query = query.eq('formulacion_categoria', formulacion_categoria)

            result = query.order('fecha_creacion', desc=True).limit(limit).execute()
            return result.data
        except Exception as e:
            logger.error(f"Error searching similar análisis: {e}")
            raise


class CategoriasRepository:
    """Repositorio para gestionar categorías dinámicas"""

    def __init__(self):
        self.client = SupabaseClient.get_client()
        self.table = 'categorias_dinamicas'

    def get_categorias_by_tipo(self, tipo: str) -> List[Dict]:
        """Obtiene todas las categorías de un tipo específico"""
        try:
            result = self.client.table(self.table)\
                .select('*')\
                .eq('tipo', tipo)\
                .order('orden')\
                .execute()

            return result.data
        except Exception as e:
            logger.error(f"Error getting categorías for tipo {tipo}: {e}")
            raise

    def create_categoria(self, tipo: str, valor: str, orden: int = 0) -> Dict:
        """Crea una nueva categoría"""
        try:
            result = self.client.table(self.table).insert({
                'tipo': tipo,
                'valor': valor,
                'usuario_creado': True,
                'orden': orden
            }).execute()

            logger.info(f"Categoría created: {tipo} - {valor}")
            return result.data[0]
        except Exception as e:
            # Si ya existe (violación de UNIQUE constraint), retornar la existente
            if 'duplicate key' in str(e).lower():
                result = self.client.table(self.table)\
                    .select('*')\
                    .eq('tipo', tipo)\
                    .eq('valor', valor)\
                    .execute()
                return result.data[0] if result.data else None

            logger.error(f"Error creating categoría: {e}")
            raise

    def delete_categoria(self, categoria_id: str) -> bool:
        """Elimina una categoría (solo si fue creada por usuario)"""
        try:
            self.client.table(self.table)\
                .delete()\
                .eq('id', categoria_id)\
                .eq('usuario_creado', True)\
                .execute()

            logger.info(f"Categoría deleted: {categoria_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting categoría {categoria_id}: {e}")
            raise


# Instancias globales
jokes_repo = JokesRepository()
analysis_repo = AnalysisRepository()
bitacora_repo = BitacoraRepository()
analisis_chistes_repo = AnalisisChistesRepository()
categorias_repo = CategoriasRepository()
