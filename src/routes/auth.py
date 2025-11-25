"""
Rutas de autenticación simple
"""
from flask import Blueprint, request, jsonify, session
from src.config import config
import logging
import os

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

# Contraseña de acceso (desde .env)
ACCESS_PASSWORD = os.getenv('ACCESS_PASSWORD', 'metodo2024')


@auth_bp.route('/login', methods=['POST'])
def login():
    """Endpoint de login simple"""
    try:
        data = request.get_json()
        password = data.get('password', '')

        if password == ACCESS_PASSWORD:
            session['authenticated'] = True
            session.permanent = True  # Mantener sesión
            logger.info('Login successful')
            return jsonify({
                'success': True,
                'message': 'Acceso concedido'
            }), 200
        else:
            logger.warning('Login failed - incorrect password')
            return jsonify({
                'success': False,
                'error': 'Contraseña incorrecta'
            }), 401

    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({
            'success': False,
            'error': 'Error en login'
        }), 500


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Cerrar sesión"""
    session.pop('authenticated', None)
    return jsonify({
        'success': True,
        'message': 'Sesión cerrada'
    }), 200


@auth_bp.route('/check', methods=['GET'])
def check_auth():
    """Verificar si está autenticado"""
    is_authenticated = session.get('authenticated', False)
    return jsonify({
        'success': True,
        'authenticated': is_authenticated
    }), 200
