"""
Rutas para funcionalidades de bitácora/diario
"""
from flask import Blueprint, request, jsonify
from src.services.supabase_client import bitacora_repo
import logging

logger = logging.getLogger(__name__)

bitacora_bp = Blueprint('bitacora', __name__, url_prefix='/api/bitacora')


@bitacora_bp.route('/', methods=['GET'])
def get_entries():
    """Obtiene todas las entradas de bitácora con filtros opcionales"""
    try:
        filters = {}

        # Filtros opcionales
        if request.args.get('tipo'):
            filters['tipo'] = request.args.get('tipo')

        if request.args.get('chiste_relacionado_id'):
            filters['chiste_relacionado_id'] = request.args.get('chiste_relacionado_id')

        if request.args.get('limit'):
            filters['limit'] = int(request.args.get('limit'))

        entries = bitacora_repo.get_all_entries(filters)

        return jsonify({
            'success': True,
            'data': entries,
            'count': len(entries)
        }), 200

    except Exception as e:
        logger.error(f"Error getting bitácora entries: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bitacora_bp.route('/<entry_id>', methods=['GET'])
def get_entry(entry_id):
    """Obtiene una entrada específica"""
    try:
        entry = bitacora_repo.get_entry(entry_id)

        if not entry:
            return jsonify({
                'success': False,
                'error': 'Entry not found'
            }), 404

        return jsonify({
            'success': True,
            'data': entry
        }), 200

    except Exception as e:
        logger.error(f"Error getting bitácora entry {entry_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bitacora_bp.route('/', methods=['POST'])
def create_entry():
    """Crea una nueva entrada de bitácora"""
    try:
        data = request.get_json()

        # Validar campos requeridos
        if not data.get('contenido'):
            return jsonify({
                'success': False,
                'error': 'contenido is required'
            }), 400

        # Construir datos de la entrada
        entry_data = {
            'contenido': data['contenido'],
            'tipo': data.get('tipo', 'nota_general'),
            'titulo': data.get('titulo'),
            'estado_animo': data.get('estado_animo'),
            'tags': data.get('tags', []),
            'chiste_relacionado_id': data.get('chiste_relacionado_id'),
            'presentacion_relacionada_id': data.get('presentacion_relacionada_id')
        }

        # Crear entrada
        entry = bitacora_repo.create_entry(entry_data)

        return jsonify({
            'success': True,
            'data': entry
        }), 201

    except Exception as e:
        logger.error(f"Error creating bitácora entry: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bitacora_bp.route('/<entry_id>', methods=['PUT'])
def update_entry(entry_id):
    """Actualiza una entrada existente"""
    try:
        data = request.get_json()

        # Verificar que la entrada existe
        existing = bitacora_repo.get_entry(entry_id)
        if not existing:
            return jsonify({
                'success': False,
                'error': 'Entry not found'
            }), 404

        # Campos permitidos para actualizar
        allowed_fields = [
            'contenido', 'tipo', 'titulo', 'estado_animo',
            'tags', 'chiste_relacionado_id', 'presentacion_relacionada_id'
        ]

        updates = {k: v for k, v in data.items() if k in allowed_fields}

        if not updates:
            return jsonify({
                'success': False,
                'error': 'No valid fields to update'
            }), 400

        # Actualizar entrada
        updated_entry = bitacora_repo.update_entry(entry_id, updates)

        return jsonify({
            'success': True,
            'data': updated_entry
        }), 200

    except Exception as e:
        logger.error(f"Error updating bitácora entry {entry_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bitacora_bp.route('/<entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    """Elimina una entrada (soft delete por defecto)"""
    try:
        # Verificar que la entrada existe
        existing = bitacora_repo.get_entry(entry_id)
        if not existing:
            return jsonify({
                'success': False,
                'error': 'Entry not found'
            }), 404

        # Eliminar (soft delete)
        bitacora_repo.delete_entry(entry_id, soft_delete=True)

        return jsonify({
            'success': True,
            'message': 'Entry deleted successfully'
        }), 200

    except Exception as e:
        logger.error(f"Error deleting bitácora entry {entry_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
