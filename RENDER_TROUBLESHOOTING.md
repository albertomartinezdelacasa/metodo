# 🔧 Render.com - Guía de Troubleshooting

## 🚨 Errores Comunes y Soluciones

### 1. Error: "Build Failed" o "Failed to install requirements"

**Síntomas:**
```
ERROR: Could not find a version that satisfies the requirement...
```

**Solución:**

1. Verifica que `runtime.txt` tenga una versión válida de Python:
   ```bash
   cat runtime.txt
   # Debe decir: python-3.11.9 (o similar)
   ```

2. Si no existe `runtime.txt`, créalo:
   ```bash
   echo "python-3.11.9" > runtime.txt
   ```

3. Actualiza versiones en `requirements.txt` si son muy antiguas:
   ```bash
   pip install --upgrade pip
   pip list --outdated
   ```

---

### 2. Error: "Application failed to respond"

**Síntomas:**
```
Application failed to respond to health check
Your service is failing because it is not responding to HTTP requests
```

**Causas comunes:**

#### A) Puerto incorrecto

**Solución:** Render usa la variable de entorno `PORT`. Verifica en `render.yaml`:

```yaml
startCommand: gunicorn src.app:app --bind 0.0.0.0:$PORT
```

O en Render Dashboard → Settings → Start Command:
```
gunicorn src.app:app --bind 0.0.0.0:$PORT
```

#### B) La app no arranca

**Solución:** Revisa los logs en Render Dashboard:
1. Ve a tu servicio en Render
2. Click en **"Logs"**
3. Busca errores al inicio

**Errores comunes:**
```
ModuleNotFoundError: No module named 'src'
```
**Fix:** Asegúrate de tener `src/__init__.py`

```
Configuration error: Missing GEMINI_API_KEY
```
**Fix:** Agrega las variables de entorno en Render

---

### 3. Error: "Missing environment variables"

**Síntomas:**
```
Configuration error: Missing SUPABASE_URL
ValueError: Missing required environment variable
```

**Solución:**

1. Ve a Render Dashboard → Tu servicio → **Environment**
2. Agrega TODAS estas variables:

```
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
GEMINI_API_KEY=AIzaSy...
FLASK_ENV=production
FLASK_DEBUG=False
PORT=10000
```

**Variables opcionales:**
```
TODOIST_TOKEN=tu_token
TODOIST_PROJECT_ID=2362882414
```

3. Haz clic en **"Save Changes"**
4. Render redesplegará automáticamente

---

### 4. Error: "Import Error" o "Module not found"

**Síntomas:**
```
ModuleNotFoundError: No module named 'google.generativeai'
ImportError: cannot import name 'supabase'
```

**Solución:**

1. Verifica que `requirements.txt` esté completo:
   ```bash
   cat requirements.txt
   ```

2. Debe incluir:
   ```
   Flask==3.0.0
   gunicorn==21.2.0
   supabase==2.10.0
   google-generativeai==0.3.2
   ```

3. Si falta algo, agrégalo y haz push:
   ```bash
   echo "google-generativeai==0.3.2" >> requirements.txt
   git add requirements.txt
   git commit -m "Add missing dependency"
   git push
   ```

---

### 5. Error: "Static files not loading"

**Síntomas:**
- La app carga pero sin CSS
- Iconos no aparecen
- JavaScript no funciona

**Solución:**

Verifica las rutas en `src/app.py`:
```python
app = Flask(__name__,
            template_folder='../templates',  # Relativo a src/
            static_folder='../static')       # Relativo a src/
```

---

### 6. Error: "Database connection failed"

**Síntomas:**
```
Supabase client initialization failed
Connection timeout
```

**Solución:**

1. Verifica las credenciales de Supabase:
   - Ve a tu proyecto en Supabase
   - Settings → API
   - Copia **URL** y **anon/public key**

2. En Render, actualiza las variables:
   ```
   SUPABASE_URL=https://xxxxx.supabase.co (sin "/" al final)
   SUPABASE_KEY=eyJhbGci... (key completa)
   ```

3. Ejecuta el schema en Supabase:
   - Supabase → SQL Editor
   - Pega el contenido de `database_schema.sql`
   - Run

---

### 7. Error: "Service keeps crashing"

**Síntomas:**
- El servicio arranca y se cae inmediatamente
- Logs muestran: `Worker timeout` o `Worker died`

**Solución:**

#### A) Timeout de Gunicorn

