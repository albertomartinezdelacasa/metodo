"""
Rutas para funcionalidades de IA
"""
from flask import Blueprint, request, jsonify
from src.services.ai_agent import ai_agent
from src.services.supabase_client import jokes_repo, analysis_repo
import logging

logger = logging.getLogger(__name__)

ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')


@ai_bp.route('/analyze', methods=['POST'])
def analyze_joke():
    """Analiza un chiste con IA"""
    try:
        data = request.get_json()

        if not data.get('joke_text') and not data.get('joke_id'):
            return jsonify({
                'success': False,
                'error': 'Either joke_text or joke_id is required'
            }), 400

        # Obtener texto del chiste
        if data.get('joke_id'):
            joke = jokes_repo.get_joke(data['joke_id'])
            if not joke:
                return jsonify({
                    'success': False,
                    'error': 'Joke not found'
                }), 404
            joke_text = joke['contenido']
            joke_id = data['joke_id']
        else:
            joke_text = data['joke_text']
            joke_id = None

        # Analizar con IA
        analysis = ai_agent.analyze_joke(joke_text)

        # Si hay joke_id, guardar análisis en BD
        if joke_id and data.get('save', True):
            analysis_data = {
                'chiste_id': joke_id,
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
            saved_analysis = analysis_repo.create_analysis(analysis_data)
            analysis['id'] = saved_analysis['id']

        return jsonify({
            'success': True,
            'data': analysis
        }), 200

    except Exception as e:
        logger.error(f"Error analyzing joke: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ai_bp.route('/improve', methods=['POST'])
def suggest_improvements():
    """Sugiere mejoras para un chiste"""
    try:
        data = request.get_json()

        if not data.get('joke_text'):
            return jsonify({
                'success': False,
                'error': 'joke_text is required'
            }), 400

        joke_text = data['joke_text']
        analysis = data.get('analysis')  # Análisis previo (opcional)

        improvements = ai_agent.suggest_improvements(joke_text, analysis)

        return jsonify({
            'success': True,
            'data': improvements
        }), 200

    except Exception as e:
        logger.error(f"Error suggesting improvements: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ai_bp.route('/variations', methods=['POST'])
def generate_variations():
    """Genera variaciones de un chiste"""
    try:
        data = request.get_json()

        if not data.get('joke_text'):
            return jsonify({
                'success': False,
                'error': 'joke_text is required'
            }), 400

        joke_text = data['joke_text']
        num_variations = data.get('num_variations', 3)

        variations = ai_agent.generate_variations(joke_text, num_variations)

        return jsonify({
            'success': True,
            'data': variations
        }), 200

    except Exception as e:
        logger.error(f"Error generating variations: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ai_bp.route('/brainstorm', methods=['POST'])
def brainstorm_ideas():
    """Genera ideas de chistes sobre un tema"""
    try:
        data = request.get_json()

        if not data.get('topic'):
            return jsonify({
                'success': False,
                'error': 'topic is required'
            }), 400

        topic = data['topic']
        style = data.get('style', 'observacional')
        num_ideas = data.get('num_ideas', 5)

        ideas = ai_agent.brainstorm_ideas(topic, style, num_ideas)

        return jsonify({
            'success': True,
            'data': ideas
        }), 200

    except Exception as e:
        logger.error(f"Error brainstorming ideas: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ai_bp.route('/patterns', methods=['POST'])
def identify_patterns():
    """Identifica patrones en una colección de chistes"""
    try:
        data = request.get_json()

        if not data.get('joke_ids') and not data.get('jokes'):
            return jsonify({
                'success': False,
                'error': 'Either joke_ids or jokes array is required'
            }), 400

        # Obtener chistes
        if data.get('joke_ids'):
            jokes = [jokes_repo.get_joke(jid) for jid in data['joke_ids']]
            jokes = [j for j in jokes if j]  # Filtrar None
        else:
            jokes = data['jokes']

        if len(jokes) < 2:
            return jsonify({
                'success': False,
                'error': 'At least 2 jokes are required for pattern analysis'
            }), 400

        patterns = ai_agent.identify_patterns(jokes)

        return jsonify({
            'success': True,
            'data': patterns
        }), 200

    except Exception as e:
        logger.error(f"Error identifying patterns: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ai_bp.route('/tags', methods=['POST'])
def suggest_tags():
    """Sugiere tags para un chiste"""
    try:
        data = request.get_json()

        if not data.get('joke_text'):
            return jsonify({
                'success': False,
                'error': 'joke_text is required'
            }), 400

        tags = ai_agent.suggest_tags(data['joke_text'])

        return jsonify({
            'success': True,
            'data': tags
        }), 200

    except Exception as e:
        logger.error(f"Error suggesting tags: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ai_bp.route('/analyze-concepts', methods=['POST'])
def analyze_concepts():
    """Analiza en profundidad los conceptos de un chiste"""
    try:
        data = request.get_json()

        if not data.get('joke_text') and not data.get('joke_id'):
            return jsonify({
                'success': False,
                'error': 'Either joke_text or joke_id is required'
            }), 400

        # Obtener texto del chiste
        if data.get('joke_id'):
            joke = jokes_repo.get_joke(data['joke_id'])
            if not joke:
                return jsonify({
                    'success': False,
                    'error': 'Joke not found'
                }), 404
            joke_text = joke['contenido']
            joke_id = data['joke_id']
        else:
            joke_text = data['joke_text']
            joke_id = None

        # Analizar conceptos con IA
        concepts = ai_agent.analyze_concepts(joke_text)

        # Si hay joke_id y se debe guardar, actualizar análisis existente
        if joke_id and data.get('save', True):
            # Obtener el último análisis
            latest_analysis = analysis_repo.get_latest_analysis(joke_id)

            if latest_analysis:
                # Actualizar análisis existente con información de conceptos
                analysis_repo.client.table('analisis_ia').update({
                    'tipo_concepto': concepts.get('tipo_concepto'),
                    'explicacion_tipo_concepto': concepts.get('explicacion_tipo'),
                    'mapa_conceptos': concepts.get('mapa_conceptos')
                }).eq('id', latest_analysis['id']).execute()

                # Actualizar el chiste con el concepto principal
                jokes_repo.update_joke(joke_id, {
                    'concepto': concepts.get('concepto_principal')
                })
            else:
                # Crear nuevo análisis con solo información de conceptos
                analysis_data = {
                    'chiste_id': joke_id,
                    'tipo_concepto': concepts.get('tipo_concepto'),
                    'explicacion_tipo_concepto': concepts.get('explicacion_tipo'),
                    'mapa_conceptos': concepts.get('mapa_conceptos')
                }
                analysis_repo.create_analysis(analysis_data)

                # Actualizar el chiste
                jokes_repo.update_joke(joke_id, {
                    'concepto': concepts.get('concepto_principal')
                })

        return jsonify({
            'success': True,
            'data': concepts
        }), 200

    except Exception as e:
        logger.error(f"Error analyzing concepts: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ai_bp.route('/analyze-rupture', methods=['POST'])
def analyze_rupture():
    """Analiza la mecánica de ruptura de un chiste"""
    try:
        data = request.get_json()

        if not data.get('joke_text') and not data.get('joke_id'):
            return jsonify({
                'success': False,
                'error': 'Either joke_text or joke_id is required'
            }), 400

        # Obtener texto del chiste
        if data.get('joke_id'):
            joke = jokes_repo.get_joke(data['joke_id'])
            if not joke:
                return jsonify({
                    'success': False,
                    'error': 'Joke not found'
                }), 404
            joke_text = joke['contenido']
            joke_id = data['joke_id']
        else:
            joke_text = data['joke_text']
            joke_id = None

        # Analizar ruptura con IA
        rupture = ai_agent.analyze_rupture(joke_text)

        # Si hay joke_id y se debe guardar, actualizar análisis existente
        if joke_id and data.get('save', True):
            # Obtener el último análisis
            latest_analysis = analysis_repo.get_latest_analysis(joke_id)

            if latest_analysis:
                # Actualizar análisis existente con información de ruptura
                analysis_repo.client.table('analisis_ia').update({
                    'tipo_ruptura': rupture.get('tipo_ruptura'),
                    'subtipo_ruptura': rupture.get('subtipo_ruptura'),
                    'explicacion_ruptura': rupture.get('explicacion_ruptura')
                }).eq('id', latest_analysis['id']).execute()
            else:
                # Crear nuevo análisis con solo información de ruptura
                analysis_data = {
                    'chiste_id': joke_id,
                    'tipo_ruptura': rupture.get('tipo_ruptura'),
                    'subtipo_ruptura': rupture.get('subtipo_ruptura'),
                    'explicacion_ruptura': rupture.get('explicacion_ruptura')
                }
                analysis_repo.create_analysis(analysis_data)

        return jsonify({
            'success': True,
            'data': rupture
        }), 200

    except Exception as e:
        logger.error(f"Error analyzing rupture: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
