"""
Configuración de la aplicación
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class Config:
    """Configuración base de la aplicación"""

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    PORT = int(os.getenv('PORT', 5000))

    # Supabase
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

    # AI Provider (groq or gemini)
    AI_PROVIDER = os.getenv('AI_PROVIDER', 'groq')

    # Groq AI
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GROQ_MODEL = 'llama-3.3-70b-versatile'  # Modelo gratuito y potente

    # Google Gemini AI (backup)
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = 'gemini-1.5-flash'

    # Todoist
    TODOIST_TOKEN = os.getenv('TODOIST_TOKEN')
    TODOIST_PROJECT_ID = os.getenv('TODOIST_PROJECT_ID', '2362882414')

    # Obsidian
    OBSIDIAN_VAULT_PATH = os.getenv('OBSIDIAN_VAULT_PATH', './exports')

    # CORS
    CORS_ORIGINS = [
        'http://localhost:5000',
        'http://127.0.0.1:5000',
        'https://*.onrender.com'
    ]

    @classmethod
    def validate(cls):
        """Valida que las variables de entorno críticas estén configuradas"""
        required = {
            'SUPABASE_URL': cls.SUPABASE_URL,
            'SUPABASE_KEY': cls.SUPABASE_KEY,
        }

        missing = [key for key, value in required.items() if not value]

        # Check AI provider
        if cls.AI_PROVIDER == 'groq' and not cls.GROQ_API_KEY:
            missing.append('GROQ_API_KEY')
        elif cls.AI_PROVIDER == 'gemini' and not cls.GEMINI_API_KEY:
            missing.append('GEMINI_API_KEY')
        elif not cls.GROQ_API_KEY and not cls.GEMINI_API_KEY:
            missing.append('GROQ_API_KEY o GEMINI_API_KEY')

        if missing:
            raise ValueError(
                f"Faltan variables de entorno requeridas: {', '.join(missing)}\n"
                "Copia .env.example a .env y configura los valores."
            )

        return True


# Instancia de configuración
config = Config()
