# 🗄️ SETUP SUPABASE - GUÍA DEFINITIVA

## ✅ PASO A PASO PARA CONFIGURAR TU BASE DE DATOS

### **📋 Resumen:**
- 8 tablas principales
- 3 triggers automáticos
- 2 vistas útiles
- Tags pre-cargados
- Versioning automático de chistes

---

## 🚀 **PASOS:**

### **1. Crear Cuenta en Supabase (GRATIS)**

1. Ve a: https://supabase.com
2. Click en **"Start your project"**
3. Login con GitHub/Google
4. Click **"New Project"**
5. Rellena:
   - **Name:** `metodo-comedia`
   - **Database Password:** (copia y guarda esta contraseña)
   - **Region:** Elige la más cercana
   - **Pricing Plan:** FREE
6. Click **"Create new project"**
7. **Espera 2-3 minutos** mientras Supabase crea tu base de datos

---

### **2. Obtener Credenciales (IMPORTANTE)**

Una vez creado el proyecto:

1. Ve a **Settings** (icono engranaje, menú izquierdo)
2. Click en **API**
3. Copia estos 2 valores (los necesitarás para Render):

```
Project URL:
https://xxxxxxxxxxxxx.supabase.co
👆 Esta es tu SUPABASE_URL

anon/public key:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ey...
👆 Esta es tu SUPABASE_KEY
```

**✨ GUÁRDALAS EN UN LUGAR SEGURO** (las usarás en paso 5)

---

### **3. Ejecutar el Schema SQL**

1. En Supabase, ve a **SQL Editor** (icono </> en menú izquierdo)
2. Click en **"+ New query"**
3. **Copia TODO el contenido** del archivo `database_schema.sql` (330 líneas)
4. Pégalo en el editor
5. Click en **"RUN"** (botón verde abajo a la derecha)
6. **Espera 5-10 segundos**

### **✅ Verificación:**

Deberías ver en la parte inferior:

```
Success. Rows returned: 8

chistes
analisis_ia
bitacora
chistes_presentaciones
chistes_tags
presentaciones
tags
versiones_chiste
```

Si ves esto: **¡Perfecto! ✅ La base de datos está lista.**

---

### **4. Verificar que TODO se creó correctamente**

En el SQL Editor, ejecuta esta query de verificación:

```sql
-- Verificar tablas
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

-- Verificar tags pre-cargados
SELECT COUNT(*) as total_tags FROM tags;

-- Verificar triggers
SELECT trigger_name, event_object_table
FROM information_schema.triggers
WHERE trigger_schema = 'public';
```

**Deberías ver:**
- ✅ 8 tablas
- ✅ 18 tags pre-cargados
- ✅ 3 triggers (update_chistes_modtime, save_version_before_update, update_bitacora_modtime)

---

### **5. Configurar Variables de Entorno en Render**

Ahora que tienes Supabase listo, configura Render:

1. Ve a: https://dashboard.render.com
2. Click en tu servicio **"metodo-comedia"**
3. Ve a **"Environment"** (menú izquierdo)
4. Click **"Add Environment Variable"** y agrega:

```bash
# SUPABASE (del paso 2)
SUPABASE_URL = https://xxxxxxxxxxxxx.supabase.co
SUPABASE_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# GEMINI AI (obtén gratis en https://makersuite.google.com/app/apikey)
GEMINI_API_KEY = AIzaSy...

# TODOIST (opcional)
TODOIST_TOKEN = (tu token, opcional)
TODOIST_PROJECT_ID = 2362882414
```

5. Click **"Save Changes"**
6. Render hará **redeploy automático** (2-3 minutos)

---

### **6. Verificar que la App Funciona**

1. Espera a que Render termine el deploy
2. Abre la URL de tu app: `https://metodo-comedia-xxxx.onrender.com`
3. **Primera vez tarda 30-60 segundos** (free tier despierta el servidor)
4. Deberías ver la interfaz de Método Comedia
5. **Prueba escribir un chiste y guardarlo**
6. Ve a Supabase → **Table Editor** → tabla `chistes` → deberías ver tu chiste guardado ✅

---

## 🎯 **ESTRUCTURA DE LA BASE DE DATOS**

### **Tablas Principales:**

#### **1. `chistes`** - Tus chistes
Campos: titulo, contenido, estado, calificacion, veces_usado, concepto, premisa, remate, notas

#### **2. `analisis_ia`** - Resultados de análisis con IA
Campos: estructura, tecnicas, puntos_fuertes, puntos_debiles, scores, tipo_concepto, tipo_ruptura

#### **3. `tags`** - Categorización
18 tags pre-cargados: familia, tecnologia, exageración, wordplay, etc.

#### **4. `chistes_tags`** - Relación chistes ↔ tags

#### **5. `versiones_chiste`** - Historial automático
Cada vez que editas un chiste, se guarda la versión anterior automáticamente

#### **6. `presentaciones`** - Shows/eventos
Tracking de dónde usaste tus chistes

#### **7. `chistes_presentaciones`** - Relación chistes ↔ shows

#### **8. `bitacora`** - Diario de comediante
Reflexiones, ideas, observaciones

---

## 🔧 **TRIGGERS AUTOMÁTICOS**

### **1. Auto-actualizar `fecha_modificacion`**
Cada vez que editas un chiste, se actualiza automáticamente la fecha.

### **2. Versioning Automático**
Antes de guardar cambios en un chiste, se guarda automáticamente la versión anterior.

### **3. Bitácora `modificado_en`**
Actualiza fecha de modificación en entradas de bitácora.

---

## 📊 **VISTAS ÚTILES**

### **`chistes_con_analisis`**
Chistes con su último análisis de IA en una sola query.

```sql
SELECT * FROM chistes_con_analisis;
```

### **`estadisticas_chistes`**
Estadísticas agrupadas por estado.

```sql
SELECT * FROM estadisticas_chistes;
```

---

## ⚠️ **TROUBLESHOOTING**

### **Error: "relation already exists"**
✅ **Normal** - Significa que la tabla ya existe. El script usa `CREATE TABLE IF NOT EXISTS`, así que es seguro ejecutarlo múltiples veces.

### **No veo los tags pre-cargados**
Ejecuta manualmente:
```sql
SELECT * FROM tags;
```
Si está vacío, ejecuta la sección de DATOS INICIALES del `database_schema.sql`.

### **La app dice "Configuration error"**
Verifica que en Render tengas configuradas las 3 variables:
- SUPABASE_URL
- SUPABASE_KEY
- GEMINI_API_KEY

### **Los chistes no se guardan**
1. Ve a Supabase → SQL Editor
2. Ejecuta: `SELECT * FROM chistes;`
3. Si ves error, revisa que el schema se ejecutó correctamente

---

## 🎉 **¡LISTO!**

Tu base de datos está 100% configurada y lista para:
- ✅ Guardar chistes
- ✅ Analizar con IA
- ✅ Tracking de versiones automático
- ✅ Organizar con tags
- ✅ Llevar bitácora
- ✅ Registrar shows

---

## 📞 **CREDENCIALES FINALES PARA RENDER:**

```bash
# Copia esto y pégalo en Render → Environment:

SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
GEMINI_API_KEY=AIzaSy...
FLASK_ENV=production
FLASK_DEBUG=False
PORT=10000
```

Guarda y espera el redeploy. ¡Tu app estará funcionando en 2-3 minutos!
