# 🚀 Guía de Deployment - Método Comedia

## ✅ Estado Actual

- ✅ Todo el código implementado (Backend + Frontend)
- ✅ Base de datos migrada en Supabase
- ✅ Commit de Git creado
- ⏳ **PENDIENTE: Push a GitHub**
- ⏸️ Deploy a Render.com

---

## 📤 PASO 1: Push a GitHub (ACCIÓN REQUERIDA)

### Problema Actual
Git está usando la cuenta incorrecta (`albertoMHR` en lugar de `albertomartinezdelacasa`).

### Solución A: GitHub Desktop (MÁS FÁCIL)
1. Abre **GitHub Desktop**
2. Asegúrate de estar logueado con la cuenta: `albertomartinezdelacasa`
3. Ve a `File → Add Local Repository`
4. Selecciona la carpeta: `C:\Users\alber\OneDrive\Documentos\memoria_claude\metodo`
5. Click en **"Push origin"** (botón azul arriba a la derecha)

### Solución B: Terminal con Token
```bash
# 1. Genera un Personal Access Token en GitHub
# Ve a: https://github.com/settings/tokens
# Click: "Generate new token (classic)"
# Selecciona: repo (todos los permisos)
# Copia el token generado

# 2. En la terminal:
cd "C:\Users\alber\OneDrive\Documentos\memoria_claude\metodo"

# 3. Push usando el token como contraseña
git push -u origin main
# Usuario: albertomartinezdelacasa
# Password: <pega tu token aquí>
```

### Solución C: Configurar Credenciales
```bash
# Actualizar credenciales de Windows
git credential-manager-core erase "https://github.com"

# Luego hacer push (te pedirá login)
git push -u origin main
```

---

## 🌐 PASO 2: Deploy en Render.com

Una vez el código esté en GitHub, sigue estos pasos:

### 1. Crear Cuenta en Render
- Ve a: https://render.com
- Click en "Get Started for Free"
- **Conéctate con tu cuenta de GitHub** (`albertomartinezdelacasa`)

### 2. Crear Web Service
1. Click en **"New +"** → **"Web Service"**
2. Busca el repositorio: `metodo`
3. Click en **"Connect"**

### 3. Configuración del Service

**Configuración Básica:**
- **Name**: `metodo-comedia` (o el nombre que quieras)
- **Region**: Frankfurt (o el más cercano a España)
- **Branch**: `main`
- **Root Directory**: (dejar vacío)
- **Runtime**: `Python 3`

**Build & Deploy:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn src.app:app`

**Instance Type:**
- Selecciona: **Free** (0$/mes)

### 4. Variables de Entorno

En la sección **"Environment Variables"**, agrega las siguientes variables (cópialas de tu archivo `.env`):

```bash
# Supabase (OBLIGATORIAS)
SUPABASE_URL=https://tuproyecto.supabase.co
SUPABASE_KEY=eyJhbGci...
SUPABASE_SERVICE_KEY=eyJhbGci...

# Google Gemini AI (OBLIGATORIA)
GEMINI_API_KEY=AIzaSy...

# Todoist (OPCIONAL)
TODOIST_TOKEN=c4cee5abfa79870a2c1e4767e4228eb3846d2651
TODOIST_PROJECT_ID=2362882414

