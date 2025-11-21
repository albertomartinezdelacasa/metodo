"""
Rutas para gestión de chistes (CRUD)
"""
from flask import Blueprint, request, jsonify
from src.services.supabase_client import jokes_repo
from src.services.ai_agent import ai_agent
import logging

logger = logging.getLogger(__name__)

jokes_bp = Blueprint('jokes', __name__, url_prefix='/api/jokes')


@jokes_bp.route('/', methods=['GET'])
def get_all_jokes():
    """Obtiene todos los chistes con filtros opcionales"""
    try:
        filters = {}

        # Filtros opcionales
        if request.args.get('estado'):
            filters['estado'] = request.args.get('estado')
        if request.args.get('calificacion_min'):
            filters['calificacion_min'] = int(request.args.get('calificacion_min'))

        jokes = jokes_repo.get_all_jokes(filters)

        return jsonify({
            'success': True,
            'data': jokes,
            'count': len(jokes)
        }), 200

    except Exception as e:
        logger.error(f"Error getting jokes: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@jokes_bp.route('/<joke_id>', methods=['GET'])
def get_joke(joke_id):
    """Obtiene un chiste específico"""
    try:
        joke = jokes_repo.get_joke(joke_id)

        if not joke:
            return jsonify({
                'success': False,
                'error': 'Joke not found'
            }), 404

        return jsonify({
            'success': True,
            'data': joke
        }), 200

    except Exception as e:
        logger.error(f"Error getting joke {joke_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@jokes_bp.route('/', methods=['POST'])
def create_joke():
    """Crea un nuevo chiste"""
    try:
        data = request.get_json()

        # Validación
        if not data.get('contenido'):
            return jsonify({
                'success': False,
                'error': 'Content is required'
            }), 400

        # Preparar datos
        joke_data = {
            'titulo': data.get('titulo', ''),
            'contenido': data['contenido'],
            'estado': data.get('estado', 'borrador'),
            'calificacion': data.get('calificacion'),
            'notas': data.get('notas', '')
        }

        # Crear chiste
        joke = jokes_repo.create_joke(joke_data)

        # Auto-analizar con IA si está disponible
        if ai_agent and data.get('auto_analyze', False):
            try:
                from src.services.supabase_client import analysis_repo
                analysis = ai_agent.analyze_joke(joke['contenido'])

                # Guardar análisis
                analysis_data = {
                    'chiste_id': joke['id'],
                    'estructura': analysis.get('estructura'),
                    'tecnicas': analysis.get('tecnicas'),
                    'puntos_fuertes': analysis.get('puntos_fuertes'),
                    'puntos_debiles': analysis.get('puntos_debiles'),
                    'sugerencias': analysis.get('sugerencias'),
                    'puntuacion_estructura': analysis['scores'].get('estructura'),
                    'puntuacion_originalidad': analysis['scores'].get('originalidad'),
                    'puntuacion_timing': analysis['scores'].get('timing'),
                    'puntuacion_general': analysis['scores'].get('general')
                }
                analysis_repo.create_analysis(analysis_data)

                joke['auto_analysis'] = analysis

            except Exception as e:
                logger.warning(f"Auto-analysis failed: {e}")

        return jsonify({
            'success': True,
            'data': joke
        }), 201

    except Exception as e:
        logger.error(f"Error creating joke: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@jokes_bp.route('/<joke_id>', methods=['PUT'])
def update_joke(joke_id):
    """Actualiza un chiste existente"""
    try:
        data = request.get_json()

        # Campos actualizables
        updates = {}
        for field in ['titulo', 'contenido', 'estado', 'calificacion', 'notas', 'reaccion_audiencia']:
            if field in data:
                updates[field] = data[field]

        if not updates:
            return jsonify({
                'success': False,
                'error': 'No fields to update'
            }), 400

        joke = jokes_repo.update_joke(joke_id, updates)

        return jsonify({
            'success': True,
            'data': joke
        }), 200

    except Exception as e:
        logger.error(f"Error updating joke {joke_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@jokes_bp.route('/<joke_id>', methods=['DELETE'])
def delete_joke(joke_id):
    """Elimina un chiste (soft delete)"""
    try:
        soft_delete = request.args.get('soft', 'true').lower() == 'true'
        jokes_repo.delete_joke(joke_id, soft_delete=soft_delete)

        return jsonify({
            'success': True,
            'message': 'Joke deleted successfully'
        }), 200

    except Exception as e:
        logger.error(f"Error deleting joke {joke_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@jokes_bp.route('/<joke_id>/use', methods=['POST'])
def mark_as_used(joke_id):
    """Marca un chiste como usado (incrementa contador)"""
    try:
        joke = jokes_repo.increment_usage(joke_id)

        return jsonify({
            'success': True,
            'data': joke,
            'message': f"Usage count: {joke['veces_usado']}"
        }), 200

    except Exception as e:
        logger.error(f"Error marking joke {joke_id} as used: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
