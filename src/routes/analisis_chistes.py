"""
Rutas para gestión de análisis de chistes de otros comediantes
"""
from flask import Blueprint, request, jsonify
from src.services.supabase_client import analisis_chistes_repo
import logging

logger = logging.getLogger(__name__)

analisis_chistes_bp = Blueprint('analisis_chistes', __name__)


@analisis_chistes_bp.route('/', methods=['GET'])
def get_all_analisis():
    """Obtiene todos los análisis con filtros opcionales"""
    try:
        filters = {}

        # Obtener parámetros de query
        if request.args.get('comediante'):
            filters['comediante'] = request.args.get('comediante')
        if request.args.get('concepto_categoria'):
            filters['concepto_categoria'] = request.args.get('concepto_categoria')
        if request.args.get('perspectiva_categoria'):
            filters['perspectiva_categoria'] = request.args.get('perspectiva_categoria')
        if request.args.get('limit'):
            filters['limit'] = int(request.args.get('limit'))

        analisis_list = analisis_chistes_repo.get_all_analisis(filters if filters else None)

        return jsonify({
            'success': True,
            'data': analisis_list,
            'count': len(analisis_list)
        }), 200

    except Exception as e:
        logger.error(f"Error getting análisis: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@analisis_chistes_bp.route('/<analisis_id>', methods=['GET'])
def get_analisis(analisis_id):
    """Obtiene un análisis específico por ID"""
    try:
        analisis = analisis_chistes_repo.get_analisis(analisis_id)

        if not analisis:
            return jsonify({
                'success': False,
                'error': 'Análisis no encontrado'
            }), 404

        return jsonify({
            'success': True,
            'data': analisis
        }), 200

    except Exception as e:
        logger.error(f"Error getting análisis {analisis_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@analisis_chistes_bp.route('/', methods=['POST'])
def create_analisis():
    """Crea un nuevo análisis de chiste"""
    try:
        data = request.get_json()

        # Validar campos requeridos
        if not data.get('premisa') or not data.get('ruptura') or not data.get('remate'):
            return jsonify({
                'success': False,
                'error': 'Premisa, ruptura y remate son obligatorios'
            }), 400

        # Crear el análisis
        analisis = analisis_chistes_repo.create_analisis(data)

        return jsonify({
            'success': True,
            'data': analisis,
            'message': 'Análisis creado exitosamente'
        }), 201

    except Exception as e:
        logger.error(f"Error creating análisis: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@analisis_chistes_bp.route('/<analisis_id>', methods=['PUT'])
def update_analisis(analisis_id):
    """Actualiza un análisis existente"""
    try:
        data = request.get_json()

        # Verificar que el análisis existe
        existing = analisis_chistes_repo.get_analisis(analisis_id)
        if not existing:
            return jsonify({
                'success': False,
                'error': 'Análisis no encontrado'
            }), 404

        # Actualizar
        analisis = analisis_chistes_repo.update_analisis(analisis_id, data)

        return jsonify({
            'success': True,
            'data': analisis,
            'message': 'Análisis actualizado exitosamente'
        }), 200

    except Exception as e:
        logger.error(f"Error updating análisis {analisis_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@analisis_chistes_bp.route('/<analisis_id>', methods=['DELETE'])
def delete_analisis(analisis_id):
    """Elimina un análisis (soft delete)"""
    try:
        # Verificar que el análisis existe
        existing = analisis_chistes_repo.get_analisis(analisis_id)
        if not existing:
            return jsonify({
                'success': False,
                'error': 'Análisis no encontrado'
            }), 404

        # Eliminar (soft delete)
        analisis_chistes_repo.delete_analisis(analisis_id, soft_delete=True)

        return jsonify({
            'success': True,
            'message': 'Análisis eliminado exitosamente'
        }), 200

    except Exception as e:
        logger.error(f"Error deleting análisis {analisis_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@analisis_chistes_bp.route('/similar', methods=['POST'])
def search_similar():
    """Busca análisis similares basados en categorías"""
    try:
        data = request.get_json()

        concepto_categoria = data.get('concepto_categoria')
        perspectiva_categoria = data.get('perspectiva_categoria')
        formulacion_categoria = data.get('formulacion_categoria')
        limit = data.get('limit', 10)

        # Buscar similares
        similar = analisis_chistes_repo.search_similar(
            concepto_categoria=concepto_categoria,
            perspectiva_categoria=perspectiva_categoria,
            formulacion_categoria=formulacion_categoria,
            limit=limit
        )

        return jsonify({
            'success': True,
            'data': similar,
            'count': len(similar)
        }), 200

    except Exception as e:
        logger.error(f"Error searching similar análisis: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
