# 🚀 Guía de Inicio Rápido - Método Comedia

## ⏱️ Tiempo estimado: 15 minutos

---

## Paso 1: Configurar Base de Datos (5 min)

### 1.1 Crear Cuenta Supabase

1. Ve a https://supabase.com
2. Click en **"Start your project"**
3. Crea cuenta con GitHub/Google (gratis)

### 1.2 Crear Proyecto

1. Click **"New Project"**
2. Nombre: `metodo-comedia` (o el que quieras)
3. Database Password: (guarda esta contraseña)
4. Region: Elige la más cercana
5. Click **"Create new project"** (tarda 1-2 min)

### 1.3 Ejecutar Schema SQL

1. En Supabase, ve a **SQL Editor** (icono izquierdo)
2. Click **"New query"**
3. Abre el archivo `database_schema.sql` de este proyecto
4. **Copia todo el contenido** y pégalo en Supabase
5. Click **"Run"** (abajo a la derecha)
6. Deberías ver: "Success. No rows returned"

### 1.4 Obtener Credenciales

1. Ve a **Settings** → **API**
2. Copia estos 3 valores:
   - **Project URL** (ej: https://xxx.supabase.co)
   - **anon public** key
   - **service_role** key (click "Reveal" primero)

---

## Paso 2: API de Google Gemini (2 min)

### 2.1 Obtener API Key

1. Ve a https://makersuite.google.com/app/apikey
2. Click **"Create API Key"**
3. Selecciona un proyecto de Google Cloud (o crea uno nuevo)
4. Copia la API key que empieza con `AIzaSy...`

**Nota:** Es **100% gratis**, 1,500 requests/día. No necesitas tarjeta.

---

## Paso 3: Configurar Proyecto Local (3 min)

### 3.1 Crear Entorno Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3.2 Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3.3 Configurar Variables de Entorno

1. Copia el archivo de ejemplo:
```bash
cp .env.example .env
```

2. Abre `.env` con tu editor favorito

3. Completa con tus credenciales del Paso 1 y 2:

```env
# Paso 1.4 - Supabase
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=tu_anon_public_key
SUPABASE_SERVICE_KEY=tu_service_role_key

# Paso 2.1 - Gemini
GEMINI_API_KEY=AIzaSy_tu_key_aqui

# Opcional - Si tienes Todoist
TODOIST_TOKEN=tu_token
TODOIST_PROJECT_ID=2362882414

# Flask (dejar como está)
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
```

4. Guarda el archivo

---

## Paso 4: Ejecutar la Aplicación (1 min)

```bash
python src/app.py
```

Deberías ver:
```
* Running on http://0.0.0.0:5000
```

---

## Paso 5: ¡Usar la App! (∞ min)

1. Abre tu navegador en: http://localhost:5000

2. **Escribir tu primer chiste:**
   - Tab "Escribir"
   - Escribe un chiste
   - Click "Analizar con IA"
   - ¡Mira el análisis automático!

3. **Generar ideas:**
   - Tab "Ideas"
   - Escribe un tema (ej: "familia")
   - Click "Generar Ideas"

4. **Ver tus chistes:**
   - Tab "Mis Chistes"
   - Ve todos tus chistes guardados

---

## 🎉 ¡Listo!

Tu aplicación está funcionando localmente. Ahora puedes:

### Siguiente: Instalar como PWA en tu teléfono

**iPhone:**
1. Abre http://localhost:5000 en **Safari** (debe ser Safari, no Chrome)
2. Tap el botón **Compartir** (cuadrado con flecha)
3. Scroll y tap **"Añadir a pantalla de inicio"**
4. Nombra la app: "Comedia"
5. ¡Listo! Ahora tienes un icono en tu pantalla

**Android:**
1. Abre http://localhost:5000 en Chrome
2. Menú → **"Instalar app"** o **"Añadir a pantalla inicio"**

---

## 📊 Deployment a Internet (Opcional)

Si quieres que funcione desde cualquier lugar (no solo localhost):

### Opción Recomendada: Render.com (Gratis)

1. Sube tu código a GitHub
2. Ve a https://render.com
3. Click **"New +"** → **"Web Service"**
4. Conecta tu repo de GitHub
5. Configuración:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn src.app:app`
6. En **"Environment"**, agrega las mismas variables del `.env`:
   - SUPABASE_URL
   - SUPABASE_KEY
   - SUPABASE_SERVICE_KEY
   - GEMINI_API_KEY
7. Click **"Create Web Service"**

En ~5 minutos tendrás una URL pública (ej: `https://metodo-comedia.onrender.com`)

**Limitación Free Tier:** Se duerme tras 15 min sin uso (30-60s para despertar)

---

## ❓ Problemas Comunes

### "ModuleNotFoundError: No module named 'flask'"
→ No activaste el entorno virtual. Ejecuta:
```bash
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### "Configuration error: Missing GEMINI_API_KEY"
→ El archivo `.env` no existe o está vacío. Revisa Paso 3.3

### "Supabase client initialization failed"
→ Verifica que las credenciales en `.env` sean correctas. No deben tener espacios ni comillas.

### La IA no responde
→ Verifica:
1. API key de Gemini es correcta
2. No excediste 1,500 requests/día
3. Tienes conexión a internet

### No se guardan los chistes
→ Verifica:
1. Ejecutaste `database_schema.sql` en Supabase
2. Las credenciales de Supabase son correctas
3. Ve a Supabase → Table Editor → deberías ver la tabla "chistes"

---

## 📞 Necesitas Ayuda?

1. Revisa `CLAUDE.md` - Documentación técnica completa
2. Revisa `README.md` - Guía general del proyecto
3. Abre un issue en GitHub

---

**¡A crear chistes mejores con IA! 🎤🚀**
