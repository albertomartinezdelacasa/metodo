# 🚂 DEPLOY EN RAILWAY - MÉTODO COMEDIA

Guía paso a paso para desplegar la aplicación en Railway.app

---

## ✅ **Pre-requisitos**

Antes de empezar, asegúrate de tener:

1. ✅ **Cuenta en Railway:** https://railway.app (gratis, login con GitHub)
2. ✅ **Supabase configurado:** Base de datos con el schema ejecutado
3. ✅ **API Key de Gemini:** https://makersuite.google.com/app/apikey
4. ✅ **Credenciales listas:**
   ```
   SUPABASE_URL=https://pwztxtbwomiftdmogwjq.supabase.co
   SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB3enR4dGJ3b21pZnRkbW9nd2pxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMzNzEyMTEsImV4cCI6MjA3ODk0NzIxMX0.MhfwaUMEMIauWsJ55GRHm5qB7IWxbRue2N_VuujnNUs
   GEMINI_API_KEY=[tu key aquí]
   ```

---

## 🚀 **PASO 1: Crear Proyecto en Railway**

### **Opción A: Deploy desde GitHub (Recomendado)**

1. Ve a **https://railway.app**
2. Click en **"Start a New Project"**
3. Selecciona **"Deploy from GitHub repo"**
4. Conecta tu cuenta de GitHub si no lo has hecho
5. Busca y selecciona el repositorio: **albertomartinezdelacasa/metodo**
6. Selecciona la branch: **claude/continue-app-development-01HjmzLs3mmvzjbQRvcgBnVb**
7. Click en **"Deploy Now"**

### **Opción B: Deploy con Railway CLI**

```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# Crear proyecto
railway init

# Deploy
railway up
```

---

## ⚙️ **PASO 2: Configurar Variables de Entorno**

Una vez creado el proyecto:

1. En el dashboard de Railway, click en tu proyecto
2. Ve a la pestaña **"Variables"**
3. Click en **"+ New Variable"** para cada una:

```bash
# Supabase (REQUERIDO)
SUPABASE_URL=https://pwztxtbwomiftdmogwjq.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB3enR4dGJ3b21pZnRkbW9nd2pxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMzNzEyMTEsImV4cCI6MjA3ODk0NzIxMX0.MhfwaUMEMIauWsJ55GRHm5qB7IWxbRue2N_VuujnNUs

# Google Gemini AI (REQUERIDO)
GEMINI_API_KEY=[Obtén en https://makersuite.google.com/app/apikey]

# Flask Config
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=[genera una clave aleatoria segura]

# Todoist (OPCIONAL)
TODOIST_TOKEN=[tu token si quieres integración]
TODOIST_PROJECT_ID=2362882414
```

4. Click **"Deploy"** o espera el auto-redeploy

---

## 🔍 **PASO 3: Verificar el Deploy**

### **Monitorear Logs:**

1. En Railway, ve a la pestaña **"Deployments"**
2. Click en el deployment activo
3. Verás los logs en tiempo real:

```
Building...
Installing dependencies from requirements.txt
Starting gunicorn...
✓ Server running on port 5000
```

### **Obtener URL:**

1. En tu proyecto de Railway, ve a **"Settings"**
2. Busca la sección **"Domains"**
3. Click en **"Generate Domain"**
4. Railway te dará una URL como:
   ```
   https://metodo-production-xxxx.up.railway.app
   ```
5. **¡Copia esta URL!**

---

## ✅ **PASO 4: Probar la Aplicación**

1. **Abre la URL** en tu navegador
2. **Primera vez tarda ~30 segundos** (cold start)
3. Deberías ver la interfaz de **Método Comedia**
4. **Prueba:**
   - Escribe un chiste
   - Click en "💾 Guardar Chiste"
   - Ve a "📋 Mis Chistes"
   - Click en "🔍 Análisis General"
   - **¡Debería funcionar!**

---

## 📱 **PASO 5: Instalar PWA en el Móvil**

