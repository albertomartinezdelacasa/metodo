# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 📋 PROJECT OVERVIEW

**Método Comedia** is a web application for stand-up comedians to analyze, improve, and manage their jokes using AI.

**Stack:**
- Backend: Python 3.11+, Flask, Google Gemini AI (free tier)
- Frontend: HTML5, Tailwind CSS, Vanilla JavaScript, PWA
- Database: Supabase (PostgreSQL)
- Integrations: Todoist API
- Deployment: Render.com (free tier)

---

## 🚀 QUICK START

### Development Setup

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 4. Run the app
python src/app.py
```

Access at: http://localhost:5000

### Database Setup

1. Create Supabase project at https://supabase.com
2. Execute `database_schema.sql` in Supabase SQL Editor
3. Copy URL and keys to `.env`

### Get Free API Keys

- **Gemini AI**: https://makersuite.google.com/app/apikey (1500 req/day free)
- **Supabase**: https://supabase.com (500MB free)
- **Todoist**: https://todoist.com/prefs/integrations

---

## 🏗️ ARCHITECTURE

```
metodo/
├── src/
│   ├── app.py                    # Flask app entry point
│   ├── config.py                 # Configuration & env vars
│   ├── services/
│   │   ├── supabase_client.py   # Database operations
│   │   ├── ai_agent.py          # Gemini AI integration
│   │   └── todoist_client.py    # Todoist sync
│   ├── routes/
│   │   ├── jokes.py             # CRUD endpoints
│   │   └── ai.py                # AI analysis endpoints
│   └── utils/
│       └── prompts.py           # AI prompt templates
├── templates/
│   └── index.html               # Main PWA interface
├── static/
│   ├── css/style.css
│   ├── js/app.js                # Frontend logic
│   ├── manifest.json            # PWA config
│   └── service-worker.js        # Offline support
└── database_schema.sql          # Supabase schema

```

---

## 🔑 ENVIRONMENT VARIABLES

Required variables in `.env`:

```bash
# Supabase (required)
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJhbGci...
SUPABASE_SERVICE_KEY=eyJhbGci...

# Google Gemini AI (required)
GEMINI_API_KEY=AIzaSy...

# Todoist (optional)
TODOIST_TOKEN=c4cee5abfa79870a2c1e4767e4228eb3846d2651
TODOIST_PROJECT_ID=2362882414

# Flask
FLASK_ENV=production
FLASK_DEBUG=False
PORT=5000
```

---

## 📊 DATABASE SCHEMA

### Main Tables

**chistes** - Jokes storage
- Fields: id, titulo, contenido, estado, calificacion, veces_usado, notas
- Estados: borrador, revisado, probado, pulido, archivado
- Soft delete: eliminado (boolean)

**analisis_ia** - AI analysis results
- Links to chistes via chiste_id
- Stores: estructura (JSON), tecnicas (array), scores (numeric)
- Automatically created when analyzing jokes

**tags** - Categorization tags
- Categories: tema, tecnica, audiencia, tono, evento

**chistes_tags** - Many-to-many relationship

**versiones_chiste** - Version history (auto-saved on content updates)

**presentaciones** - Show tracking

**chistes_presentaciones** - Jokes used in shows

---

## 🤖 AI AGENT CAPABILITIES

### Available AI Functions

```python
from src.services.ai_agent import ai_agent

# Analyze joke structure
analysis = ai_agent.analyze_joke(joke_text)
# Returns: estructura, tecnicas, puntos_fuertes/debiles, sugerencias, scores

# Suggest improvements
improvements = ai_agent.suggest_improvements(joke_text, analysis)
# Returns: 3 improved versions (timing, claridad, twist)

# Generate variations
variations = ai_agent.generate_variations(joke_text, num=3)

# Brainstorm ideas
ideas = ai_agent.brainstorm_ideas(topic="familia", style="observacional", num=5)

# Identify patterns
patterns = ai_agent.identify_patterns(jokes_list)

