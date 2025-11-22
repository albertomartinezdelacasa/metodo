# 📱 Guía de Gestión Móvil - Método Comedia

Esta guía te muestra cómo administrar tu proyecto **Método Comedia** completamente desde tu móvil usando GitHub Mobile y la PWA.

---

## 🎯 ¿Qué puedes hacer desde el móvil?

### 1. **Gestión de Chistes** (PWA)
- ✅ Crear y editar chistes
- ✅ Analizar chistes con IA
- ✅ Ver mejoras sugeridas
- ✅ Gestionar bitácora
- ✅ Generar ideas (brainstorm)

### 2. **Gestión de Código** (GitHub Issues)
- ✅ Ejecutar tests
- ✅ Desplegar a Render
- ✅ Crear backups de base de datos
- ✅ Analizar calidad de código
- ✅ Actualizar dependencias
- ✅ Ver historial de comandos

---

## 📲 Instalación y Setup

### Paso 1: Instala la PWA en tu iPhone

1. Abre Safari y ve a tu app: `https://TU-APP.onrender.com`
2. Toca el botón **Compartir** (icono de cuadrado con flecha)
3. Selecciona **"Agregar a pantalla de inicio"**
4. Toca **"Agregar"**
5. ¡Listo! Ahora tienes el ícono en tu pantalla de inicio

**Nota:** La PWA funciona offline gracias al Service Worker.

### Paso 2: Instala GitHub Mobile

1. Descarga **GitHub Mobile** desde el App Store
2. Inicia sesión con tu cuenta de GitHub
3. Busca tu repositorio: `metodo`
4. Activa las notificaciones para estar al tanto de los resultados

### Paso 3: Configura los Enlaces en la PWA

Los enlaces en el tab **"Gestión"** de la PWA están configurados con placeholders. Debes actualizarlos:

**Edita el archivo:** `templates/index.html`

**Busca y reemplaza:**
```html
<!-- Antes -->
<a href="https://github.com/TU_USUARIO/metodo/issues/new?template=mobile-run-tests.yml"

<!-- Después (reemplaza TU_USUARIO con tu usuario de GitHub) -->
<a href="https://github.com/albertoromgar/metodo/issues/new?template=mobile-run-tests.yml"
```

**Haz esto para todos los enlaces:**
- `mobile-run-tests.yml`
- `mobile-deploy.yml`
- `mobile-backup-db.yml`
- `mobile-analyze-code.yml`
- `mobile-update-deps.yml`

---

## 🚀 Cómo Usar el Sistema desde el Móvil

### Workflow Recomendado

#### **Opción A: Usar la PWA (Gestión de Contenido)**

1. Abre la app desde tu pantalla de inicio
2. Ve al tab **"Escribir"**
3. Escribe un chiste nuevo
4. Toca **"Analizar con IA"**
5. Revisa las sugerencias de mejora
6. Guarda el chiste mejorado
7. Ve al tab **"Bitácora"** para registrar tus ideas

**Ventajas:**
- Funciona offline
- Interfaz optimizada para móvil
- Acceso rápido a IA

#### **Opción B: Usar GitHub Issues (Gestión Técnica)**

1. Abre la PWA y ve al tab **"⚙️ Gestión"**
2. Toca el botón de la acción que quieres realizar (ej: **Ejecutar Tests**)
3. Esto abrirá GitHub en Safari con un formulario pre-llenado
4. Completa los detalles adicionales si es necesario
5. Toca **"Submit new issue"**
6. GitHub Actions ejecutará el comando automáticamente
7. Recibirás una notificación cuando termine
8. El issue se cerrará automáticamente si tiene éxito

**Comandos disponibles:**

| Comando | ¿Qué hace? | ¿Cuándo usarlo? |
|---------|-----------|-----------------|
| 🧪 **Tests** | Ejecuta pytest completo | Antes de hacer deploy, después de cambios |
| 🚀 **Deploy** | Despliega a Render | Cuando quieras publicar cambios |
| 💾 **Backup BD** | Crea backup de Supabase | Antes de migraciones, semanalmente |
| 🔍 **Análisis** | Ejecuta pylint | Para revisar calidad de código |
| 📦 **Dependencias** | Revisa paquetes outdated | Mensualmente, para seguridad |

---

## 📊 Ejemplos de Uso Real

### Ejemplo 1: Ejecutar Tests antes de Deploy

