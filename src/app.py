"""
Aplicación Flask principal - Método Comedia
"""
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from src.config import config
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app():
    """Factory function para crear la aplicación Flask"""

    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static')

    # Configuración
    app.config.from_object(config)

    # CORS
    CORS(app, origins=config.CORS_ORIGINS)

    # Validar configuración
    try:
        config.validate()
        logger.info("Configuration validated successfully")
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise

    # Registrar blueprints
    from src.routes.jokes import jokes_bp
    from src.routes.ai import ai_bp
    from src.routes.bitacora import bitacora_bp
    from src.routes.analisis_chistes import analisis_chistes_bp
    from src.routes.categorias import categorias_bp

    app.register_blueprint(jokes_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(bitacora_bp)
    app.register_blueprint(analisis_chistes_bp, url_prefix='/api/analisis-chistes')
    app.register_blueprint(categorias_bp, url_prefix='/api/categorias')

    # Rutas básicas
    @app.route('/')
    def index():
        """Página principal"""
        return render_template('index.html')

    @app.route('/health')
    def health():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'service': 'metodo-comedia',
            'version': '1.0.0'
        }), 200

    @app.route('/manifest.json')
    def manifest():
        """PWA manifest"""
        from flask import send_from_directory
        return send_from_directory('../static', 'manifest.json')

    @app.route('/service-worker.js')
    def service_worker():
        """PWA service worker"""
        from flask import send_from_directory
        return send_from_directory('../static', 'service-worker.js')

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'Resource not found'
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal error: {error}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

    logger.info("Flask app created successfully")
    return app


# Crear instancia de la app
app = create_app()


if __name__ == '__main__':
    port = config.PORT
    debug = config.DEBUG

    logger.info(f"Starting server on port {port} (debug={debug})")
    app.run(host='0.0.0.0', port=port, debug=debug)
