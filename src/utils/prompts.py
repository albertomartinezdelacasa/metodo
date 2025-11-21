"""
Templates de prompts para el agente de IA
"""

ANALYZE_JOKE_PROMPT = """Eres un experto en comedia stand-up y análisis humorístico. Analiza el siguiente chiste en profundidad:

CHISTE:
"{joke_text}"

Proporciona un análisis estructurado en formato JSON con la siguiente estructura:

{{
  "estructura": {{
    "setup": "identifica y cita el setup (la preparación)",
    "punchline": "identifica y cita el punchline (el remate)",
    "twist": "describe el elemento sorpresa o giro",
    "callback": "si hay referencia a algo anterior, descríbelo"
  }},
  "tecnicas": ["lista las técnicas cómicas utilizadas"],
  "puntos_fuertes": ["qué aspectos funcionan bien y por qué"],
  "puntos_debiles": ["qué aspectos podrían mejorar y por qué"],
  "sugerencias": ["3-5 sugerencias específicas de mejora"],
  "scores": {{
    "estructura": 7.5,
    "originalidad": 8.0,
    "timing": 7.0,
    "general": 7.5
  }}
}}

TÉCNICAS CÓMICAS POSIBLES:
- Exageración: amplificar la realidad
- Incongruencia: elementos que no encajan
- Wordplay: juegos de palabras
- Observacional: comentarios sobre la vida cotidiana
- Autoburla: reírse de uno mismo
- Sarcasmo: ironía mordaz
- Timing: ritmo y pausas
- Callback: referencia a chiste anterior
- Regla de tres: patrón-patrón-sorpresa
- Absurdo: lógica ilógica
- Comparación: analogías inesperadas

CRITERIOS DE EVALUACIÓN:
- Estructura (0-10): Setup claro, punchline efectivo, twist sorprendente
- Originalidad (0-10): Perspectiva única, evita clichés
- Timing (0-10): Ritmo, pausas, construcción de tensión
- General (0-10): Promedio ponderado + factor "wow"

Responde SOLO con el JSON, sin texto adicional.
"""

SUGGEST_IMPROVEMENTS_PROMPT = """Basándote en el análisis previo de este chiste, genera versiones mejoradas.

CHISTE ORIGINAL:
"{joke_text}"

ANÁLISIS PREVIO:
{analysis_summary}

Genera 3 versiones mejoradas del chiste que:
1. VERSION_TIMING: Optimiza el timing y ritmo del punchline
2. VERSION_CLARIDAD: Mejora la claridad del setup sin perder impacto
3. VERSION_TWIST: Fortalece el elemento sorpresa o giro

Responde en formato JSON:

{{
  "version_timing": {{
    "texto": "versión mejorada enfocada en timing",
    "cambios": "qué se modificó y por qué mejora el timing"
  }},
  "version_claridad": {{
    "texto": "versión mejorada enfocada en claridad",
    "cambios": "qué se modificó y por qué mejora la claridad"
  }},
  "version_twist": {{
    "texto": "versión mejorada enfocada en el twist",
    "cambios": "qué se modificó y por qué mejora la sorpresa"
  }},
  "recomendacion": "cuál de las 3 versiones recomiendas y por qué"
}}

Mantén la esencia del chiste original. Responde SOLO con JSON.
"""

GENERATE_VARIATIONS_PROMPT = """Genera {num_variations} variaciones del siguiente chiste, explorando diferentes enfoques:

CHISTE ORIGINAL:
"{joke_text}"

Para cada variación:
- Mantén la premisa básica
- Explora diferentes punchlines
- Experimenta con técnicas distintas
- Varía el estilo (más absurdo, más observacional, más sarcástico, etc.)

Responde en formato JSON:

{{
  "variaciones": [
    {{
      "numero": 1,
      "texto": "variación del chiste",
      "tecnica": "técnica principal usada",
      "estilo": "estilo de humor",
      "diferencia": "en qué se diferencia del original"
    }},
    ...
  ]
}}

Responde SOLO con JSON.
"""

BRAINSTORM_IDEAS_PROMPT = """Genera {num_ideas} ideas originales de chistes sobre el siguiente tema:

TEMA: {topic}
ESTILO PREFERIDO: {style}

Para cada idea proporciona:
- Setup básico (la preparación)
- Dirección del punchline (sin escribirlo completo, solo la idea)
- Técnica sugerida
- Nivel de dificultad (fácil, medio, difícil)

Responde en formato JSON:

{{
  "ideas": [
    {{
      "numero": 1,
      "setup": "setup básico del chiste",
      "direccion_punchline": "hacia dónde debería ir el remate",
      "tecnica": "técnica cómica sugerida",
      "dificultad": "fácil|medio|difícil",
      "notas": "notas adicionales o tips"
    }},
    ...
  ]
}}

Busca perspectivas originales y evita clichés. Responde SOLO con JSON.
"""