**Situación:** Hiciste cambios en el código y quieres asegurarte de que todo funciona antes de desplegar.

**Pasos:**

1. Abre la PWA → Tab **"Gestión"**
2. Toca **"Ejecutar Tests →"**
3. Se abre GitHub en Safari
4. Marca las opciones:
   - ✅ Run all tests
   - ✅ Verbose output
5. Toca **"Submit new issue"**
6. Espera 2-3 minutos
7. Recibes notificación de GitHub Mobile
8. Revisa los resultados en el issue
9. Si todo está ✅, ve al tab **"Gestión"** y toca **"Deploy →"**

### Ejemplo 2: Backup antes de Migración

**Situación:** Vas a ejecutar una migración de base de datos y quieres un backup de seguridad.

**Pasos:**

1. PWA → Tab **"Gestión"** → **"Backup BD →"**
2. En el formulario:
   - ✅ Include all tables
   - ✅ Compress backup
   - Reason: "Antes de migración de nuevos campos"
3. Toca **"Submit new issue"**
4. Espera confirmación en GitHub Mobile
5. Procede con la migración con tranquilidad

### Ejemplo 3: Análisis de Código

**Situación:** Quieres revisar la calidad del código antes de un pull request.

**Pasos:**

1. PWA → Tab **"Gestión"** → **"Analizar →"**
2. Selecciona:
   - Focus Area: **All code**
   - ✅ Check all Python files
   - ✅ Include security scan
3. Toca **"Submit new issue"**
4. Revisa el análisis cuando termine
5. El issue incluirá el reporte completo de pylint

---

## 🔗 Workflow Híbrido (PWA + GitHub)

### Caso de Uso: Añadir Feature + Deploy

**Escenario:** Estás en un café y quieres agregar una nueva funcionalidad y desplegarla.

**Workflow:**

1. **Investigación** (PWA)
   - Abre la PWA
   - Ve al tab **"Gestión"** → **"Enlaces Rápidos"**
   - Toca **"Panel de Supabase"** para revisar la estructura de DB

2. **Edición de Código** (GitHub Mobile)
   - Abre GitHub Mobile
   - Navega a `src/routes/jokes.py`
   - Toca el icono de **"..."** → **"Edit file"**
   - Haz tus cambios
   - Commit directamente a `main` (o crea un branch)

3. **Testing** (GitHub Issues)
   - Vuelve a la PWA → Tab **"Gestión"**
   - Toca **"Ejecutar Tests →"**
   - Espera confirmación

4. **Deploy** (GitHub Issues)
   - Si tests pasan ✅
   - Tab **"Gestión"** → **"Deploy →"**
   - Completa el formulario con los cambios que hiciste
   - Submit

5. **Verificación** (PWA)
   - Espera 5-10 min (tiempo de deploy de Render)
   - Recarga la PWA
   - Prueba la nueva funcionalidad

---

## ⚙️ Configuración Avanzada

### Personalizar GitHub Actions

Los workflows están en: `.github/workflows/mobile-commands.yml`

**Para agregar un nuevo comando:**

1. Edita `mobile-commands.yml`
2. Agrega un nuevo `case` en el switch:
```yaml
custom-command)
  echo "Ejecutando comando personalizado..."
  python mi_script.py
  ;;
```
3. Crea un nuevo template en `.github/ISSUE_TEMPLATE/mobile-custom.yml`

### Agregar más enlaces rápidos

Edita `templates/index.html` en la sección **"Enlaces Rápidos"**:

```html
<a href="https://tu-servicio.com" target="_blank" class="block text-blue-600 hover:underline">
    → Mi Servicio Custom
</a>
```

---

## 🛡️ Seguridad y Buenas Prácticas

### ✅ Hacer

- Ejecuta tests antes de cada deploy
- Crea backups antes de migraciones
- Revisa los logs de GitHub Actions
- Usa branches para features grandes
- Mantén las dependencias actualizadas

### ❌ Evitar

- NO hagas deploy sin tests
- NO edites archivos críticos sin backup
- NO ignores los errores en los issues
- NO compartas los enlaces de issues públicamente (contienen tokens)
- NO hagas commits directos a `main` en producción (usa branches)

---

## 📊 Monitoreo y Estadísticas

### Dashboard en la PWA

El tab **"Gestión"** incluye un dashboard con:

