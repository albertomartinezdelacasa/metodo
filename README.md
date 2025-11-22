# 🎤 Método Comedia

Sistema de análisis y mejora de chistes de stand-up con Inteligencia Artificial.

> **Stack 100% Gratuito:** Google Gemini AI + Supabase + Render.com = $0/mes

---

## ✨ Características

- 🤖 **Análisis de IA**: Estructura, técnicas, puntos fuertes/débiles
- ✨ **Sugerencias de Mejora**: 3 versiones optimizadas de cada chiste
- 💡 **Brainstorming**: Genera ideas sobre cualquier tema
- 📊 **Gestión**: Organiza chistes por estado (borrador → pulido)
- 🎭 **Tracking**: Contador de usos y calificaciones
- 📱 **PWA**: Instala en iPhone/Android como app nativa
- 📲 **Gestión Móvil**: Administra tu proyecto desde el móvil (deploy, tests, backups)
- 🔄 **Todoist Sync**: Sincroniza tareas (opcional)
- 🌐 **Offline**: Funciona sin conexión gracias a Service Worker

---

## 🚀 Inicio Rápido

### 1. Requisitos

- Python 3.11+
- Cuenta Supabase (gratis)
- API Key de Google Gemini (gratis)

### 2. Instalación

```bash
# Clonar repositorio
git clone <tu-repo>
cd metodo

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configuración

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales
nano .env  # o usa tu editor favorito
```

**Variables requeridas:**
```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu_key_aqui
GEMINI_API_KEY=AIzaSy_tu_key_aqui
```

### 4. Base de Datos

