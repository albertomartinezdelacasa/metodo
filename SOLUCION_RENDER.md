# 🔧 Solución: Deploy en Render.com

## 📊 Diagnóstico Actual

Tu proyecto está **95% listo** para desplegar en Render. Solo tienes que:

1. ✅ Commit los cambios recientes
2. ✅ Push a GitHub
3. ✅ Configurar en Render Dashboard

---

## 🚀 Pasos para Desplegar (Solución Rápida)

### Paso 1: Commit y Push (5 minutos)

Primero necesitas autenticarte en GitHub. Tienes el error:
```
Permission denied to albertomartinezdelacasa/metodo.git
```

**Solución A: GitHub CLI (Recomendado)**

```bash
# Instala GitHub CLI si no lo tienes
# Descarga de: https://cli.github.com/

# Autentica
gh auth login

# Selecciona:
# - GitHub.com
# - HTTPS
# - Login with a web browser

# Luego haz push
git push
```

**Solución B: Cambiar a SSH**

```bash
# Cambiar remote a SSH
git remote set-url origin git@github.com:albertomartinezdelacasa/metodo.git

# Push
git push
```

**Solución C: Personal Access Token**

1. Ve a: https://github.com/settings/tokens
2. Generate new token (classic)
3. Marca: `repo` (todos los permisos de repositorio)
4. Copia el token
5. Úsalo como contraseña cuando hagas push:
   ```bash
   git push
   # Username: albertomartinezdelacasa
   # Password: [pega tu token aquí]
   ```

### Paso 2: Desplegar en Render (10 minutos)

Una vez que hagas push exitosamente:

#### A) Si YA TIENES un servicio en Render que no funciona

1. Ve a: https://dashboard.render.com
2. Encuentra tu servicio "metodo-comedia" (o como lo hayas llamado)
3. Click en el servicio
4. Click en **"Manual Deploy"** → **"Deploy latest commit"**
5. Espera 5-10 minutos
6. Revisa los **Logs** para ver si hay errores

Si sigue fallando, ve al **Paso B**.

#### B) Si NO TIENES servicio o quieres empezar de cero

1. Ve a: https://dashboard.render.com
2. Click en **"New +"** → **"Web Service"**

3. **Connect Repository:**
   - Si no aparece tu repo, click en **"Configure GitHub"**
   - Autoriza a Render a acceder a tu repositorio
   - Selecciona el repositorio **"metodo"**

4. **Service Configuration:**
   ```
   Name: metodo-comedia
   Environment: Python 3
   Branch: main
   Root Directory: (dejar vacío)
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn src.app:app --bind 0.0.0.0:$PORT
   ```

5. **Plan:** Selecciona **"Free"**

6. **Environment Variables:**

   Click en **"Advanced"** → **"Add Environment Variable"**

   Agrega estas variables (¡CÓPIALAS DE TU ARCHIVO .env!):

   | Key | Value |
   |-----|-------|
   | `SUPABASE_URL` | Tu URL de Supabase |
   | `SUPABASE_KEY` | Tu key anon/public |
   | `SUPABASE_SERVICE_KEY` | Tu service_role key |
   | `GEMINI_API_KEY` | Tu API key de Gemini |
   | `FLASK_ENV` | `production` |
   | `FLASK_DEBUG` | `False` |

   **Opcionales:**
   | Key | Value |
   |-----|-------|
   | `TODOIST_TOKEN` | Tu token de Todoist |
   | `TODOIST_PROJECT_ID` | `2362882414` |

7. Click en **"Create Web Service"**

8. **Espera 5-10 minutos** mientras Render:
   - Clona tu repositorio
   - Instala dependencias
   - Inicia la app

9. **Verifica que funcione:**

   Render te dará una URL como: `https://metodo-comedia-xxxx.onrender.com`

   Prueba estos endpoints:

   ```
   https://tu-app.onrender.com/health
   → Debe devolver: {"status": "healthy", ...}

   https://tu-app.onrender.com/
   → Debe cargar tu app con CSS y todo
   ```

---

## 🐛 Si Render Sigue Fallando

### Ver los Logs

1. Render Dashboard → Tu servicio → **"Logs"**
2. Busca mensajes de error

### Errores Comunes:

#### Error 1: "Build failed"
```
ERROR: Could not find a version that satisfies the requirement...
```

**Solución:**
- Verifica que `requirements.txt` esté en la raíz del proyecto
- No debe tener versiones incompatibles

#### Error 2: "Application failed to respond"
```
Your service is failing because it is not responding to HTTP requests
```

**Solución:**
- Verifica que el Start Command sea exactamente:
  ```
  gunicorn src.app:app --bind 0.0.0.0:$PORT
  ```
- Asegúrate de que las variables de entorno estén configuradas

#### Error 3: "ModuleNotFoundError"
```
ModuleNotFoundError: No module named 'src'
```

**Solución:**
- Verifica que exista `src/__init__.py` ✅ (ya lo tienes)
- El Start Command debe ser `src.app:app` (con punto, no slash)

#### Error 4: "Configuration error"
```
Configuration error: Missing GEMINI_API_KEY
```

**Solución:**
- Ve a Render Dashboard → Environment
- Agrega las variables de entorno que faltan
- Haz Manual Deploy después de agregarlas

---

## 📋 Checklist Final

Antes de declarar victoria, verifica:

- [ ] Puedes acceder a `https://tu-app.onrender.com/health`
- [ ] La página principal carga con CSS
- [ ] Puedes crear un chiste nuevo
- [ ] El análisis de IA funciona
- [ ] No hay errores en los logs de Render

---

## 🎯 Comando Rápido (Todo en Uno)

Si solo quieres hacer push rápido:

```bash
# Opción 1: Con GitHub CLI
gh auth login
git push

# Opción 2: Con SSH
git remote set-url origin git@github.com:albertomartinezdelacasa/metodo.git
git push
```

Luego ve a Render Dashboard y haz "Manual Deploy".

---

## 📞 ¿Qué error específico estás viendo?

Para ayudarte mejor, necesito saber:

1. **¿Ya tienes un servicio en Render?** (Sí/No)
2. **¿Qué mensaje de error ves?** (copia los logs)
3. **¿En qué paso estás?** (push a GitHub / deploy en Render / otro)

Con esa info puedo darte una solución exacta.

---

## ✅ Script de Verificación

Ejecuta esto para ver si todo está OK:

```bash
# Ver si hay cambios sin commit
git status

# Ver configuración de git
git remote -v

# Probar autenticación
gh auth status  # Si tienes GitHub CLI
```

---

**💡 Tip:** Si todo falla, la forma más fácil es:

1. Eliminar el servicio actual en Render (si existe)
2. Crear uno nuevo desde cero siguiendo el Paso 2B
3. Asegurarte de agregar TODAS las variables de entorno

El 90% de los problemas en Render son por variables de entorno faltantes.