IDENTIFY_PATTERNS_PROMPT = """Analiza los siguientes {num_jokes} chistes y identifica patrones en el estilo cómico:

CHISTES:
{jokes_text}

Identifica:
1. Técnicas más utilizadas
2. Temas recurrentes
3. Estructura preferida
4. Fortalezas consistentes
5. Áreas de mejora comunes
6. Estilo distintivo

Responde en formato JSON:

{{
  "tecnicas_frecuentes": [
    {{"tecnica": "nombre", "frecuencia": 5, "porcentaje": 50}}
  ],
  "temas_recurrentes": ["tema1", "tema2"],
  "estructura_preferida": "descripción de la estructura típica",
  "fortalezas": ["fortaleza1", "fortaleza2"],
  "areas_mejora": ["área1", "área2"],
  "estilo_distintivo": "descripción del estilo único",
  "recomendaciones": [
    "recomendación específica basada en los patrones"
  ]
}}

Responde SOLO con JSON.
"""

TAG_SUGGESTION_PROMPT = """Sugiere tags/etiquetas apropiados para categorizar este chiste:

CHISTE:
"{joke_text}"

Categorías de tags:
- TEMA: sobre qué es el chiste (familia, tecnología, viajes, etc.)
- TÉCNICA: qué técnica usa (exageración, wordplay, observacional, etc.)
- AUDIENCIA: para qué tipo de público (general, adultos, corporativo, etc.)
- TONO: qué tono tiene (ligero, oscuro, sarcástico, absurdo, etc.)

Responde en formato JSON:

{{
  "tema": ["tag1", "tag2"],
  "tecnica": ["tag1", "tag2"],
  "audiencia": ["tag1"],
  "tono": ["tag1"]
}}

Máximo 3 tags por categoría. Responde SOLO con JSON.
"""

ANALYZE_CONCEPTS_PROMPT = """Eres un experto en análisis conceptual de humor. Analiza en detalle el CONCEPTO del siguiente chiste:

CHISTE:
"{joke_text}"

Analiza:

1. **CONCEPTO PRINCIPAL**: Identifica el concepto central del chiste (la idea o situación principal)

2. **TIPO DE CONCEPTO**: Clasifica el concepto como:
   - SIMPLE: Un solo concepto claro y directo
   - COMPUESTO: Combina dos o más conceptos diferentes
   - CONCRETO: Basado en objetos/situaciones tangibles y específicas
   - ABSTRACTO: Basado en ideas, emociones o conceptos intangibles

3. **MAPA DE ASOCIACIONES**: Identifica las asociaciones mentales que conectan el setup con el punchline:
   - ¿Qué conceptos asociados se activan?
   - ¿Cómo se relacionan entre sí?
   - ¿Qué asociación inesperada crea el humor?

Responde en formato JSON:

{{
  "concepto_principal": "descripción clara del concepto central",
  "tipo_concepto": "simple|compuesto|concreto|abstracto",
  "explicacion_tipo": "explicación detallada de por qué es este tipo",
  "mapa_conceptos": {{
    "concepto_inicial": "concepto que presenta el setup",
    "asociaciones_esperadas": ["asociaciones lógicas/esperadas"],
    "asociacion_inesperada": "la asociación sorpresa que crea el humor",
    "conceptos_secundarios": ["otros conceptos que intervienen"],
    "explicacion": "cómo funciona el mapa de asociaciones"
  }},
  "ejemplos_similares": ["ejemplos de chistes con estructura conceptual similar"],
  "potencial_expansion": "cómo se podría expandir o explotar más este concepto"
}}

Responde SOLO con JSON.
"""

ANALYZE_RUPTURE_PROMPT = """Eres un experto en mecánicas de humor. Analiza la RUPTURA humorística del siguiente chiste:

CHISTE:
"{joke_text}"

La RUPTURA es el mecanismo que rompe la expectativa y crea la sorpresa/risa. Analiza:

1. **TIPO DE RUPTURA**: Identifica el tipo principal:
   - INCONGRUENCIA: Elementos que no deberían ir juntos
   - REINTERPRETACIÓN: Cambio en el significado de algo dicho antes
   - EXAGERACIÓN: Llevar algo al extremo absurdo
   - DEFLACIÓN: Reducir algo importante a trivial
   - INVERSIÓN: Voltear roles o expectativas
   - YUXTAPOSICIÓN: Contrastar elementos opuestos
   - SORPRESA: Elemento completamente inesperado
   - VIOLACIÓN DE NORMA: Romper una regla social/lógica

2. **SUBTIPO**: Especifica más el mecanismo:
   - Para incongruencia: ¿semántica, situacional, conceptual?
   - Para reinterpretación: ¿doble sentido, contexto, perspectiva?
   - Para exageración: ¿escala, consecuencias, características?
   - Etc.

3. **MECÁNICA**: Explica exactamente CÓMO funciona la ruptura paso a paso

Responde en formato JSON:

{{
  "tipo_ruptura": "tipo principal de ruptura",
  "subtipo_ruptura": "subtipo específico",
  "explicacion_ruptura": "explicación detallada del mecanismo",
  "expectativa_creada": "qué expectativa crea el setup",
  "momento_ruptura": "en qué punto exacto ocurre la ruptura",
  "efecto_logrado": "qué efecto humorístico logra",
  "intensidad_ruptura": "suave|moderada|fuerte - qué tan drástica es",
  "mejoras_posibles": ["cómo podría intensificarse la ruptura"],
  "ejemplos_similares": ["ejemplos de rupturas del mismo tipo"]
}}

Responde SOLO con JSON.
"""