# Flask
FLASK_ENV=production
FLASK_DEBUG=False
PORT=5000
```

**IMPORTANTE:**
- ✅ Copia los valores EXACTOS de tu archivo `.env` local
- ✅ No incluyas comillas en los valores
- ✅ Verifica que `SUPABASE_SERVICE_KEY` sea la "service_role" key, no la "anon" key

### 5. Deploy

1. Click en **"Create Web Service"**
2. Render empezará a construir tu app (tarda 2-3 minutos)
3. Verás logs en tiempo real
4. Cuando veas "Build successful" y "Deploy live", ¡está listo! 🎉

### 6. Obtener URL

Tu app estará disponible en:
```
https://metodo-comedia.onrender.com
```

(o el nombre que elegiste)

---

## 📱 PASO 3: Probar PWA en iPhone

### 1. Abre la URL en Safari (iPhone)
```
https://tu-app.onrender.com
```

**IMPORTANTE:** Debe ser Safari, no Chrome.

### 2. Instalar como App
1. Toca el botón de "Compartir" (cuadrado con flecha hacia arriba)
2. Scroll hacia abajo
3. Toca **"Agregar a pantalla de inicio"**
4. Confirma el nombre y toca **"Agregar"**

### 3. Abrir la App
- La app aparecerá en tu pantalla de inicio como una app nativa
- Abre la app (se abrirá en pantalla completa sin la barra de Safari)
- ¡Listo! Ya tienes tu PWA instalada 📱✨

---

## ⚠️ NOTAS IMPORTANTES

### Limitaciones del Free Tier de Render
- ✅ **Gratis para siempre**
- ⏰ **Se duerme después de 15 minutos sin uso**
- ⏱️ **Tarda 30-60 segundos en despertar** cuando alguien accede
- 🔄 **750 horas/mes gratis** (suficiente para uso personal)

### Primera carga lenta
La primera vez que abras la app después de que se haya dormido:
1. Verás un spinner o pantalla de carga
2. Espera 30-60 segundos
3. La app se "despertará" y funcionará normal
4. Las siguientes cargas serán instantáneas (mientras esté despierta)

### Si necesitas que esté siempre activa
Render ofrece planes pagos desde $7/mes que mantienen la app siempre despierta.

---

## 🔍 VERIFICACIÓN POST-DEPLOY

### 1. Health Check
Abre en tu navegador:
```
https://tu-app.onrender.com/health
```

Deberías ver:
```json
{
  "status": "healthy",
  "service": "metodo-comedia",
  "version": "1.0.0"
}
```

### 2. Prueba de Funcionalidad
1. ✅ Crear un chiste nuevo
2. ✅ Analizar con IA básica
3. ✅ Analizar conceptos
4. ✅ Analizar rupturas
5. ✅ Crear entrada de bitácora
6. ✅ Filtrar chistes por estado

### 3. PWA Offline
1. Abre la app en iPhone
2. Activa el modo avión
3. La app debería seguir mostrando la interfaz (aunque no podrá guardar datos nuevos)
4. Desactiva el modo avión
5. Los datos se sincronizarán automáticamente

---

## 🆘 TROUBLESHOOTING

### "Application failed to start"
- ✅ Verifica que todas las variables de entorno estén configuradas
- ✅ Revisa los logs en Render para ver el error específico
- ✅ Asegúrate que `gunicorn` esté en `requirements.txt`

### "Database connection failed"
- ✅ Verifica que `SUPABASE_URL` y `SUPABASE_KEY` sean correctos
- ✅ Asegúrate de usar la "anon" key para `SUPABASE_KEY`
- ✅ Usa la "service_role" key para `SUPABASE_SERVICE_KEY`

### "AI analysis not working"
- ✅ Verifica que `GEMINI_API_KEY` sea válida
- ✅ Confirma que no hayas excedido el límite de 1500 requests/día

### PWA no se instala en iPhone
- ✅ Debe ser HTTPS (Render usa HTTPS automáticamente)
- ✅ Debe abrirse en Safari, no en Chrome
- ✅ Verifica que `manifest.json` y `service-worker.js` se carguen correctamente

---

## 📊 MONITOREO

### Ver Logs en Tiempo Real
1. Ve a tu dashboard de Render
2. Click en tu web service
3. Pestaña "Logs"
4. Verás todos los requests y errores en tiempo real

### Métricas
Render te muestra:
- CPU usage
- Memory usage
- Request count
- Response times

---

## 🎉 ¡YA CASI ESTÁS!

**Checklist Final:**
- [ ] Push a GitHub completado
- [ ] Web Service creado en Render
- [ ] Variables de entorno configuradas
- [ ] Deploy exitoso (sin errores en logs)
- [ ] Health check responde OK
- [ ] App funciona en navegador
- [ ] PWA instalada en iPhone
- [ ] Todas las funciones probadas

**Una vez completado todo, tendrás:**
- ✅ Una PWA profesional funcionando 24/7
- ✅ Análisis de IA ilimitados (1500/día gratis)
- ✅ Base de datos robusta en Supabase
- ✅ Accesible desde cualquier dispositivo
- ✅ Instalable en iPhone como app nativa

---

**¿Necesitas ayuda?**
- Revisa los logs de Render
- Verifica las variables de entorno
- Prueba el health check endpoint
- Contacta si hay algún error específico

**¡Éxito con tu deploy! 🚀**
