"""
Rutas para gestión de categorías dinámicas
"""
from flask import Blueprint, request, jsonify
from src.services.supabase_client import categorias_repo
import logging

logger = logging.getLogger(__name__)

categorias_bp = Blueprint('categorias', __name__)


@categorias_bp.route('/<tipo>', methods=['GET'])
def get_categorias(tipo):
    """
    Obtiene todas las categorías de un tipo específico
    Tipos válidos: perspectiva, actitud, concepto, formulacion
    """
    try:
        # Validar tipo
        valid_tipos = ['perspectiva', 'actitud', 'concepto', 'formulacion']
        if tipo not in valid_tipos:
            return jsonify({
                'success': False,
                'error': f'Tipo inválido. Debe ser uno de: {", ".join(valid_tipos)}'
            }), 400

        categorias = categorias_repo.get_categorias_by_tipo(tipo)

        return jsonify({
            'success': True,
            'data': categorias,
            'count': len(categorias)
        }), 200

    except Exception as e:
        logger.error(f"Error getting categorías for tipo {tipo}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@categorias_bp.route('/', methods=['POST'])
def create_categoria():
    """Crea una nueva categoría"""
    try:
        data = request.get_json()

        # Validar campos requeridos
        if not data.get('tipo') or not data.get('valor'):
            return jsonify({
                'success': False,
                'error': 'Tipo y valor son obligatorios'
            }), 400

        # Validar tipo
        valid_tipos = ['perspectiva', 'actitud', 'concepto', 'formulacion']
        if data['tipo'] not in valid_tipos:
            return jsonify({
                'success': False,
                'error': f'Tipo inválido. Debe ser uno de: {", ".join(valid_tipos)}'
            }), 400

        # Crear categoría
        categoria = categorias_repo.create_categoria(
            tipo=data['tipo'],
            valor=data['valor'],
            orden=data.get('orden', 0)
        )

        return jsonify({
            'success': True,
            'data': categoria,
            'message': 'Categoría creada exitosamente'
        }), 201

    except Exception as e:
        logger.error(f"Error creating categoría: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@categorias_bp.route('/<categoria_id>', methods=['DELETE'])
def delete_categoria(categoria_id):
    """Elimina una categoría (solo si fue creada por usuario)"""
    try:
        categorias_repo.delete_categoria(categoria_id)

        return jsonify({
            'success': True,
            'message': 'Categoría eliminada exitosamente'
        }), 200

    except Exception as e:
        logger.error(f"Error deleting categoría {categoria_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@categorias_bp.route('/all', methods=['GET'])
def get_all_categorias():
    """Obtiene todas las categorías agrupadas por tipo"""
    try:
        tipos = ['perspectiva', 'actitud', 'concepto', 'formulacion']
        result = {}

        for tipo in tipos:
            categorias = categorias_repo.get_categorias_by_tipo(tipo)
            result[tipo] = categorias

        return jsonify({
            'success': True,
            'data': result
        }), 200

    except Exception as e:
        logger.error(f"Error getting all categorías: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