En Render Dashboard → Start Command:
```bash
gunicorn src.app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 1
```

#### B) Memoria insuficiente (Free tier = 512MB)

Reduce workers en Start Command:
```bash
gunicorn src.app:app --bind 0.0.0.0:$PORT --workers 1 --threads 2
```

#### C) Error en código de inicialización

Revisa `src/config.py` y asegúrate de que no falle la validación:
```python
def validate(self):
    """No debe hacer raise si variables opcionales faltan"""
    if not self.GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY not set")
        # NO: raise ValueError("Missing GEMINI_API_KEY")
```

---

## 📋 Checklist Pre-Deploy

Antes de desplegar en Render, verifica:

- [ ] `requirements.txt` existe y está completo
- [ ] `runtime.txt` tiene versión válida de Python (3.11.9)
- [ ] `Procfile` o `render.yaml` configurado correctamente
- [ ] Código funciona en local (`python src/app.py`)
- [ ] Variables de entorno en `.env` funcionan
- [ ] Database schema ejecutado en Supabase
- [ ] Todas las rutas usan paths relativos correctos
- [ ] No hay imports absolutos que fallen en producción

---

## 🔍 Cómo Revisar Logs en Render

1. Ve a [dashboard.render.com](https://dashboard.render.com)
2. Click en tu servicio **"metodo-comedia"**
3. Click en **"Logs"** en el menú lateral
4. Busca estos mensajes clave:

**✅ Señales de éxito:**
```
==> Build successful 🎉
==> Starting service...
Starting server on port 10000
Flask app created successfully
Configuration validated successfully
```

**❌ Señales de error:**
```
ERROR: Could not find a version...
ModuleNotFoundError: No module named...
Configuration error: Missing...
Application failed to respond
Worker timeout
```

---

## 🚀 Deploy desde Cero

Si nada funciona, empieza de nuevo:

### 1. Elimina el servicio actual en Render

1. Dashboard → Tu servicio → **Settings**
2. Scroll hasta abajo → **Delete Service**

### 2. Crea un nuevo servicio

1. Render Dashboard → **New** → **Web Service**
2. Conecta tu repositorio de GitHub
3. Configuración:
   ```
   Name: metodo-comedia
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn src.app:app --bind 0.0.0.0:$PORT
   ```

### 3. Agrega variables de entorno

En la sección **Environment Variables**:
```
SUPABASE_URL = https://xxxxx.supabase.co
SUPABASE_KEY = eyJhbGci...
GEMINI_API_KEY = AIzaSy...
FLASK_ENV = production
```

### 4. Deploy

Click en **"Create Web Service"**

Espera 5-10 minutos. Render:
1. Clonará tu repo
2. Instalará dependencias
3. Ejecutará el start command
4. Te dará una URL: `https://metodo-comedia-xxxx.onrender.com`

---

## 🧪 Test Local antes de Deploy

Simula el ambiente de Render en local:

```bash
# 1. Activa el entorno virtual
venv\Scripts\activate  # Windows

# 2. Instala dependencias exactas
pip install -r requirements.txt

# 3. Prueba con gunicorn (como Render)
gunicorn src.app:app --bind 0.0.0.0:5000

# 4. Abre http://localhost:5000
# Si funciona aquí, debería funcionar en Render
```

---

## 📞 Necesitas Ayuda Específica

Si el error persiste, necesito ver:

1. **Logs de Render** (copia los últimos 50 líneas)
2. **Mensaje de error específico**
3. **URL de tu servicio en Render**

Puedes copiar los logs así:

1. Render Dashboard → Logs
2. Click en el icono de **"Copy"** (arriba a la derecha)
3. Pégalos aquí

---

## ✅ Verificación Final

Una vez desplegado, verifica:

1. **Health check:**
   ```
   https://tu-app.onrender.com/health
   ```
   Debería responder:
   ```json
   {
     "status": "healthy",
     "service": "metodo-comedia",
     "version": "1.0.0"
   }
   ```

2. **Página principal:**
   ```
   https://tu-app.onrender.com/
   ```
   Debe cargar la interfaz completa con CSS

3. **API de chistes:**
   ```
   https://tu-app.onrender.com/api/jokes/
   ```
   Debe devolver JSON (aunque esté vacío)

---

**¿Cuál es el error específico que estás viendo?**

Dime el mensaje de error y te ayudo a solucionarlo paso a paso.
