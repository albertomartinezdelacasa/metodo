"""
Agente de IA para análisis de chistes - Soporta Groq y Gemini
"""
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
import requests
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class ComedyAIAgent:
    """Agente de IA para análisis y mejora de chistes - Soporta múltiples proveedores"""

    def __init__(self):
        """Inicializa el agente de IA con el proveedor configurado"""
        self.provider = config.AI_PROVIDER

        if self.provider == 'groq':
            if not config.GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY not configured")
            self.api_key = config.GROQ_API_KEY
            self.model = config.GROQ_MODEL
            self.api_url = "https://api.groq.com/openai/v1/chat/completions"
            logger.info(f"AI Agent initialized with Groq model: {self.model}")

        elif self.provider == 'gemini':
            if not config.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY not configured")
            import google.generativeai as genai
            genai.configure(api_key=config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(
                model_name=config.GEMINI_MODEL,
                generation_config={
                    "temperature": 0.9,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 2048,
                }
            )
            logger.info(f"AI Agent initialized with Gemini model: {config.GEMINI_MODEL}")
        else:
            raise ValueError(f"Unknown AI provider: {self.provider}")

    def _call_groq(self, prompt: str) -> str:
        """Llama a la API de Groq"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "Eres un experto en comedia stand-up y análisis humorístico. Responde siempre en JSON válido."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.9,
            "max_tokens": 2048
        }

        response = requests.post(self.api_url, headers=headers, json=data, timeout=60)
        response.raise_for_status()

        result = response.json()
        return result['choices'][0]['message']['content']

    def _call_gemini(self, prompt: str) -> str:
        """Llama a la API de Gemini"""
        response = self.model.generate_content(prompt)
        return response.text

    def _generate(self, prompt: str) -> str:
        """Genera respuesta usando el proveedor configurado"""
        if self.provider == 'groq':
            return self._call_groq(prompt)
        else:
            return self._call_gemini(prompt)

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
        """
        try:
            prompt = ANALYZE_JOKE_PROMPT.format(joke_text=joke_text)
            response = self._generate(prompt)

            analysis = self._parse_json_response(response)
            logger.info(f"Joke analyzed successfully. Score: {analysis.get('scores', {}).get('general', 'N/A')}")

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing joke: {e}")
            raise

    def suggest_improvements(self, joke_text: str, analysis: Optional[Dict] = None) -> Dict:
        """
        Sugiere mejoras para un chiste
        """
        try:
            if not analysis:
                analysis = self.analyze_joke(joke_text)

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

            response = self._generate(prompt)
            improvements = self._parse_json_response(response)

            logger.info("Improvements suggested successfully")
            return improvements

        except Exception as e:
            logger.error(f"Error suggesting improvements: {e}")
            raise

    def generate_variations(self, joke_text: str, num_variations: int = 3) -> List[Dict]:
        """
        Genera variaciones del chiste
        """
        try:
            prompt = GENERATE_VARIATIONS_PROMPT.format(
                joke_text=joke_text,
                num_variations=num_variations
            )

            response = self._generate(prompt)
            result = self._parse_json_response(response)

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
        """
        try:
            prompt = BRAINSTORM_IDEAS_PROMPT.format(
                topic=topic,
                style=style,
                num_ideas=num_ideas
            )

            response = self._generate(prompt)
            result = self._parse_json_response(response)

            ideas = result.get('ideas', [])
            logger.info(f"Generated {len(ideas)} ideas about: {topic}")

            return ideas

        except Exception as e:
            logger.error(f"Error brainstorming ideas: {e}")
            raise

    def identify_patterns(self, jokes: List[Dict]) -> Dict:
        """
        Identifica patrones en una colección de chistes
        """
        try:
            jokes_text = "\n\n---\n\n".join([
                f"CHISTE {i+1}:\n{joke.get('contenido', joke.get('texto', ''))}"
                for i, joke in enumerate(jokes)
            ])

            prompt = IDENTIFY_PATTERNS_PROMPT.format(
                num_jokes=len(jokes),
                jokes_text=jokes_text
            )

            response = self._generate(prompt)
            patterns = self._parse_json_response(response)

            logger.info(f"Patterns identified from {len(jokes)} jokes")
            return patterns

        except Exception as e:
            logger.error(f"Error identifying patterns: {e}")
            raise

    def suggest_tags(self, joke_text: str) -> Dict:
        """
        Sugiere tags para categorizar un chiste
        """
        try:
            prompt = TAG_SUGGESTION_PROMPT.format(joke_text=joke_text)
            response = self._generate(prompt)

            tags = self._parse_json_response(response)
            logger.info("Tags suggested successfully")

            return tags

        except Exception as e:
            logger.error(f"Error suggesting tags: {e}")
            raise

    def analyze_concepts(self, joke_text: str) -> Dict:
        """
        Analiza en profundidad los conceptos del chiste
        """
        try:
            prompt = ANALYZE_CONCEPTS_PROMPT.format(joke_text=joke_text)
            response = self._generate(prompt)

            concepts = self._parse_json_response(response)
            logger.info(f"Concepts analyzed. Type: {concepts.get('tipo_concepto', 'unknown')}")

            return concepts

        except Exception as e:
            logger.error(f"Error analyzing concepts: {e}")
            raise

    def analyze_rupture(self, joke_text: str) -> Dict:
        """
        Analiza la mecánica de ruptura humorística del chiste
        """
        try:
            prompt = ANALYZE_RUPTURE_PROMPT.format(joke_text=joke_text)
            response = self._generate(prompt)

            rupture = self._parse_json_response(response)
            logger.info(f"Rupture analyzed. Type: {rupture.get('tipo_ruptura', 'unknown')}")

            return rupture

        except Exception as e:
            logger.error(f"Error analyzing rupture: {e}")
            raise


# Instancia global del agente
def get_ai_agent():
    """Obtiene instancia del agente AI si está configurado"""
    try:
        return ComedyAIAgent()
    except ValueError as e:
        logger.warning(f"AI Agent not available: {e}")
        return None

ai_agent = get_ai_agent()