1. Crea proyecto en [Supabase](https://supabase.com)
2. Ve a SQL Editor
3. Ejecuta el contenido de `database_schema.sql`
4. Copia URL y keys al `.env`

### 5. Ejecutar

```bash
python src/app.py
```

Abre: http://localhost:5000

---

## 📱 Instalar como App (PWA)

### iPhone
1. Abre en Safari
2. Tap **Compartir** → **Añadir a pantalla de inicio**
3. ¡Listo! Ahora tienes el icono en tu pantalla

### Android
1. Abre en Chrome
2. Menú → **Instalar app** o **Añadir a pantalla inicio**

---

## 📲 Gestión Móvil

**¡NUEVO!** Ahora puedes administrar tu proyecto completamente desde el móvil usando GitHub Mobile y la PWA.

### ¿Qué puedes hacer desde el móvil?

✅ **Gestión de Chistes** (PWA)
- Crear, editar y analizar chistes
- Ver mejoras sugeridas por IA
- Gestionar bitácora

✅ **Gestión Técnica** (GitHub Issues)
- 🧪 Ejecutar tests automáticos
- 🚀 Desplegar a producción
- 💾 Crear backups de base de datos
- 🔍 Analizar calidad de código
- 📦 Actualizar dependencias
- 📊 Ver estadísticas del sistema

### Setup Rápido

1. **Instala la PWA** (instrucciones arriba)

2. **Configura gestión móvil:**
   ```bash
   python configure_mobile.py
   ```

3. **Instala GitHub Mobile** desde tu App Store

4. **Listo!** Ve al tab "⚙️ Gestión" en la PWA

📖 **Guía completa:** Ver [MOBILE_GUIDE.md](MOBILE_GUIDE.md) para instrucciones detalladas, workflows y troubleshooting.

---

## 🔑 Obtener API Keys (Gratis)

### Google Gemini AI
1. Ve a https://makersuite.google.com/app/apikey
2. Crea API key (gratis, sin tarjeta)
3. Límite: 1,500 requests/día

### Supabase
1. Ve a https://supabase.com
2. Crea proyecto (gratis)
3. Settings → API → Copia URL y keys
4. Límite: 500MB database, 50k usuarios/mes

### Todoist (Opcional)
1. https://todoist.com/prefs/integrations
2. Copia tu token de API

---

## 🌐 Deploy en Render (Gratis)

### Opción 1: Desde GitHub

1. Push tu código a GitHub
2. Ve a [Render.com](https://render.com)
3. New → Web Service
4. Conecta GitHub repo
5. Configuración:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn src.app:app`
6. Agrega variables de entorno del `.env`
7. Deploy!

### Opción 2: render.yaml

```yaml
services:
  - type: web
    name: metodo-comedia
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn src.app:app
```

Push a GitHub y Render detectará automáticamente.

**Nota:** Free tier se duerme tras 15min inactividad (tarda 30-60s en despertar)

---

## 📖 Uso

### Escribir Chiste

1. Tab **"Escribir"**
2. Escribe tu chiste
3. Selecciona estado y calificación
4. **Guardar** o **Analizar con IA**

### Analizar con IA

- **Analizar**: Obtén estructura, técnicas, scores
- **Sugerir Mejoras**: 3 versiones optimizadas
- Scores: Estructura, Originalidad, Timing, General (0-10)

### Generar Ideas

1. Tab **"Ideas"**
2. Escribe tema (ej: "tecnología")
3. Selecciona estilo
4. **Generar Ideas**

### Ver Mis Chistes

1. Tab **"Mis Chistes"**
2. Filtra por estado
3. Ve estadísticas de uso y calificaciones

---

## 🛠️ Desarrollo

### Estructura del Proyecto

```
metodo/
├── src/
│   ├── app.py              # Flask app principal
│   ├── config.py           # Configuración
│   ├── services/           # Lógica de negocio
│   ├── routes/             # API endpoints
│   └── utils/              # Utilidades
├── templates/              # HTML
├── static/                 # CSS, JS, PWA
├── database_schema.sql     # Schema de BD
├── requirements.txt        # Dependencias Python
└── .env                    # Variables de entorno
```

### API Endpoints

```
GET    /api/jokes/              # Listar chistes
POST   /api/jokes/              # Crear chiste
GET    /api/jokes/<id>          # Obtener chiste
PUT    /api/jokes/<id>          # Actualizar chiste
DELETE /api/jokes/<id>          # Eliminar chiste

POST   /api/ai/analyze          # Analizar con IA
POST   /api/ai/improve          # Sugerir mejoras
POST   /api/ai/brainstorm       # Generar ideas
POST   /api/ai/variations       # Variaciones del chiste
```

### Tests

```bash
pytest tests/
```

---

## 💰 Costos

| Servicio | Costo | Límites |
|----------|-------|---------|
| **Gemini AI** | $0 | 1,500 req/día |
| **Supabase** | $0 | 500MB DB, 50k users/mes |
| **Render.com** | $0 | Sleep tras 15min |
| **Todoist** | $0 | API incluida |
| **TOTAL** | **$0/mes** | ✅ |

---

## 📊 Roadmap

- [ ] Export a Obsidian (.md)
- [ ] Grabación de audio
- [ ] Tracking de shows
- [ ] Análisis de patrones
- [ ] Modo colaborativo
- [ ] Analytics avanzado

---

## 🐛 Troubleshooting

**Error: "GEMINI_API_KEY not configured"**
- Verifica que `.env` existe y tiene la API key

**No carga chistes**
- Revisa conexión a Supabase
- Verifica que ejecutaste `database_schema.sql`

**IA no responde**
- Check límite de 1500 req/día de Gemini
- Verifica API key válida

**PWA no instala**
- Necesita HTTPS (funciona en localhost)
- En producción, Render provee HTTPS automático

---

## 📝 Licencia

MIT License - Usa libremente

---

## 💬 Soporte

- Revisa `CLAUDE.md` para documentación técnica
- Issues: Abre un issue en GitHub
- Email: [tu-email]

---

**🎤 ¡Mejora tu comedia con IA! 🚀**

Hecho con ❤️ por un comediante para comediantes