- **Total de Chistes:** Chistes activos (no eliminados)
- **Análisis IA:** Chistes que tienen análisis de IA
- **Rating Promedio:** Calificación promedio de tus chistes
- **Total de Shows:** Presentaciones registradas

**Actualizar estadísticas:**
Toca **"🔄 Actualizar estadísticas"** debajo del dashboard.

### Ver historial de comandos

En el tab **"Gestión"**, toca **"📊 Ver Issues"** para ver:
- Todos los comandos ejecutados
- Cuáles fallaron
- Logs completos de cada ejecución

---

## 🐛 Troubleshooting

### La PWA no se instala en iPhone

**Solución:**
- Usa Safari (no Chrome)
- Asegúrate de tener HTTPS (Render lo provee automáticamente)
- Intenta desde modo incógnito primero

### Los enlaces de GitHub no funcionan

**Problema:** Los templates de issues no se encuentran

**Solución:**
1. Asegúrate de haber hecho commit de `.github/ISSUE_TEMPLATE/`
2. Espera 5 min después del commit (GitHub indexa los templates)
3. Verifica que los archivos `.yml` no tengan errores de sintaxis

### GitHub Actions no se ejecuta

**Problema:** El issue se crea pero el workflow no corre

**Solución:**
1. Ve a GitHub → **Settings** → **Actions** → **General**
2. Permite "Read and write permissions"
3. Habilita "Allow GitHub Actions to create and approve pull requests"
4. Guarda cambios

### El deploy falla

**Problema:** Render no puede desplegar

**Solución:**
1. Revisa los logs en Render Dashboard
2. Verifica que `requirements.txt` esté actualizado
3. Asegúrate de que todas las env vars están en Render
4. Revisa que no haya errores de sintaxis en el código

### Las estadísticas no cargan

**Problema:** El dashboard muestra "-" en todos los números

**Solución:**
1. Abre la consola del navegador (Safari → Develop → Console)
2. Busca errores de red
3. Verifica que la API esté online (abre `https://tu-app.onrender.com/api/jokes/`)
4. Revisa las variables de entorno de Supabase

---

## 🎓 Tips y Trucos

### Usar Siri Shortcuts (Avanzado)

Puedes crear un Shortcut de iOS que:
1. Abra la PWA
2. Navegue directamente al tab de Gestión
3. Abra un comando específico de GitHub

**Ejemplo:** "Hey Siri, ejecuta tests de Comedia"

### Notificaciones Push

Para recibir notificaciones inmediatas:

1. Abre GitHub Mobile
2. Ve a Settings → Notifications
3. Activa **"Push notifications"**
4. Activa **"Participating"** (para issues que creas)

### Offline Mode

La PWA funciona offline para:
- Ver chistes guardados (últimos 50)
- Leer análisis previos
- Navegar la bitácora

**NO funciona offline:**
- Crear nuevos análisis de IA (requiere internet)
- Sincronizar con base de datos
- Ejecutar comandos de GitHub

---

## 📚 Recursos Adicionales

### Enlaces Útiles

- **GitHub Actions Docs:** https://docs.github.com/actions
- **PWA Guide:** https://web.dev/progressive-web-apps/
- **Supabase Docs:** https://supabase.com/docs
- **Render Docs:** https://render.com/docs

### Archivos Clave del Proyecto

| Archivo | ¿Qué es? | ¿Cuándo editarlo? |
|---------|----------|-------------------|
| `.github/workflows/mobile-commands.yml` | Workflow de GitHub Actions | Para agregar nuevos comandos |
| `.github/ISSUE_TEMPLATE/*.yml` | Templates de issues | Para personalizar formularios |
| `templates/index.html` | Frontend de la PWA | Para cambiar interfaz |
| `static/js/app.js` | Lógica del frontend | Para agregar funcionalidades |
| `CLAUDE.md` | Instrucciones para Claude Code | Para que Claude entienda el proyecto |

---

## 🎉 Conclusión

Con este sistema puedes:

✅ Gestionar chistes desde cualquier lugar
✅ Ejecutar comandos de desarrollo desde tu móvil
✅ Desplegar actualizaciones sin computadora
✅ Monitorear el estado de tu proyecto en tiempo real
✅ Trabajar offline cuando no hay internet

**¿Preguntas?** Abre un issue en GitHub o consulta con Claude Code.

---

**Última actualización:** 2025-11-22
**Versión:** 1.0.0
