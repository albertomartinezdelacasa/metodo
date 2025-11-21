"""
Agente de IA para análisis de chistes usando Google Gemini
"""
import google.generativeai as genai
from src.config import config
from src.utils.prompts import (
    ANALYZE_JOKE_PROMPT,
    SUGGEST_IMPROVEMENTS_PROMPT,
    GENERATE_VARIATIONS_PROMPT,
    BRAINSTORM_IDEAS_PROMPT,
    IDENTIFY_PATTERNS_PROMPT,
    TAG_SUGGESTION_PROMPT,
    ANALYZE_CONCEPTS_PROMPT,
    ANALYZE_RUPTURE_PROMPT
)
import json
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class ComedyAIAgent:
    """Agente de IA para análisis y mejora de chistes usando Google Gemini"""

    def __init__(self):
        """Inicializa el agente de IA con Google Gemini"""
        if not config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not configured")

        genai.configure(api_key=config.GEMINI_API_KEY)

        # Configuración del modelo
        self.generation_config = {
            "temperature": 0.9,  # Creatividad alta para comedia
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }

        self.model = genai.GenerativeModel(
            model_name=config.GEMINI_MODEL,
            generation_config=self.generation_config,
        )

        logger.info(f"AI Agent initialized with model: {config.GEMINI_MODEL}")

    def _parse_json_response(self, response_text: str) -> Dict:
        """Parsea la respuesta JSON del modelo"""
        try:
            # Limpiar el texto de posibles markdown code blocks
            cleaned = response_text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]

            cleaned = cleaned.strip()
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON response: {e}\nResponse: {response_text}")
            raise ValueError(f"Invalid JSON response from AI: {e}")

    def analyze_joke(self, joke_text: str) -> Dict:
        """
        Analiza la estructura y técnicas de un chiste

        Args:
            joke_text: Texto del chiste a analizar

        Returns:
            Dict con el análisis estructurado
        """
        try:
            prompt = ANALYZE_JOKE_PROMPT.format(joke_text=joke_text)
            response = self.model.generate_content(prompt)

            analysis = self._parse_json_response(response.text)
            logger.info(f"Joke analyzed successfully. Score: {analysis['scores']['general']}")

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing joke: {e}")
            raise

    def suggest_improvements(self, joke_text: str, analysis: Optional[Dict] = None) -> Dict:
        """
        Sugiere mejoras para un chiste

        Args:
            joke_text: Texto del chiste
            analysis: Análisis previo del chiste (opcional)

        Returns:
            Dict con versiones mejoradas
        """
        try:
            # Si no hay análisis, generar uno primero
            if not analysis:
                analysis = self.analyze_joke(joke_text)

            # Crear resumen del análisis
            analysis_summary = f"""
Puntos fuertes: {', '.join(analysis.get('puntos_fuertes', []))}
Puntos débiles: {', '.join(analysis.get('puntos_debiles', []))}
Técnicas: {', '.join(analysis.get('tecnicas', []))}
Scores: {json.dumps(analysis.get('scores', {}))}
"""

            prompt = SUGGEST_IMPROVEMENTS_PROMPT.format(
                joke_text=joke_text,
                analysis_summary=analysis_summary
            )

            response = self.model.generate_content(prompt)
            improvements = self._parse_json_response(response.text)

            logger.info("Improvements suggested successfully")
            return improvements

        except Exception as e:
            logger.error(f"Error suggesting improvements: {e}")
            raise

    def generate_variations(self, joke_text: str, num_variations: int = 3) -> List[Dict]:
        """
        Genera variaciones del chiste

        Args:
            joke_text: Texto del chiste original
            num_variations: Número de variaciones a generar

        Returns:
            Lista de variaciones
        """
        try:
            prompt = GENERATE_VARIATIONS_PROMPT.format(
                joke_text=joke_text,
                num_variations=num_variations
            )

            response = self.model.generate_content(prompt)
            result = self._parse_json_response(response.text)

            variations = result.get('variaciones', [])
            logger.info(f"Generated {len(variations)} variations")

            return variations

        except Exception as e:
            logger.error(f"Error generating variations: {e}")
            raise

    def brainstorm_ideas(self, topic: str, style: str = "observacional",
                        num_ideas: int = 5) -> List[Dict]:
        """
        Genera ideas de chistes sobre un tema

        Args:
            topic: Tema sobre el que generar ideas
            style: Estilo de humor preferido
            num_ideas: Número de ideas a generar

        Returns:
            Lista de ideas de chistes
        """
        try:
            prompt = BRAINSTORM_IDEAS_PROMPT.format(
                topic=topic,
                style=style,
                num_ideas=num_ideas
            )

            response = self.model.generate_content(prompt)
            result = self._parse_json_response(response.text)

            ideas = result.get('ideas', [])
            logger.info(f"Generated {len(ideas)} ideas about: {topic}")

            return ideas

        except Exception as e:
            logger.error(f"Error brainstorming ideas: {e}")
            raise

    def identify_patterns(self, jokes: List[Dict]) -> Dict:
        """
        Identifica patrones en una colección de chistes

        Args:
            jokes: Lista de diccionarios con chistes (debe tener campo 'contenido')

        Returns:
            Dict con patrones identificados
        """
        try:
            # Construir texto con todos los chistes
            jokes_text = "\n\n---\n\n".join([
                f"CHISTE {i+1}:\n{joke.get('contenido', joke.get('texto', ''))}"
                for i, joke in enumerate(jokes)
            ])

            prompt = IDENTIFY_PATTERNS_PROMPT.format(
                num_jokes=len(jokes),
                jokes_text=jokes_text
            )

            response = self.model.generate_content(prompt)
            patterns = self._parse_json_response(response.text)

            logger.info(f"Patterns identified from {len(jokes)} jokes")
            return patterns

        except Exception as e:
            logger.error(f"Error identifying patterns: {e}")
            raise

    def suggest_tags(self, joke_text: str) -> Dict:
        """
        Sugiere tags para categorizar un chiste

        Args:
            joke_text: Texto del chiste

        Returns:
            Dict con tags sugeridos por categoría
        """
        try:
            prompt = TAG_SUGGESTION_PROMPT.format(joke_text=joke_text)
            response = self.model.generate_content(prompt)

            tags = self._parse_json_response(response.text)
            logger.info("Tags suggested successfully")

            return tags

        except Exception as e:
            logger.error(f"Error suggesting tags: {e}")
            raise

    def analyze_concepts(self, joke_text: str) -> Dict:
        """
        Analiza en profundidad los conceptos del chiste

        Args:
            joke_text: Texto del chiste a analizar

        Returns:
            Dict con análisis conceptual detallado:
            - concepto_principal: El concepto central
            - tipo_concepto: simple/compuesto/concreto/abstracto
            - explicacion_tipo: Por qué es ese tipo
            - mapa_conceptos: Mapa de asociaciones conceptuales
            - ejemplos_similares: Ejemplos de estructura similar
            - potencial_expansion: Cómo explotar más el concepto
        """
        try:
            prompt = ANALYZE_CONCEPTS_PROMPT.format(joke_text=joke_text)
            response = self.model.generate_content(prompt)

            concepts = self._parse_json_response(response.text)
            logger.info(f"Concepts analyzed. Type: {concepts.get('tipo_concepto', 'unknown')}")

            return concepts

        except Exception as e:
            logger.error(f"Error analyzing concepts: {e}")
            raise

    def analyze_rupture(self, joke_text: str) -> Dict:
        """
        Analiza la mecánica de ruptura humorística del chiste

        Args:
            joke_text: Texto del chiste a analizar

        Returns:
            Dict con análisis de la ruptura:
            - tipo_ruptura: Tipo principal de ruptura
            - subtipo_ruptura: Subtipo específico
            - explicacion_ruptura: Cómo funciona el mecanismo
            - expectativa_creada: Qué expectativa crea el setup
            - momento_ruptura: Punto exacto de la ruptura
            - efecto_logrado: Efecto humorístico conseguido
            - intensidad_ruptura: suave/moderada/fuerte
            - mejoras_posibles: Cómo intensificar
            - ejemplos_similares: Ejemplos del mismo tipo
        """
        try:
            prompt = ANALYZE_RUPTURE_PROMPT.format(joke_text=joke_text)
            response = self.model.generate_content(prompt)

            rupture = self._parse_json_response(response.text)
            logger.info(f"Rupture analyzed. Type: {rupture.get('tipo_ruptura', 'unknown')}")

            return rupture

        except Exception as e:
            logger.error(f"Error analyzing rupture: {e}")
            raise


# Instancia global del agente
ai_agent = ComedyAIAgent() if config.GEMINI_API_KEY else None