# Suggest tags
tags = ai_agent.suggest_tags(joke_text)
```

### Prompt Templates

Located in `src/utils/prompts.py`. Modify these to customize AI behavior:
- `ANALYZE_JOKE_PROMPT` - Main analysis template
- `SUGGEST_IMPROVEMENTS_PROMPT` - Improvement suggestions
- `BRAINSTORM_IDEAS_PROMPT` - Idea generation
- etc.

---

## 🌐 API ENDPOINTS

### Jokes CRUD

```
GET    /api/jokes/              # List all jokes (filter: ?estado=probado)
GET    /api/jokes/<id>          # Get single joke
POST   /api/jokes/              # Create joke
PUT    /api/jokes/<id>          # Update joke
DELETE /api/jokes/<id>          # Delete joke (soft delete)
POST   /api/jokes/<id>/use      # Increment usage counter
```

### AI Operations

```
POST   /api/ai/analyze          # Analyze joke with AI
POST   /api/ai/improve          # Suggest improvements
POST   /api/ai/variations       # Generate variations
POST   /api/ai/brainstorm       # Generate ideas
POST   /api/ai/patterns         # Identify patterns
POST   /api/ai/tags             # Suggest tags
```

### Request/Response Examples

**Create Joke:**
```json
POST /api/jokes/
{
  "titulo": "Chiste sobre aviones",
  "contenido": "Los pilotos siempre dicen...",
  "estado": "borrador",
  "calificacion": 7,
  "notas": "Probar en show abierto"
}
```

**Analyze Joke:**
```json
POST /api/ai/analyze
{
  "joke_text": "Mi chiste aquí...",
  "save": true  // Save to database if joke_id provided
}
```

---

## 📱 PWA FEATURES

### Installation

Users can install the app on iPhone/Android:
1. Open in Safari/Chrome
2. Tap "Share" → "Add to Home Screen"
3. App opens fullscreen like native app

### Offline Support

Service Worker caches:
- HTML/CSS/JS files
- Network-first strategy for API calls
- Falls back to cache when offline

### Configuration

- `static/manifest.json` - App metadata, icons, colors
- `static/service-worker.js` - Offline behavior

---

## 🚢 DEPLOYMENT

### Render.com (Free Tier)

1. Connect GitHub repo to Render
2. Create Web Service:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn src.app:app`
3. Add environment variables
4. Deploy!

**Files for deployment:**
- `Procfile` - For Heroku-compatible platforms
- `render.yaml` - Render.com configuration
- `runtime.txt` - Python version

**Important:** Free tier sleeps after 15min inactivity (30-60s wake time)

---

## 🔍 DEVELOPMENT PATTERNS

### Adding New AI Function

1. Add prompt template to `src/utils/prompts.py`
2. Add method to `ComedyAIAgent` class in `src/services/ai_agent.py`
3. Create route in `src/routes/ai.py`
4. Add frontend function in `static/js/app.js`

### Database Queries

Always use repository classes:
```python
from src.services.supabase_client import jokes_repo, analysis_repo

# Create
joke = jokes_repo.create_joke(data)

# Read
joke = jokes_repo.get_joke(joke_id)
all_jokes = jokes_repo.get_all_jokes({'estado': 'pulido'})

# Update
jokes_repo.update_joke(joke_id, {'calificacion': 9})

# Delete (soft)
jokes_repo.delete_joke(joke_id, soft_delete=True)
```

### Error Handling

All API routes return consistent format:
```json
{
  "success": true/false,
  "data": {...},          // On success
  "error": "message"      // On failure
}
```

---

## 🐛 TROUBLESHOOTING

**"Configuration error: Missing GEMINI_API_KEY"**
- Create `.env` file from `.env.example`
- Add your Gemini API key

**"Supabase client initialization failed"**
- Check SUPABASE_URL and SUPABASE_KEY in `.env`
- Verify Supabase project is active

**AI requests failing**
- Check Gemini API key is valid
- Free tier: 1500 requests/day limit
- Response must be valid JSON

**Frontend not loading**
- Check Flask is running on correct port
- Verify static files path in `src/app.py`

**PWA not installing**
- HTTPS required (works on localhost)
- Check manifest.json is valid
- Verify service-worker.js loads

---

## 📝 CODING CONVENTIONS

- **Python:** PEP 8, type hints encouraged
- **JavaScript:** ES6+, async/await for API calls
- **CSS:** Tailwind utility classes preferred
- **Commits:** Descriptive messages, present tense
- **Logging:** Use `logger.info/error` not `print`

---

## 🔒 SECURITY NOTES

- **NEVER** commit `.env` file (in `.gitignore`)
- API keys should be in environment variables only
- Supabase RLS (Row Level Security) disabled by default
- CORS configured for localhost + Render domains
- Input validation on all API endpoints

---

## 📊 USEFUL QUERIES

```sql
-- Get jokes with latest AI analysis
SELECT c.*, a.puntuacion_general
FROM chistes c
LEFT JOIN LATERAL (
  SELECT * FROM analisis_ia
  WHERE chiste_id = c.id
  ORDER BY fecha_analisis DESC
  LIMIT 1
) a ON true
WHERE NOT c.eliminado;

-- Most used jokes
SELECT titulo, contenido, veces_usado
FROM chistes
WHERE NOT eliminado
ORDER BY veces_usado DESC
LIMIT 10;

-- Performance by estado
SELECT estado,
       COUNT(*) as total,
       AVG(calificacion) as avg_rating
FROM chistes
WHERE NOT eliminado
GROUP BY estado;
```

---

## 💡 FUTURE ENHANCEMENTS

Ideas for expansion:
- Voice recording integration
- Export to Obsidian (.md files)
- Pattern analysis across all jokes
- Show/performance tracking
- Collaborative features
- Video recording analysis
- Audience reaction tracking

---

## 📞 IMPORTANT NOTES

- Gemini AI is FREE (1500 req/day) - no credit card needed
- Supabase free tier: 500MB database, 50k users/month
- Todoist integration is optional, not required for core functionality
- Project ID for Todoist: **2362882414** (Metodo project only)
- PWA works on iPhone but requires Safari (not Chrome)

---

**Last updated:** 2025-11-17
**Version:** 1.0.0