### **iPhone (Safari):**
1. Abre la URL de Railway en Safari
2. Toca el botón **Compartir** (cuadrito con flecha)
3. Scroll y selecciona **"Añadir a pantalla de inicio"**
4. Toca **"Añadir"**
5. ¡Listo! Tendrás un icono como app nativa

### **Android (Chrome):**
1. Abre la URL de Railway en Chrome
2. Verás popup **"Instalar app"**
3. Toca **"Instalar"**
4. O ve a **⋮ → Añadir a pantalla de inicio**
5. ¡Funciona offline y como app nativa!

---

## 🔧 **Troubleshooting**

### **Error: "Application failed to respond"**

**Causa:** Variables de entorno faltantes

**Solución:**
1. Verifica que agregaste las 3 variables requeridas:
   - SUPABASE_URL
   - SUPABASE_KEY
   - GEMINI_API_KEY
2. Redeploy: Settings → Redeploy

---

### **Error: "Configuration error"**

**Causa:** Variables mal configuradas

**Solución:**
1. Ve a Variables en Railway
2. Verifica que no haya espacios extra
3. Asegúrate de que las URLs empiezan con `https://`
4. Redeploy

---

### **Los chistes no se guardan**

**Causa:** Supabase no configurado correctamente

**Solución:**
1. Verifica que ejecutaste el SQL schema en Supabase
2. Verifica las credenciales en Railway
3. Ve a Railway → Logs y busca errores de BD

---

### **Análisis de IA no funciona**

**Causa:** GEMINI_API_KEY inválida o límite alcanzado

**Solución:**
1. Verifica la key en: https://makersuite.google.com/app/apikey
2. Límite free tier: 1500 req/día
3. Espera 24h o usa otra cuenta de Google

---

## 📊 **Railway Free Tier**

**Límites:**
- ✅ $5 USD de crédito gratis/mes
- ✅ 500 horas de ejecución/mes
- ✅ 100 GB de ancho de banda
- ✅ Sin límite de proyectos
- ⚠️ Duerme después de inactividad (wake ~5-10 segundos)

**Suficiente para:**
- Uso personal
- Testing
- Proyectos pequeños/medianos
- ~200-500 usuarios activos/mes

---

## 🔄 **Auto-Deploy desde GitHub**

Railway detecta automáticamente cambios en tu branch:

1. Haces `git push` a tu branch
2. Railway detecta el cambio
3. Hace build automático
4. Redeploy en ~1-2 minutos
5. ¡Listo! Cambios en producción

---

## 📝 **Comandos Útiles de Railway CLI**

```bash
# Ver logs en vivo
railway logs

# Abrir shell en producción
railway shell

# Ver variables de entorno
railway variables

# Abrir la app en navegador
railway open

# Ver status
railway status
```

---

## 🎯 **Checklist Final**

Antes de considerar el deploy completo, verifica:

- [ ] Proyecto creado en Railway
- [ ] Variables de entorno configuradas (3 mínimo)
- [ ] Deploy exitoso (sin errores en logs)
- [ ] URL generada y accesible
- [ ] Supabase schema ejecutado
- [ ] Migración realidad_absurda ejecutada
- [ ] Puedes guardar un chiste
- [ ] Puedes analizar un chiste
- [ ] PWA instalable en móvil
- [ ] Auto-deploy configurado (GitHub)

---

## 🚀 **URLs Importantes**

- **Railway Dashboard:** https://railway.app/dashboard
- **Railway Docs:** https://docs.railway.app
- **Tu App:** https://metodo-production-[tu-id].up.railway.app
- **Supabase:** https://app.supabase.com
- **Gemini API:** https://makersuite.google.com/app/apikey

---

## 📞 **Soporte**

**Problemas con Railway:**
- Discord: https://discord.gg/railway
- Docs: https://docs.railway.app

**Problemas con la App:**
- GitHub Issues: https://github.com/albertomartinezdelacasa/metodo/issues

---

**¡Listo para producción! 🎉**

Tu app está desplegada en Railway y accesible desde cualquier dispositivo.
